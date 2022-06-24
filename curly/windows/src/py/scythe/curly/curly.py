import uuid
import json
import curl

g_client = None

CATEGORY_WORKER = 4
CURLY_MODULE_ID = uuid.UUID('f52ad330-f3fe-11ec-9bb2-290282c90ef4')

def init(client, **kwargs):
    """

    :param client:
    :param kwargs:
    :return:
    """
    global g_client
    g_client = client
    return True


def run(message,  **kwargs):
    """

    :param bytes message:
    :param kwargs:
    :return bytes or None: None if post will happen asynchronously
    """
    message_dict = json.loads(message.decode('utf-8'))
    return curl.main(**message_dict)
  


def getinfo():
    """

    :return:
    """
    return { "type": CATEGORY_WORKER, "version" : {"major": 1, "minor": 0}, "id" : CURLY_MODULE_ID}


def deinit(**kwargs):
    """

    :param kwargs:
    :return:
    """
    return True
