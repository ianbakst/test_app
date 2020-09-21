from flask_restx import reqparse


def setup_tamr_form() -> reqparse.RequestParser:
    # make a request parser to power swagger form and be able to validate request
    tamr_form_arguments = reqparse.RequestParser()
    tamr_form_arguments.add_argument('Host', type=str, required=True, help='Tamr hostname to which to connect', location='form')
    tamr_form_arguments.add_argument('Port', type=str, required=True, help='Port on which Tamr is running', default='9100', location='form')
    tamr_form_arguments.add_argument('Username', type=str, required=True, help='Tamr username as whom to authenticate', location='form')
    tamr_form_arguments.add_argument('Password', type=str, required=True, help='Tamr user password', location='form')
    tamr_form_arguments.add_argument('Protocol', type=str, required=True, help='One of http, https', default='http', location='form')

    return tamr_form_arguments