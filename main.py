from flask import Flask, render_template, request, send_from_directory, jsonify
import utils
from chatbot_config import CHATBOT_CONFIG
from lib import intent_classificion
from lib.status import *
import gensim.downloader
import mysql.connector

intent_classification_svc = utils.load_file_as_obj(CHATBOT_CONFIG["INTENT_CLASSIFIER_SVM_PATH"])
w2v_model = gensim.downloader.load('word2vec-google-news-300')
toplist_df = utils.load_file_as_obj(CHATBOT_CONFIG["TOPLIST_DF"])
destination_df = utils.load_file_as_obj(CHATBOT_CONFIG["DESTINATION_DF"])
review_df = utils.load_file_as_obj(CHATBOT_CONFIG["ATTRACTION_DF"])
db_connector = mysql.connector.connect(**CHATBOT_CONFIG["DATABASE_CONFIG"])

app = Flask(__name__, template_folder='templates')
app.static_folder = './templates/'

cur_status = StartStatus()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get_response", methods=["POST"])
def get_bot_response():
    chat_history = utils.convert_request_form_to_list(request.form)

    global cur_status
    cur_status = next_status(cur_status, chat_history[-1]["content"])
    response = cur_status.make_response()

    if cur_status.end_topic:
        cur_status = StartStatus()

    return jsonify(response)


@app.route('/images/<filename>')
def send_images_needs_by_javascript(filename):
    return send_from_directory('templates/images', filename)


def next_status(cur_status, user_input):
    try:
        new_status = None
        if cur_status.type == "StartStatus":
            intent_idx, intent_name = intent_classificion.inference(intent_classification_svc, user_input, w2v_model)
            if intent_name == "greeting":
                new_status = GreetingStatus()
                return new_status
            if intent_name == "toplist":
                new_status = ToplistStatus1()
                return new_status
            if intent_name == "destination":
                new_status = DestinationStatus1()
                return new_status
            if intent_name == "attraction":
                new_status = AttractionStatus1()
                return new_status
            if intent_name == "irrelevant":
                new_status = IrrelevantStatus()
                return new_status
        if cur_status.type == "ToplistStatus1":
            new_status = ToplistStatus2(toplist_df=toplist_df,
                                        sentence=user_input,
                                        w2v_model=w2v_model,
                                        db_connector=db_connector)
            return new_status
        if cur_status.type == "DestinationStatus1":
            new_status = DestinationStatus2(destination_df=destination_df,
                                            sentence=user_input,
                                            w2v_model=w2v_model,
                                            db_connector=db_connector)
            return new_status
        if cur_status.type == "AttractionStatus1":
            new_status = AttractionStatus2(review_df=review_df,
                                           sentence=user_input,
                                           w2v_model=w2v_model,
                                           db_connector=db_connector)
            return new_status
        return ErrorStatus() if new_status is None else new_status
    except:
        new_status = ErrorStatus()
        return new_status


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
