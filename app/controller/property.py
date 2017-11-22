
import json

from peewee import DoesNotExist, IntegrityError
from flask import Blueprint, request, Response, jsonify

from app.models.property import Property

from app import app
property = Blueprint('property', __name__)

@property.route('/property', methods=['POST'])
def get_or_create_property():
    '''
        gets a post request with a json property object
        creates a db instance of json property 
        returns id of db instance
    '''
    content = request.get_json()


    new_property = Property().get_or_create(
    Available = content.get("Available"),
    Rent = content.get("Rent"),
    Beds = content.get("Beds"),
    Baths = content.get("Baths"),
    Pets = content.get("Pets"),
    Features = content.get("Features"),
    Address = content.get("Address"),
    imageUrl = content.get("ImageUrl")
        )[0]
    if new_property.Interested is not None and str(content.get("id")) not in str(new_property.Interested):
        interested  ="{} {} {}".format(new_property.Interested , ' ' , str(content.get("id")))
        print(interested)
        new_property.Interested = interested
        new_property.save()
    print(new_property)
    try:
        pass
        # new_property.save(force_insert = True)
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

@property.route('/property/<id>', methods = ['PUT'])
def update_property( id):
    # key will be a unique value eventually
    # so only value will be passed

    content = request.get_json()
    # print(content)

    updateKey = list(content.keys())[0]
    updating_property = Property.get(Property.id == id)

    # print(updating_property._data)

    if len(list(content.keys())) == 0:
        return Response(status = 303)

    elif updateKey is not None and updateKey in updating_property._data.keys():
        # print(updateKey)

        updating_property._data[updateKey] = content[updateKey]
        
        try:
            updating_property.save()
            return json.dumps(updating_property.to_dict())

        except IntegrityError:
            return Response(status=409)
       
    else:
        # key does not exist in table status 
        return Response(status = 404)

@property.route('/property/<id>', methods = ['DELETE'])
def delete_property(id):

    try:
        deleteing_property = Property.get(Property.id == id)
    except DoesNotExist:
        return Response(status = 404)
    try:
        deleteing_property.delete_instance()
        return Response(status = 200)

    except IntegrityError:
            return Response(status=409)      

    return Response(status = 404)







