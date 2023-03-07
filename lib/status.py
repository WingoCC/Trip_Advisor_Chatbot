import random
from lib import recommendation
from lib.abstract_status import AbstractStatus


class StartStatus(AbstractStatus):
    def __init__(self):
        self.type = "StartStatus"
        self.end_topic = False

    def make_response(self):
        return ""


class GreetingStatus(AbstractStatus):
    def __init__(self):
        self.type = "GreetingStatus"
        self.end_topic = True

    def make_response(self):
        greeting = [
            "Hello!<br>What can I do for you?",
            "Hi Dear<br>What can I do for you?",
            "Nice to meet you!<br>What can I do for you?",
        ]
        return greeting[random.randint(0, len(greeting) - 1)]


class ToplistStatus1(AbstractStatus):
    def __init__(self):
        self.type = "ToplistStatus1"
        self.end_topic = False

    def make_response(self):
        return "It seems like you want a list of destinations.<br>Describe the places you want to find"


class ToplistStatus2(AbstractStatus):
    def __init__(self, toplist_df, sentence, w2v_model, db_connector):
        self.type = "ToplistStatus2"
        self.end_topic = True
        self.sentence = sentence
        self.toplist_df = toplist_df
        self.w2v_model = w2v_model
        self.db_connector = db_connector

    def make_response(self):
        # def recommend_toplist_by_sentence(toplist_df, sentence, w2v_model, db_connector)
        toplist = recommendation.recommend_toplist_by_sentence(
            self.toplist_df,
            self.sentence,
            self.w2v_model,
            self.db_connector
        )

        response = ""
        if toplist is None:
            response = "Sorry, no toplist founded<br> If you don't mind, please put it in another way and try it again."
        else:
            response = "Oh! I have found a toplist for you!<br>"
            if toplist["name"]:
                response += ("Toplist name: <br>" + toplist["name"] + "<br>")
            if toplist["link"]:
                response += ("Toplist link: <br>" + toplist["link"] + "<br>")
        return response


class DestinationStatus1(AbstractStatus):
    def __init__(self):
        self.type = "DestinationStatus1"
        self.end_topic = False

    def make_response(self):
        return "It seems like you want to find a destination.<br>What kind of destinations you want to go?"


class DestinationStatus2(AbstractStatus):
    def __init__(self, destination_df, sentence, w2v_model, db_connector):
        self.type = "DestinationStatus2"
        self.end_topic = True
        self.destination_df = destination_df
        self.sentence = sentence
        self.w2v_model = w2v_model
        self.db_connector = db_connector

    def make_response(self):
        # recommend_destination_by_sentence(destination_df, sentence, w2v_model, db_connector):
        destination = recommendation.recommend_destination_by_sentence(
            self.destination_df,
            self.sentence,
            self.w2v_model,
            self.db_connector
        )
        response = ""
        if destination is None:
            response = "Sorry! No destination in my database can be recommended to you."
        else:
            response = "Hey! Here is a destination you may want to go!<br>"
            if destination["name"]:
                response += ("Destination name: <br>" + destination["name"] + "<br>")
            if destination["link"]:
                response += ("Destination link: <br>" + destination["link"] + "<br>")
            if destination["description"]:
                response += ("Destination description: <br>" + destination["description"] + "<br>")
            if destination["location_tags"]:
                response += ("Destination location infomation: <br>" + destination["location_tags"] + "<br>")
            if destination["attractions_link"]:
                response += ("Attractions here: <br>" + destination["attractions_link"] + "<br>")
            if destination["restaurants_link"]:
                response += ("Restaurants here: <br>" + destination["restaurants_link"] + "<br>")
            if destination["tours_link"]:
                response += ("Tours here: <br>" + destination["tours_link"] + "<br>")
            if destination["trip_moments_link"]:
                response += ("People's trip moments: <br>" + destination["trip_moments_link"] + "<br>")

        return response


class AttractionStatus1(AbstractStatus):
    def __init__(self):
        self.type = "AttractionStatus1"
        self.end_topic = False

    def make_response(self):
        return "It seems like you want to find an attraction.<br>What kind of attractions do you like?"


class AttractionStatus2(AbstractStatus):
    def __init__(self, review_df, sentence, w2v_model, db_connector):
        self.type = "AttractionStatus2"
        self.end_topic = True
        self.review_df = review_df
        self.sentence = sentence
        self.w2v_model = w2v_model
        self.db_connector = db_connector

    def make_response(self):
        # def recommend_attraction_by_sentence(review_df, sentence, w2v_model, db_connector):
        attraction = recommendation.recommend_attraction_by_sentence(self.review_df,
                                                                     self.sentence,self.w2v_model,
                                                                     self.db_connector)
        response = ""
        if attraction is None:
            response = "Sorry! There is no attraction founded for you"
        else:
            response = "Look! Here is the place!<br>"
            if attraction["name"]:
                response += ("Attraction name:<br>" + attraction["name"] + "<br>")
            if attraction["link"]:
                response += ("Attraction link:<br>" + attraction["link"] + "<br>")
            if attraction["location_tags"]:
                response += ("Attraction location information:<br>" + attraction["location_tags"] + "<br>")
            if attraction["open_status"]:
                response += ("Attraction open status:<br>" + attraction["open_status"] + "<br>")
            if attraction["recommended_sightseeing_time"]:
                response += ("Attraction recommended sightseeing time:<br>" + attraction["recommended_sightseeing_time"] + "<br>")
            if attraction["phone"]:
                response += ("Attraction contact information:<br>" + attraction["phone"] + "<br>")
            if attraction["address"]:
                response += ("Attraction address:<br>" + attraction["address"] + "<br>")
        return response


class IrrelevantStatus(AbstractStatus):
    def __init__(self):
        self.type = "IrrelevantStatus"
        self.end_topic = True

    def make_response(self):
        return "Sorry! I don't understand"


class ErrorStatus(AbstractStatus):
    def __init__(self):
        self.type = "ErrorStatus"
        self.end_topic = True

    def make_response(self):
        return "Sorry! error happened!<br>@#$!%!@#$#$%$%^@@"
