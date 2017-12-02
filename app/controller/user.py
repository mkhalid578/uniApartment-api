
import json

from peewee import DoesNotExist, IntegrityError
from flask import Blueprint, request, Response

from app.models.user import User
from app.models.property import Property


user = Blueprint('user', __name__)


@user.route('/user', methods=['POST'])
def create_user():
    content = request.get_json()
    new_user = User()
    new_user.FirstName = content.get("FirstName")
    new_user.LastName = content.get("LastName")
    new_user.Password = content.get("Password")
    new_user.University = content.get("University")
    new_user.Email = content.get("Email")

    try:
        new_user.save()
    except IntegrityError:
        return Response(status=409)

    return json.dumps(new_user.to_dict())


@user.route('/user', methods=['GET'])
def get_all_users():
    return json.dumps([user.to_dict() for user in User.select()])

@user.route('/user/<id>', methods=['GET'])
def get_by_id(id):
    try:
        got_user = User.get(User.id == id)
        return json.dumps(got_user.to_dict())

    except DoesNotExist:
        return Response(status = 404)

@user.route('/user/<key>=<value>', methods=['GET'])
def get_user_by_name_or_email(key, value):
    key = str(key).lower()

    jsonDict = {}
    got_user = None

    if key == 'id':
        try:
            got_user = User.get(User.id == value)
            jsonDict = got_user.to_dict()
            return json.dumps( got_user.to_dict())

        except DoesNotExist:
            return Response(status=404)

    elif key == 'username':
        try:
            got_user = User.get(User.Username == value)
            jsonDict = got_user.to_dict()
            return json.dumps( got_user.to_dict())

        except DoesNotExist:
            return Response(status=404)        

    return Response(status = 404)


@user.route('/user/<id>/property', methods=['GET'])
@user.route('/user/<key>=<value>/property', methods=['GET'])
def get_users_properts(id = None, key = None, value = None):
    content = request.get_json()
    keys = ['email', 'username']

    if id != None:
        return json.dumps([prop.to_dict() for prop in Property.select().where( Property.Interested.contains(id))])

    elif str(key).lower() in keys:
        try:
            got_user = None

            if str(key).lower() == 'email':
                got_user = User.get(User.Email == value)

            elif str(key).lower() == 'username':
                got_user = User.get(User.Username == value)

        except DoesNotExist:
            return Response(status = 409)

        return json.dumps([prop.to_dict() for prop in Property.select().where( Property.Interested.contains(got_user.id))])

    return Response(status = 404)


@user.route('/user/login', methods=['POST'])
def login_user():
    # this is not safe at all I know it will be improved if time allows 
    content = request.get_json()

    if 'Email' in list(content.keys()) or 'Password' in list(content.keys()):
        try:
            pass
            got_user = User.get(User.Email == str(content['Email']))

            if got_user.Password == content['Password']:
                # this can be edited to what ever the front end needs
                return json.dumps({'id': got_user.id})
            else:
                return Response(status = 203)
        except DoesNotExist:
            return Response(status = 404)

    return Response(status=404)

@user.route('/user/<id>', methods=['PUT'])
def update_user(id):
    # this will probably need changed for ease of use
    content = request.get_json()

    if "newPassword" in content.keys() and "Password" in content.keys():
        try:
            update_user = User.get(User.id == id)
            if update_user.Password == content['Password']:
                update_user.Password = content['newPassword']

                # this save may need a try/catch
                update_user.save()

                return json.dumps({'id' : id})
            else:
                return Response(status = 418)

        except DoesNotExist:
            return Response(status = 404)


    return Response(status=404)

@user.route('/user/<id>', methods=['DELETE'])
@user.route('/user/<key>=<value>', methods=['DELETE'])
def delete_user(id =None, key = None, value = None):

    content = request.get_json()
    keys = ['email', 'username']

    if id != None:
        try:
            got_user = User.get(User.id == id)

        except DoesNotExist:
            return Response(status = 409)

        if got_user.Password == content['Password']:
            try:
                got_user.delete_instance()
                return Response(status = 200)

            except IntegrityError:
                return Response(status=409)  

    elif str(key).lower() in keys:
        try:
            got_user = None

            if str(key).lower() == 'email':
                got_user = User.get(User.Email == value)

            elif str(key).lower() == 'username':
                got_user = User.get(User.Username == value)

        except DoesNotExist:
            return Response(status = 409)

        if got_user.Password == content['Password']:
            try:
                got_user.delete_instance()
                return Response(status = 200)

            except IntegrityError:
                return Response(status=409)  
        
        else:
            return Response(status = 203)

    return Response(status = 404)








