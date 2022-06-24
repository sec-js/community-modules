import requests
import json

def main(**kwargs):
    url = kwargs.pop('url')
    method = kwargs.pop('method')
    try:
        response = requests.request(method,url,**kwargs)
        resp_dict = f"Status Code: {response.status_code}\nHeaders: {response.headers}\nBody:{response.text}\nJSON: {response.json}"
        return resp_dict.encode('utf-8')
    except Exception as e:
        return f"An Error Occurred: {e}".encode('utf-8')
    
    