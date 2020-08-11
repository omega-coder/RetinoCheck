"""Utils for models
"""
import io
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import TestImage


def check_if_already_tested(image_pk):
    message = ""
    instance = TestImage.objects.filter(name=image_pk).first()
    if instance:
        pred_class = instance.pred_class
        real_label = instance.real_label
        if real_label:
            if real_label == pred_class:
                message = f"Both, Doctor and the model labeled eye as class {pred_class}"
            else:
                message = f"Doctor Labeled image as {real_label}, but model predicted {pred_class}"
        else:
            message = "Eye already tested, but not yet labeled by a Doctor!"
        return True, message, instance
    return False, message, instance


def check_if_rgba(pillow_image):
    return pillow_image.mode == "RGBA"


def convert_rgba_to_rgb(pillow_image):
    img_mode = pillow_image.mode
    img_format = pillow_image.format
    if img_mode == "RGBA":
        try:
            new_image = pillow_image.convert(mode='RGB')
            buffer = io.BytesIO()
            new_image.save(fp=buffer, format=img_format)
            return Image.open(buffer)
        except Exception as error:
            print(type(error), error)


def make_inMemoryUploadedFile_from_PIL_image(pil_image):
    image_format = pil_image.format
    image_mime = Image.MIME[image_format]
    image_name = f"tmp.{image_format.lower()}"
    buffer = io.BytesIO()
    pil_image.save(fp=buffer, format=image_format)
    c_file = ContentFile(buffer.getvalue())
    return InMemoryUploadedFile(c_file, None, image_name, image_mime,
                                c_file.tell, None)
