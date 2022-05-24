# Copyright (c) SCYTHE, Inc. Use is subject to agreement.

import argparse
import shlex
import struct
import json
from os.path import basename
import base64


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

    epilog =  '  scythe.invoke_bof --filepath VFS:/users/BUILTIN/scythe/av_enum.o --funcname go '
    parser = ArgumentParser(prog="invoke_bof", description="Run Beacon Object Files inside the SCYTHE client",
                            epilog=epilog)
    parser.add_argument("--filepath", help="Path to file in VFS or on Disk. Ex: C:/Users/user1/av_enum.o or VFS:/users/BUILTIN/scythe/av_enum.o", required=True)
    parser.add_argument("--funcname", help="The function name to load at. Example 'go' ",required=True)
    parser.add_argument("--params",help="Additional arguments for the BOF file.",required=False)
    return parser


def usage(db, os):
    """Return the usage of this module as a string

    :return str: Usage string for this module
    """
    return create_parser(db, os).format_help()

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
        r = ["scythe", "att&ck", "att&ck-technique:T1620"]
    return r

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
        raise ValueError("Error: argument is missing.")
    else:
        argv = shlex.split(command_line, posix=False)
    args = parser.parse_args(argv)

    if not args.filepath:
        raise ValueError("Error: --filepath argument is missing")
    if not args.funcname:
        raise ValueError("Error: --funcname is missing")

    dict_to_send = {}
    file_bytes = None
    vfs = "0"
    if has_vfs_path(args.filepath):
        file_bytes = read_vfs_file(args.filepath[4:])
        vfs = "1"
        dict_to_send['filebytes'] = base64.b64encode(file_bytes).decode('utf-8',errors="ignore")
        dict_to_send['filesize'] = str(len(file_bytes))

    dict_to_send['filepath'] = args.filepath
    dict_to_send['filename'] = basename(args.filepath)
    dict_to_send['funcname'] = args.funcname
    dict_to_send['is_vfs'] = vfs
    if args.params:
        dict_to_send['params'] = args.params.strip('"').strip("'")
    
   
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
