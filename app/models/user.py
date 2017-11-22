from peewee import * 
import json 

from app import db

# user db table
class User(Model):
    # fields in the db table
    Username = CharField(unique = True)
    Password = CharField()
    # this should not be null will need fixed
    Email = CharField(unique =True)
    University = CharField()

    class Meta:
        database = db

    # helper functions for json parsing 
    def __str__(self):
        return json.dumps(self.__dict__["_data"])

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        JsonData = dict()
        JsonData.update(self.__dict__["_data"])
        JsonData.pop("Password")
        return JsonData



        