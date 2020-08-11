"""Main App for API
"""
from flask import Flask
from flask_restx import Api, Resource
from PIL import Image, UnidentifiedImageError
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.datastructures import FileStorage
from utils import load_pretrained_model, model_predict

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app=app,
          version="1.0",
          title="Deep Learning Model API",
          description="API for deep learning operations")
ns = api.namespace("api", description="prediction operations")
upload_parser = ns.parser()
upload_parser.add_argument("image",
                           location="files",
                           type=FileStorage,
                           required=True)
upload_parser.add_argument("model_name", type=str, required=True)
upload_parser.add_argument("model_type", type=int, required=True)

LOADED_MODEL = {"name": "dr-latest", "model": None}

LOADED_MODEL["model"] = load_pretrained_model("dr-latest", model_type=0)


@ns.route("/v1/predict/")
@ns.expect(upload_parser)
class Predict(Resource):
    """ Run prediction of eye fundus images against chosen model """
    @ns.doc("Run prediction")
    def post(self):
        """Handles POST requests to /v1/predict endpoint in API namespace.

        Returns:
            Dict: Dictionary containing the prediction results for the image in the request.
        """
        args = upload_parser.parse_args()
        if args["model_name"] != LOADED_MODEL["name"]:
            LOADED_MODEL["model"] = load_pretrained_model(args["model_name"], args["model_type"])
            LOADED_MODEL["name"] = args["model_name"]
        try:
            img = Image.open(args["image"])
            res = model_predict(img, LOADED_MODEL["model"])
            return res
        except UnidentifiedImageError:
            return {
                "status": "error",
                "message": "Image cannot be opened and identified"
            }


if __name__ == "__main__":
    app.run(debug=False, port=5000, host="127.0.0.1")
