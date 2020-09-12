# -*- encoding: utf-8 -*-

import os
import io
import json
from hashlib import sha1

import requests
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from PIL import Image

from .diagnosis import DRDiagnosis
from .models import DRModel, TestImage
from .util_funcs import (check_if_already_tested, check_if_rgba,
                         convert_rgba_to_rgb,
                         make_inMemoryUploadedFile_from_PIL_image)
from datetime import datetime

DIAG = DRDiagnosis()

PREDICTION_API_ENDPOINT = "http://localhost:5000/api/v1/predict"


@login_required(login_url="/login/")
def index(request):
    context = {}
    users = User.objects.all()
    context["num_users"] = len(users)
    return render(request, "index.html.j2", context=context)


@login_required(login_url="/login/")
def profile(request):
    return render(request, "accounts/profile.html.j2", {"alpha": "beta"})


@login_required(login_url="/login/")
def results(request):
    return render(request, "results.html.j2", {"msg": "Hello"})


@login_required(login_url="/login/")
def prediction(request):
    context = {}
    if request.method == "POST":
        if request.FILES:
            try:
                image_file = Image.open(request.FILES["test-image"])
                if check_if_rgba(image_file):
                    image_file = convert_rgba_to_rgb(image_file)
                image_bytes = io.BytesIO()
                image_file.save(image_bytes, image_file.format)
                data = {"model_name": "dr-latest", "model_type": 0}
                model = DRModel.objects.filter(name=data["model_name"]).first()
                if model is None:
                    return redirect(request, "predict.html")
                image_pk = f"{sha1(image_bytes.getvalue()).hexdigest()}"
                r_val, message, instance = check_if_already_tested(image_pk)
                if r_val:
                    context["message"] = message
                    context["instance"] = instance
                    context["stade"] = DIAG.get(int(instance.pred_class),
                                                "stade")
                    context["description"] = DIAG.get(int(instance.pred_class),
                                                      "description")
                    context["uistyle"] = DIAG.get(int(instance.pred_class),
                                                  "uistyle")
                    return render(request, "results.html.j2", context=context)

                resp = requests.post(PREDICTION_API_ENDPOINT,
                                     data=data,
                                     files={"image": image_bytes.getvalue()})
                resp_json = resp.json()
                preds = ",".join([
                    "{:.6f}".format(resp_json["predictions"][key])
                    for key in resp_json["predictions"].keys()
                ])
                image_in_mem = make_inMemoryUploadedFile_from_PIL_image(
                    image_file)
                instance = TestImage(name=image_pk,
                                     image=image_in_mem,
                                     author=request.user,
                                     pred_class=json.loads(
                                         resp.text)["pred_class"],
                                     preds=preds,
                                     model=model)
                instance.save()
                context["instance"] = instance
                context["message"] = "success!"
                context["stade"] = DIAG.get(instance.pred_class, "stade")
                context["description"] = DIAG.get(instance.pred_class,
                                                  "description")
                context["uistyle"] = DIAG.get(instance.pred_class, "uistyle")
                return render(request, "results.html.j2", context=context)
            except IntegrityError:
                pass
            except Exception as error:
                print(type(error), error)

    return render(request, "predict.html.j2", context)


@login_required(login_url="/login/")
def image_labelize(request, page):
    context = {}
    images_list = TestImage.objects.all()
    paginator = Paginator(images_list, 6)
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        images = paginator.page(paginator.num_pages)
    context["images"] = images
    return render(request, "non-labelized.html.j2", context=context)


@login_required(login_url="/login/")
def correct_prediction(request):
    context = {}
    if request.method == "POST":
        name = request.POST["name"]
        reallabel = request.POST["reallabel"]
        if name and reallabel:
            instance = TestImage.objects.filter(name=name).first()
            if instance:
                instance.real_label = request.POST["reallabel"]
                instance.save()
                if int(instance.real_label) == int(instance.pred_class):
                    context[
                        "message"] = f"Both doctor and model predicted the image as class {instance.real_label}"
                else:
                    context[
                        "message"] = f"Doctor labelized image as class {instance.real_label}, but model predicted class {instance.pred_class}"
                context["instance"] = instance
                context["stade"] = DIAG.get(int(instance.pred_class), "stade")
                context["description"] = DIAG.get(int(instance.pred_class),
                                                  "description")
                context["uistyle"] = DIAG.get(int(instance.pred_class),
                                              "uistyle")
                return render(request, "corrected.html.j2", context=context)
            else:
                return redirect('predict')
    else:
        return redirect('predict')


@login_required(login_url="/login/")
def result_name(request, name):
    context = {}
    r_val, message, instance = check_if_already_tested(name)
    if r_val:
        context["message"] = message
        context["instance"] = instance
        context["stade"] = DIAG.get(int(instance.pred_class),
                                    "stade")
        context["description"] = DIAG.get(int(instance.pred_class),
                                            "description")
        context["uistyle"] = DIAG.get(int(instance.pred_class),
                                        "uistyle")
        return render(request, "results.html.j2", context=context)
    else:
        return render(request, "index.html.j2")


@login_required(login_url="/login/")
def gen_report(request, name):
    #check_if_pdf_exists()
    instance = TestImage.objects.filter(name=name).first()
    pdf_template_json = open("media/reports_data/template.json", "r", encoding='utf-8')
    pdf_data_json = json.load(pdf_template_json)
    if instance:
        model_name = instance.model.name
        preds = list(map(float, instance.preds.split(',')))
        pred_class = instance.pred_class
        real_label = instance.real_label
        eye_orientation = instance.eye_orientation
        author = instance.author.username
        generated_at = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        pdf_data_json["rapport_gentime"] = generated_at
        pdf_data_json["pred_class"] = str(pred_class)
        if real_label:
            pdf_data_json["real_label"] = real_label
        if eye_orientation:
            pdf_data_json["eye_orientation"] = eye_orientation
        pdf_data_json["model_name"] = model_name
        pdf_data_json["author"] = author
        diagnostic = DIAG.get(int(instance.pred_class), "description")
        pdf_data_json["diagnostic"] = diagnostic
        pdf_data_json["stade"] = DIAG.get(int(instance.pred_class), "stade")
        pdf_data_json["db_name"] = instance.name


        pdf_data_json["top_holdings"][0]["amount"] = str(preds[0])
        pdf_data_json["top_holdings"][1]["amount"] = str(preds[1])
        pdf_data_json["top_holdings"][2]["amount"] = str(preds[2])
        pdf_data_json["top_holdings"][3]["amount"] = str(preds[3])
        pdf_data_json["top_holdings"][4]["amount"] = str(preds[4])



        # CREATE JSON FILE FOR REPORT
        pdf_template_json.close()
        json_pdf_new = open(f"media/reports_data/{instance.name}.json", "w")

        # DUMP jSON IN FILE

        json.dump(pdf_data_json, json_pdf_new)
        json_pdf_new.close()

        # PDF GENERATION
        #command = "ls"
        command = f'cd report; python3 gen_factsheet.py ../media/reports_data/{instance.name}.json'
        os.system(command)


        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{instance.name}.pdf"'
        f = open(
            f'media/reports/{instance.name}.pdf',
            'rb')
        data = f.read()
        response.write(data)
        return response
    else:
        return redirect('predict')
