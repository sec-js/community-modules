import uuid
import bigip
import json
import sys
g_client = None

CATEGORY_WORKER = 4
F5_BIGIP_MODULE_ID = uuid.UUID('4c422760-cfef-11ec-84d4-43a9e99d43e1')

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
    targets = message_dict['targets']
    cmd = message_dict['payload']
    result = bigip.main(targets=targets, payload=cmd)
    

    message = result.encode('utf-8')

    return message



def getinfo():
    """

    :return:
    """
    return { "type": CATEGORY_WORKER, "version" : {"major": 1, "minor": 0}, "id" : F5_BIGIP_MODULE_ID}


def deinit(**kwargs):
    """

    :param kwargs:
    :return:
    """
    return True
