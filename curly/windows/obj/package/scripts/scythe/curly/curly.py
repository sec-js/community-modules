# Copyright (c) SCYTHE, Inc. Use is subject to agreement.

import argparse
import shlex
import struct
import json

__fs = None

def has_vfs_path(source):
    return source.lower().startswith("vfs:/")

def read_vfs_file(path):
    global __fs
    if not __fs:
        from vfs import ScytheVFS
        __fs = ScytheVFS()
    return __fs.read_file(path)

# noinspection PyUnusedLocal
def create_parser(db, os="windows"):
    class ArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            raise ValueError(message)

    epilog =  '  scythe.curly --url="http://scythe.io" -H={"Accept":"*/*"}\n'
    parser = ArgumentParser(prog="curly", description="Perform Web Requests from inside the scythe implant",
                            epilog=epilog)
    parser.add_argument("--url", help="Url to connect to", required=True)
    parser.add_argument("-H","--header",help="Extra header to include in the request when sending HTTP to a server. You may specify any number of extra headers. Ex: \"{'Accept': '*/*'}\" or path to JSON headers file in VFS",required=False)
    parser.add_argument("-u","--user",help="<user:password> Specify the username and password to use for server authentication",required=False)
    parser.add_argument("-X","--method",help="Specifies a customer request method: {GET,OPTIONS,HEAD,POST,PUT,PATCH,DELETE} Default: GET",required=False,default="GET")
    parser.add_argument("-d","--data",help="Sends the specified data in a POST request",required=False)
    parser.add_argument('--cert',help="String, or VFS path to ssl client cert file (.pem)",required=False)
    parser.add_argument("--verifyssl",'-k',help="Toggle switch to ignore or verify TLS certificate on server. Default: False",required=False,default=False,action="store_false")
    parser.add_argument('--proxies',help="Dictionary mapping of protocol to the URL of the proxy",required=False)
    parser.add_argument('--cookies',help="Dictionary of key value cookies",required=False)
    parser.add_argument('--timeout',help="How many seconds to wait for the server to send data before giving up",required=False)
    parser.add_argument('--allowredirects',help="Enable/disable GET/OPTIONS/POSt/PUT/PATCH/DELETE/HEAD redirections. Default: True",required=False,default=True,action="store_false")
    return parser

# noinspection PyUnusedLocal
def succeeded(db, request,response):
    result = False
    if response and len(response) > 72:
        content = response[72:].tobytes().decode('utf-8')
        if not "Error: " in content:
            result = True
    return result

# noinspection PyUnusedLocal
def tags(reserved, request, response):
    """
    :param reserved: Reserved for future use
    :param request: Original request sent to device
    :param response: Reply from device for request
    :return: return a list of strings
    :rtype: list
    """
    r = []
    if len(request) > 0:
        r = ["scythe", "att&ck", "att&ck-technique:T1105"]
    return r

def usage(db, os):
    """Return the usage of this module as a string

    :return str: Usage string for this module
    """
    return create_parser(db, os).format_help()


# noinspection PyUnusedLocal
def create_message_body(db, command_line, campaign_name, endpoint_name):
    """Create a SCYTHE message body

    :param db: used only to retrieve operating system
    :param str command_line: command line string. If None is provided, command line will be received from sys.argv
    :param campaign_name: ignored
    :param endpoint_name: ignored
    :return str: String with message body
    """
    # You may call: db.get_setting_value("language")
    # This will return a language id string such as: "en-US"
    # You may use this result to present localized strings in the user interface.

    # You may call: db.get_campaign_operating_system_name(campaign_name)
    # This will return "windows" for Windows campaigns.
    parser = create_parser(db, db.get_campaign_operating_system_name(campaign_name))

    if not command_line:
        raise ValueError("Error: --url argument is missing.")
    else:
        argv = shlex.split(command_line, posix=False)

    args = parser.parse_args(argv)
    
    dict_to_send = {}
            
    # We need args.dest and either args.src or args.content
    if not args.url:    
        raise ValueError("Error: --url argument is missing.")
    
    dict_to_send['url'] = args.url.strip("'").strip('"')

    if args.method:
        dict_to_send['method'] = args.method       
    
    if args.header:
        headers = args.header
        if has_vfs_path(headers):
            dict_to_send['headers'] = read_vfs_file(headers[4:]).decode('utf-8')
        else:
            dict_to_send['headers'] = headers
    if args.user:
        user,password = args.user.split(":")
        dict_to_send['auth'] = (user,password)

    if args.data:
        data = args.data
        if has_vfs_path(data):
            dict_to_send['data'] = read_vfs_file(data[4:]).decode('utf-8')
        else:
            dict_to_send['data'] = data
    
    if args.cert:
        # decide whether we want to allow reads from implant disk
        cert = args.cert
        if has_vfs_path(cert):
            dict_to_send['cert'] = read_vfs_file(cert[4:]).decode('utf-8')
        else:
            dict_to_send['cert'] = args.cert

    dict_to_send['verify'] = args.verifyssl
    
    if args.proxies:
        dict_to_send['proxies'] = args.proxies
    
    if args.cert:
        dict_to_send['cert'] = args.cert
    
    if args.cookies:
        dict_to_send['cookies'] = args.cookies
    
    dict_to_send['allow_redirects'] = args.allowredirects

    return json.dumps(dict_to_send).encode('utf-8')


# noinspection PyUnusedLocal
def report(db, request, response, format_):
    """Generate a report for a request and response for this module

    :param db: ignored
    :param request: Request to report on
    :param response: Response to report on
    :param format_: ignored, always pre
    :return tuple(str, str, str): request report, response report, and format
    """
    # size of the response message is response[64:72]
    sz = struct.unpack("<Q", request[64:72].tobytes())[0]
    request_contents = request[72:72 + sz].tobytes().decode("utf-8")

    content = response[72:].tobytes().decode("utf-8")
    return "\"%s\"" % request_contents, content, "pre"


def main():
    pass


if __name__ == "__main__":
    main()
