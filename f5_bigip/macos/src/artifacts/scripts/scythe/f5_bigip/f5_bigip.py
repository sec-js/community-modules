# Copyright (c) SCYTHE, Inc. Use is subject to agreement.

import argparse
import shlex
import struct
import json

# noinspection PyUnusedLocal
def create_parser(db, os="windows"):
    class ArgumentParser(argparse.ArgumentParser):
        def error(self, message):
            raise ValueError(message)

    epilog =  '  scythe.f5_bigip --targets http://192.168.2.1 192.168.2.100:8080\n'
    parser = ArgumentParser(prog="f5_bigip", description="Test if a target server is vulnerable to CVE-2022-1388",
                            epilog=epilog)
    parser.add_argument("--targets", help="List of target servers to scan", required=True, nargs="*",default=[])
    parser.add_argument("--payload",help="Shell command to execute on target. CAUTION: If the command is successful, it could have adverse affects on a system! Default: id -a",required=False, default="id -a")
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
        content = response[72:].tobytes().decode("utf-8")
        if not "Error:" in content:
            result = True
    return result
    
# noinspection PyUnusedLocal
def tags(db, request, response):
    """
    :param reserved: Reserved for future use
    :param request: Original request sent to device
    :param response: Reply from device for request
    :return: return a list of strings
    :rtype: list
    """
    r = ["scythe", "att&ck", "att&ck-technique:T1210"]
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

 
    argv = shlex.split(command_line, posix=False)
    args = parser.parse_args(argv)        
            
    # We need args.dest and either args.src or args.content
    if not args.targets:    
        raise ValueError("Error: --targets argument is missing.")
    if not args.payload:    
        raise ValueError("Error: --payload argument is missing.")
    
    dict_to_send = {
        'targets': args.targets,
        'payload' : args.payload
    }

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
    return "%s" % request_contents, content, "pre"

def main():
    pass


if __name__ == "__main__":
    main()
