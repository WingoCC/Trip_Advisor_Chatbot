import os
import json
import pickle


def save_obj_as_file(obj, filepath):
    """
    save a python object as a file
    :param obj: a python
    :param filepath: destination file path
    :return: None
    """
    with open(filepath, "wb") as fp:
        pickle.dump(obj, fp)


def load_file_as_obj(filepath):
    """
    load a python object from file
    :param filepath: source path of the python object
    :return: the object from the path
    """
    assert os.path.exists(filepath)
    with open(filepath, "rb") as fp:
        obj = pickle.load(fp)
    return obj


def convert_request_form_to_dict(request_form):
    chat_history = json.loads(dict(request_form)["msg"])
    return chat_history


def convert_request_form_to_list(request_form):
    chat_dict = json.loads(dict(request_form)["msg"])
    chat_list = list()
    for idx in range(len(chat_dict)):
        chat_list.append(chat_dict[str(idx)])
    return chat_list
