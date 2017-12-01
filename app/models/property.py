from peewee import * 
import json 

from app import db

from app.models.user import User

       # this.priceLow = priceLow;
       #  this.priceHigh = priceHigh;
       #  this.minBed = minBed;
       #  this.maxBed = maxBed;
       #  this.rating = rating;
       #  this.imgURL = imgURL;
       #  this.aptNumber = aptNumber;
       #  this.street = street;
       #  this.city = city;
       #  this.state = state;
       #  this.zip = zip;
       #  this.address = new Address(this.aptNumber, this.street, this.city, this.state, this.zip);
    # this stuff plus features. 
# db table
class Property(Model):
    Rent = FloatField()
    PriceLow = FloatField()
    PriceHigh = FloatField()
    minBed = IntegerField()
    maxBed = IntegerField()
    Rating = FloatField()
    imageUrl = TextField()

    AptNumber = CharField()
    Street = CharField()
    City = CharField()
    State = CharField()
    Zip = CharField()
    Address = TextField()

    AppartmentName = TextField()
    Description = TextField()
    Features = TextField()
    PhoneContact = TextField()
    Availabilty = BooleanField()

    University = TextField()
    Owner = ForeignKeyField(User)
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
        # ThisOwner = None
        # try:
        #     ThisOwner = User.get(User.id == self.Owner)
        # except:
        #     ThisOwner = 0

        # JsonData.update({Owner : ThisOwner})
        return JsonData

# Property( Available = True, Rent =50, Beds = 3, Baths =1, Pets =False, Features= "no features",ContactInfo= "this guy->", Address ="mordor")