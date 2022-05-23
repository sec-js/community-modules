# Invoke-BOF

Run Beacon Object Files from within a SCYTHE Implant. 

## Credits and References

Author: scythe-proserve

Operating System(s): Windows

Additional credits and references:
* [NXJSON](https://github.com/thestr4ng3r/nxjson)
- [Futurama Bender](https://icons8.com/icon/SB0MdkfS1QQz/futurama-bender)
- [COFF Loader](https://github.com/trustedsec/COFFLoader). Huge thanks to [@kev169](https://github.com/kev169) for making an awesome extensible loader!

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

```
usage: invoke_bof [-h] --filepath FILEPATH --funcname FUNCNAME
                  [--params PARAMS]
Run Beacon Object Files inside the SCYTHE client
optional arguments:
  -h, --help           show this help message and exit
  --filepath FILEPATH  Path to file in VFS or on Disk. Ex:
                       C:/Users/user1/av_enum.o or
                       VFS:/users/BUILTIN/scythe/av_enum.o
  --funcname FUNCNAME  The function name to load at. Example 'go'
  --params PARAMS      Additional arguments for the BOF file.
scythe.invoke_bof --filepath VFS:/users/BUILTIN/scythe/av_enum.o --funcname go
```

## FAQ:

No questions yet!