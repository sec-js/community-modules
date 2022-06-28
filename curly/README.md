# curly

Perform curl web requests, data and file transfers from within the scythe implant.

## Credits and References

Author: scythe-proserve

Operating System(s): Windows

Additional credits and references:
* [Curl Icon by Icons8](https://icons8.com/)

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

```
Testing curly module's usage function:

usage: curly [-h] --url URL [-H HEADER] [-u USER] [-X METHOD] [-d DATA]

             [--cert CERT] [--verifyssl] [--proxies PROXIES]

             [--cookies COOKIES] [--timeout TIMEOUT] [--allowredirects]



Perform Web Requests from inside the scythe implant



optional arguments:

  -h, --help            show this help message and exit

  --url URL             Url to connect to

  -H HEADER, --header HEADER

                        Extra header to include in the request when sending

                        HTTP to a server. You may specify any number of extra

                        headers. Ex: "{'Accept': '*/*'}" or path to JSON

                        headers file in VFS

  -u USER, --user USER  <user:password> Specify the username and password to

                        use for server authentication

  -X METHOD, --method METHOD

                        Specifies a customer request method:

                        {GET,OPTIONS,HEAD,POST,PUT,PATCH,DELETE} Default: GET

  -d DATA, --data DATA  Sends the specified data in a POST request

  --cert CERT           String, or VFS path to ssl client cert file (.pem)

  --verifyssl, -k       Toggle switch to ignore or verify TLS certificate on

                        server. Default: False

  --proxies PROXIES     Dictionary mapping of protocol to the URL of the proxy

  --cookies COOKIES     Dictionary of key value cookies

  --timeout TIMEOUT     How many seconds to wait for the server to send data

                        before giving up

  --allowredirects      Enable/disable GET/OPTIONS/POSt/PUT/PATCH/DELETE/HEAD

                        redirections. Default: True



scythe.curly --url="http://scythe.io" -H={"Accept":"*/*"}
```

## FAQ:

No questions yet!
