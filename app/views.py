# -*- encoding: utf-8 -*-

import io
import json
from hashlib import sha1

import requests
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.shortcuts import redirect, render
from PIL import Image

from .diagnosis import DRDiagnosis
from .models import DRModel, TestImage
from .util_funcs import (check_if_already_tested, check_if_rgba,
                         convert_rgba_to_rgb,
                         make_inMemoryUploadedFile_from_PIL_image)

DIAG = DRDiagnosis()

PREDICTION_API_ENDPOINT = "http://localhost:5000/api/v1/predict"


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")


@login_required(login_url="/login/")
def profile(request):
    return render(request, "accounts/profile.html", {"alpha": "beta"})


@login_required(login_url="/login/")
def results(request):
    return render(request, "results.html", {"msg": "Hello"})


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
                    return render(request, "results.html", context=context)

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
                return render(request, "results.html", context=context)
            except IntegrityError:
                pass
            except Exception as error:
                print(type(error), error)

    return render(request, "predict.html", context)


@login_required(login_url="/login/")
def image_labelize(request):
    context = {}
    return render(request, "non-labelized.html", context)


@login_required(login_url="/login/")
def correct_prediction(request):
    context = {}
    if request.method == "POST":
        name = request.POST["name"]
        if request.POST["name"] and request.POST["reallabel"]:

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
                return render(request, "results.html", context=context)
            else:
                return redirect('predict')
    else:
        return redirect('predict')
