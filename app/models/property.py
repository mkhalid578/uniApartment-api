from peewee import * 
import json 

from app import db

from app.models.user import User


# db table
class Property(Model):
    Available = BooleanField()
    Rent = IntegerField()
    Beds = IntegerField()
    Baths = IntegerField()
    Pets = BooleanField()
    Features = TextField()
    ContactInfo = TextField()
    Address = TextField()
    # this should also be contact information but for simplicity we will have non of that 

    # owner = ForeignKeyField(User, to_field = id, related_name='property')

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
        return JsonData

# Property( Available = True, Rent =50, Beds = 3, Baths =1, Pets =False, Features= "no features",ContactInfo= "this guy->", Address ="mordor")