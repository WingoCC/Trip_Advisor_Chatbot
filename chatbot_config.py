import os


CHATBOT_CONFIG = dict()

CHATBOT_CONFIG["INTENT_CLASSIFIER_SVM_PATH"] = "./meta/intent_classification_svc.pk"
CHATBOT_CONFIG["INTENT_CLASS_NAMES"] = ["greeting", "toplist", "destination", "attraction", "irrelevant"]
CHATBOT_CONFIG["TOPLIST_DF"] = "./meta/toplist_df.pk"
CHATBOT_CONFIG["DESTINATION_DF"] = "./meta/destination_df.pk"
CHATBOT_CONFIG["ATTRACTION_DF"] = "./meta/review_df.pk"

CHATBOT_CONFIG["DATABASE_CONFIG"] = {
    "host": os.environ.get("DATABASE_HOST", "localhost"),
    "port": os.environ.get("DATABASE_PORT", 3306),
    "user": os.environ.get("DATABASE_USER", "root"),
    "passwd":os.environ.get("DATABASE_PASSWD", "chatbot5125"),
    "database": os.environ.get("DATABASE_NAME", "trip_info")
}

