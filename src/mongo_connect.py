import mongoengine

from parameters import parameters


def connect_to_mongo():
    mongoengine.connect(host=parameters["mongo_url"])
