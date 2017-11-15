
import json

from peewee import DoesNotExist, IntegrityError
from flask import Blueprint, request, Response, jsonify

from app.models.property import Property

from app import app
property = Blueprint('property', __name__)

@property.route('/property', methods=['POST'])
def create_property():
    '''
        gets a post request with a json property object
        creates a db instance of json property 
        returns id of db instance
    '''
    new_property = Property()
    # uncomment for debugging
    # print(request.get_json())
    content = request.get_json()
    new_property.Available = content.get("Available")
    new_property.Rent = content.get("Rent")
    new_property.Beds = content.get("Beds")
    new_property.Baths = content.get("Baths")
    new_property.Pets = content.get("Pets")
    new_property.Features = content.get("Features")
    new_property.ContactInfo = content.get("ContactInfo")
    new_property.Address = content.get("Address")

    try:
        new_property.save(force_insert = True)
    except IntegrityError:
        return Response(status=409)

    return json.dumps({'id': new_property.id})

@property.route('/property', methods = ['GET'])
def get_all_property():
    '''
        gets a get request for property
        return a json list of dictionaries of the properties
    '''
    # simple list comprehensions
    return json.dumps([prop.to_dict() for prop in Property.select()])

@property.route('/property/<key>=<value>', methods = ['GET'])
def get_specific_property(key, value):
    '''
        gets a request with query of key and value
        checks to see if they key exists in the db table
        searches for the value at that key 
        returns a list of values that match
    '''
    # this is not really that safe we are allow outside sources look in and 
    #  see what db tech we are using
    if key in Property.__dict__.keys():
        # uncomment for debugging 
        # print(key ,' ', type(key), '   ', value, ' ', type(value))

        # this will need a 'where like' statement for the textfields
        return json.dumps(
                [prop.to_dict() for prop in Property.select().where(Property.__dict__[key].field == int(value))] )
    else:
        # we need a status that says the query is bad because of the key
        return Response(status = 404)

@property.route('/property/<key>=<value>', methods = ['PUT'])
def update_property(key, value):
    # key will be a unique value eventually
    # so only value will be passed

    content = request.get_json()
    print(content)
    updateKey = None
    if key in Property.__dict__.keys():
        updating_property = Property.get(Property.__dict__[key].field == int(value))
        
        if len(list(content.keys())) > 0 and updateKey in Property.__dict__.keys():
            updateKey = list(content.keys())[0]
            print(updateKey)
            # updateQ = Property.update(Property.__dict__[updateKey] = content[updateKey]).where(key == value)
            # updateQ.execute()
            # updating_property.__dict__[updateKey] = content[updateKey]
            print(updating_property.__dict__)
            # updating_property.save()
            print(updating_property.__dict__)

        return json.dumps(updating_property.to_dict())
    else:
        # key does not exist in table status 
        return Response(status = 409)









