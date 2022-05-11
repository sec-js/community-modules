# f5_bigip

Check a list of servers for vulnerability to CVE-2022-1388

## Credits and References

Author: scythe-proserver

Operating System(s): 
    - MacOs
    - Windows

Additional credits and references:
* [CVE-2022-1388 PoC](https://github.com/ZephrFish/F5-CVE-2022-1388-Exploit)

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

```
usage: f5_bigip [-h] --targets [TARGETS [TARGETS ...]] [--payload PAYLOAD]

Test if a target server is vulnerable to CVE-2022-1388

optional arguments:
  -h, --help            show this help message and exit
  --targets [TARGETS [TARGETS ...]]
                        List of target servers to scan
  --payload PAYLOAD     Shell command to execute on target. CAUTION: If the
                        command is successful, it could have adverse affects
                        on a system! Default: id -a

scythe.f5_bigip --targets http://192.168.2.1 192.168.2.100:8080
```

## FAQ:

No questions yet!
