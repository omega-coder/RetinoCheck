from flask import Flask
from flask_restx import Api, Resource, reqparse
from werkzeug.middleware.proxy_fix import ProxyFix
from utils import load_pretrained_model, base64_to_pil, model_predict
from werkzeug.datastructures import FileStorage
from PIL import Image
import io

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app=app, version="1.0", title="Deep Learning Model API", description="API for deep learning operations")
ns = api.namespace("api", description="prediction operations")
upload_parser = ns.parser()
upload_parser.add_argument("image", location="files", type=FileStorage, required=True)
upload_parser.add_argument("model_name", type=str, required=True)
upload_parser.add_argument("model_type", type=int, required=True)


try:
    model = load_pretrained_model("dr-latest", model_type=0)
except Exception:
    print("Couldn't load model")


@ns.route("/v1/predict/")
@ns.expect(upload_parser)
class Predict(Resource):
    """ Run prediction of eye fundus images against chosen model """

    @ns.doc("Run prediction")
    def post(self):
        args = upload_parser.parse_args()
        print(args["image"])
        img = Image.open(args["image"])
        res = model_predict(img, model)
        return res


if __name__ == "__main__":
    app.run(debug=False, port=5000, host="0.0.0.0")
