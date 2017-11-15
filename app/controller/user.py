
import json

from peewee import DoesNotExist, IntegrityError
from flask import Blueprint, request, Response

from app.models.user import User


user = Blueprint('user', __name__)


@user.route('/user', methods=['POST'])
def create_user():
    new_user = User()
    new_user.Name = request.form.get("Name")
    new_user.Password = request.form.get("Password")
    new_user.Email = request.form.get("Email")
    new_user.Property = request.form.get("Property")

    try:
        new_user.save()
    except IntegrityError:
        return Response(status=409)

    return Response(status=200)

@user.route('/user', methods=['GET'])
def get_all_users():
	pass