from .modals import Admin, Customer, Professional, Review, Service, ServiceRequest
from flask_restful import Api , Resource, reqparse, abort, fields, marshal_with
from flask import request , jsonify

api = Api()

