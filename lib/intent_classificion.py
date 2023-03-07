from sklearn.svm import SVC
from copy import deepcopy
import pandas as pd
import gensim.downloader
import numpy as np
import nltk
from chatbot_config import CHATBOT_CONFIG
import utils


def generate_w2v_feature(words, feature_size=300):
    return np.mean([w2v_model[w] for w in nltk.word_tokenize(words) if w in w2v_model]
                   or [np.zeros(feature_size)], axis=0)


def sentence_augmentation(sentence, w2v_model, topn=30, threshold=0.5, expected_count=200):
    ret_list = list()
    for w in nltk.word_tokenize(sentence):
        if not w in w2v_model:
            continue
        similar_words = [cur_pair[0] for cur_pair in w2v_model.similar_by_word(w) if cur_pair[1] > threshold]
        if similar_words:
            ret_list.extend([sentence.replace(w, cur_similar_word) for cur_similar_word in similar_words])
    return ret_list


def get_dataset_by_description(description_list, w2v_model, topn=30, threshold=0.5, expected_count=200):
    ret_sentences = list()
    for cur_description in description_list:
        ret_sentences.extend(sentence_augmentation(cur_description, w2v_model, topn, threshold, expected_count))
    return ret_sentences


def generate_single_feature(words, w2v_model, feature_size=300):
    return np.mean([w2v_model[w] for w in nltk.word_tokenize(words) if w in w2v_model]
                   or [np.zeros(feature_size)], axis=0).reshape(1, -1)


def inference(svc, sentence, w2v_model):
    input_feature = generate_single_feature(sentence, w2v_model)
    class_idx = svc.predict(input_feature)[0]
    class_name = CHATBOT_CONFIG["INTENT_CLASS_NAMES"][class_idx]
    return class_idx, class_name


if __name__ == "__main__":
    sentence = "I want to have some Chinese food"
    # intent_classification_svc = utils.load_file_as_obj(CHATBOT_CONFIG.INTENT_CLASSIFIER_SVM_PATH)
    intent_classification_svc = utils.load_file_as_obj("../models/intent_classification_svc.pk")
    w2v_model = gensim.downloader.load('word2vec-google-news-300')
    print(inference(intent_classification_svc, sentence, w2v_model))
