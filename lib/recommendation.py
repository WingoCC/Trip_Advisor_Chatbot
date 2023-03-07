import utils
import pandas as pd
import numpy as np
import nltk
import gensim.downloader
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity
from pprint import pprint as ppt
import mysql.connector


def generate_w2v_feature(words, w2v_model, feature_size=300):
    return np.mean([w2v_model[w] for w in nltk.word_tokenize(words) if w in w2v_model]
                   or [np.zeros(feature_size)], axis=0)


def find_most_similar_toplist(toplist_df, sentence, w2v_model, threshold=0.3):
    x = generate_w2v_feature(sentence, w2v_model).reshape(1, -1)
    similarity_with_toplist = np.array(
        [cosine_similarity(x, cur_toplist_feature.reshape(1, -1))
         for cur_toplist_feature in toplist_df["feature"]]
    ).reshape((-1, ))
    idx = similarity_with_toplist.argmax()
    return toplist_df["id"][idx] if similarity_with_toplist[idx] > threshold else -1


def find_most_similar_destination(destination_df, sentence, w2v_model, threshold=0.3):
    x = generate_w2v_feature(sentence, w2v_model).reshape(1, -1)
    similarity_with_destination = np.array(
        [cosine_similarity(x, cur_destination_feature.reshape(1, -1))
         for cur_destination_feature in destination_df["feature"]]
    ).reshape((-1, ))
    idx = similarity_with_destination.argmax()
    return destination_df["id"][idx] if similarity_with_destination[idx] > threshold else -1


def find_most_similar_review(review_df, sentence, w2v_model, threshold=0.3):
    x = generate_w2v_feature(sentence, w2v_model).reshape(1, -1)
    similarity_with_review = np.array(
        [cosine_similarity(x, cur_review_feature.reshape(1, -1))
         for cur_review_feature in review_df["feature"]]
    ).reshape((-1, ))
    idx = similarity_with_review.argmax()

    return review_df["id"][idx] if similarity_with_review[idx] > threshold else -1


def recommend_toplist_by_sentence(toplist_df, sentence, w2v_model, db_connector):
    toplist_id = find_most_similar_toplist(toplist_df, sentence, w2v_model)
    if toplist_id == -1:
        return None
    mycursor = db_connector.cursor(buffered=True)
    mycursor.execute("SELECT * FROM toplist WHERE id=%d" % toplist_id)
    toplist = mycursor.fetchone()

    return {"id": toplist[0], "name": toplist[1], "link": toplist[2]}


def recommend_destination_by_sentence(destination_df, sentence, w2v_model, db_connector):
    destination_id = find_most_similar_destination(destination_df, sentence, w2v_model)
    if destination_id == -1:
        return None
    mycursor = db_connector.cursor(buffered=True)
    mycursor.execute("SELECT * FROM destination WHERE id=%d" % destination_id)
    destination = mycursor.fetchone()

    return {"id": destination[0], "name": destination[1], "link": destination[2], "description": destination[3],
            "location_tags": destination[4], "attractions_link": destination[5],
            "restaurants_link": destination[6], "tours_link": destination[7],
            "trip_moments_link": destination[8]}


def recommend_attraction_by_sentence(review_df, sentence, w2v_model, db_connector):
    review_id = find_most_similar_review(review_df, sentence, w2v_model)
    if review_id == -1:
        return None
    mycursor = db_connector.cursor(buffered=True)
    mycursor.execute("SELECT * FROM attraction, attraction_and_review WHERE attraction.id=attraction_and_review.attraction_id and review_id=%d" % 536)
    attraction = mycursor.fetchone()

    return {"id": attraction[0], "name": attraction[1], "link": attraction[2],
            "location_tags": attraction[3], "open_status": attraction[4],
            "recommended_sightseeing_time": attraction[5], "phone": attraction[6],
            "address": attraction[7]}


if __name__ == '__main__':
    w2v_model = gensim.downloader.load('word2vec-google-news-300')
    db_connector = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        passwd="chatbot5125",
        database="trip_info"
    )

    toplist_df = utils.load_file_as_obj("../meta/toplist_df.pk")
    # tid = find_most_similar_toplist(toplist_df, "PHP is the best programming language", w2v_model)
    ppt(recommend_toplist_by_sentence(toplist_df, "Best Asia-Pacific Travel Destinations", w2v_model, db_connector))

    # print(tid)
    #
    # destination_df = utils.load_file_as_obj("../meta/destination_df.pk")
    # did = find_most_similar_destination(destination_df, "Try not to become a man of success. Rather become a man of value", w2v_model)
    # print(did)
    #
    # review_df = utils.load_file_as_obj("../meta/review_df.pk")
    # rid = find_most_similar_review(review_df, "A day without sunshine is like night", w2v_model)
    # print(rid)
