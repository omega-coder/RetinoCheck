# -*- encoding: utf-8 -*-


import io
import json
from hashlib import sha1

import requests
from django import template
from django.contrib.auth.decorators import login_required
from django.db.utils import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from PIL import Image

from .models import TestImage
from .diagnosis import DRDiagnosis

DIAG = DRDiagnosis()


@login_required(login_url="/login/")
def index(request):
    return render(request, "index.html")


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:
        load_template = request.path.split("/")[-1]
        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))
    except template.TemplateDoesNotExist:
        html_template = loader.get_template("error-404.html")
        return HttpResponse(html_template.render(context, request))
    except Exception:
        html_template = loader.get_template("error-500.html")
        return HttpResponse(html_template.render(context, request))


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
                im = request.FILES["test-image"]
                image_bytes = io.BytesIO(im.read())
                data = {"model_name": "dr-latest", "model_type": 0}
                im.seek(0)
                image_pk = f"{sha1(im.read()).hexdigest()}"
                instance = TestImage.objects.filter(name=image_pk).first()
                if instance:
                    if instance.real_label is not None:
                        if instance.real_label != "":
                            if int(instance.real_label) == int(instance.pred_class):
                                context["message"] = f"Both doctor and model predicted the image as class {instance.real_label}"
                            else:
                                context["message"] = f"Doctor labelized image as class {instance.real_label}, but model predicted class {instance.pred_class}"        
                        else:
                            context["message"] = "Already prredicted this image! (Not yet labelized!)"   
                    else:
                        context["message"] = "Already prredicted this image! (Not yet labelized!)"
                    context["instance"] = instance
                    context["stade"] = DIAG.get(int(instance.pred_class), "stade")
                    context["description"] = DIAG.get(int(instance.pred_class), "description")
                    context["uistyle"] = DIAG.get(int(instance.pred_class), "uistyle")
                    return render(request, "results.html", context=context)
                resp = requests.post("http://127.0.0.1:5000/api/v1/predict/", data=data, files={"image": image_bytes})
                im.seek(0)
                resp_json = resp.json()
                preds = ",".join(
                    ["{:.6f}".format(resp_json["predictions"][key]) for key in resp_json["predictions"].keys()]
                )
                instance = TestImage(
                    name=image_pk,
                    image=im,
                    author=request.user.username,
                    pred_class=json.loads(resp.text)["pred_class"],
                    preds=preds,
                )
                instance.save()
                context["instance"] = instance
                context["message"] = "success!"
                context["stade"] = DIAG.get(int(instance.pred_class), "stade")
                context["description"] = DIAG.get(int(instance.pred_class), "description")
                context["uistyle"] = DIAG.get(int(instance.pred_class), "uistyle")
                return render(request, "results.html", context=context)
            except IntegrityError:
                pass
            except Exception as e:
                print(type(e), e)
    return render(request, "predict.html", context)


@login_required(login_url="/login/")
def image_labelize(request):
    context = {}
    return render(request, "non-labelized.html", context)


@login_required(login_url="/login/")
def correct_prediction(request):
    context = {}
    if request.method == "POST":
        #import pdb; pdb.set_trace()
        name = request.POST["name"]
        if request.POST["name"] and request.POST["reallabel"]:

            instance = TestImage.objects.filter(name=name).first()
            if instance:
                instance.real_label = request.POST["reallabel"]
                instance.save()
                if int(instance.real_label) == int(instance.pred_class):
                    context["message"] = f"Both doctor and model predicted the image as class {instance.real_label}"
                else:
                    context["message"] = f"Doctor labelized image as class {instance.real_label}, but model predicted class {instance.pred_class}"        
                context["instance"] = instance
                context["stade"] = DIAG.get(int(instance.pred_class), "stade")
                context["description"] = DIAG.get(int(instance.pred_class), "description")
                context["uistyle"] = DIAG.get(int(instance.pred_class), "uistyle")
                return render(request, "results.html", context=context)
            else:
                return redirect('predict')
    else:
        return redirect('predict')
