from flask import Flask, request
from flask_restx import Resource, Api
import json
import os
from base64 import b64decode

from tamr_unify_client.client import Client
from tamr_unify_client.auth import UsernamePasswordAuth
import tamr_toolbox.utils as tbu

from backend.example_package.example_module import get_all_project_names, get_all_dataset_names
from backend.example_package.example_form import setup_tamr_form

# Import apidoc for monkey patching
from flask_restx.apidoc import apidoc

URL_PREFIX = '/api'

# Make a global change setting the URL prefix for the swaggerui at the module level
apidoc.url_prefix = URL_PREFIX

# set up basic authentication following https://flask-restx.readthedocs.io/en/latest/swagger.html#documenting-authorizations
# which is based on top of https://swagger.io/docs/specification/2-0/authentication/basic-authentication/
authorizations = {
    'BasicAuth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    },
}

# simple setup for one user set via environment variables
my_app_username = os.environ.get("APP_USERNAME")
my_app_password = os.environ.get("APP_PASSWORD")

# don't start the app if these aren't set
if my_app_password is None or my_app_password is None:
    raise RuntimeError(f"App not setup correctly for authentication set the environment variables APP_USERNAME and APP_PASSWORD")


app = Flask(__name__, static_folder='../frontend/my-app/build', static_url_path='/')
app.config['SWAGGER_UI_DOC_EXPANSION'] = 'list'
api = Api(app,
          doc="/docs",
          version='0.1.0',
          title='Tamr Field Flask API',
          description='An example Tamr API',
          prefix='/api',
          authorizations=authorizations,
          )


@app.route('/')
def home():
    """Returns home page"""
    return app.send_static_file('index.html')


project_ns = api.namespace('projects/', description='Operations related to Tamr projects')
@api.route('/projects')
class Projects(Resource):
    """
    Assumes you are passed a form request containing information to connect to a Tamr instance
    """
    tamr_form = setup_tamr_form()
    @api.response(200, 'Projects successfully returned')
    @api.doc(security='BasicAuth')
    @api.expect(tamr_form, validate=True)
    def post(self):
        """Returns list of projects"""

        # First parse the header for credentials:
        try:
            encoded_auth_header_bytes = request.headers['Authorization'].split()[1].encode('utf-8')
            username, password = b64decode(encoded_auth_header_bytes).decode('utf-8').split(':')
            if username != my_app_username or password != my_app_password:
                raise ValueError()
        # this is too broad except that if anything above breaks it means authorization isn't correct
        except Exception:
            resp = app.response_class(
                response=json.dumps("credentials are required to access this resource."),
                status=401,
                content_type='application/json'
            )
            return resp


        host = request.form['Host']
        user = request.form['Username']
        password = request.form['Password']
        auth = UsernamePasswordAuth(user, password)
        protocol = request.form['Protocol']
        port = request.form['Port']
        tamr = Client(auth, host=host, protocol=protocol, port=port)
        projects = get_all_project_names(tamr)
        return {'projects': projects}, 200


@api.route('/datasets')
class Datasets(Resource):
    """
    This is just to demonstrate behavior if you *don't* need to have flexibility of reaching any tamr instance
    and instead can just specify it via config file.

    NOTE THIS ENDPOINT WILL BREAK AS-IS SINCE THERE IS NO REAL CONFIG FILE
    """

    @api.response(204, 'Datasets successfully returned')
    def get(self):
        """Returns list of datasets"""
        config = tbu.config.from_yaml("path/to/yaml/file")
        tamr = tbu.client.create(**config["my_instance"])
        return json.dumps(get_all_dataset_names(tamr)), 204
