"""Utilities
"""

import base64
import os
import re
from io import BytesIO
import numpy as np
import tensorflow as tf
from PIL import Image
from unipath import Path
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = Path(__file__).parent


def base64_to_pil(base64_img):
    """
    Convert base64 image data to PIL image
    """
    image_data = re.sub("^data:image/.+;base64,", "", base64_img)
    pil_image = Image.open(BytesIO(base64.b64decode(image_data)))
    return pil_image


def np_to_base64(img_np):
    """
    Convert numpy image (RGB) to base64 string
    """
    img = Image.fromarray(img_np.astype("uint8"), "RGB")
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buffered.getvalue()).decode("ascii")


def load_pretrained_model(name, model_type=0):
    if model_type == 0:
        model_path = os.path.join(BASE_DIR, f"app/trained_models/{name}/saved_model/")
        model = tf.keras.models.load_model(model_path)
        print("Model Loaded ...")
        return model
    else:
        return None


def model_predict(img, model):
    x_val = np.empty((1, 224, 224, 3), dtype=np.uint8)
    img = img.resize((224,) * 2)
    x_val[0, :, :, :] = img
    preds = model.predict(x_val)
    result = {}
    pred_proba = float("{:.3f}".format(np.amax(preds)))  # Max probability
    pred_class = int(np.argmax(np.squeeze(preds)))
    preds = preds.tolist()
    preds = list(map(lambda x: x * 100, preds[0]))
    result = {
        "predictions": {"0": preds[0], "1": preds[1], "2": preds[2], "3": preds[3], "4": preds[4]},
        "pred_proba": pred_proba,
        "pred_class": pred_class,
        "pred_at": datetime.now().strftime("%m/%d/%Y, %H:%M:%S"),
    }
    return result
