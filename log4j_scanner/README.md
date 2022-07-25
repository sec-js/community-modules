# Module Name

Test if a target or list of targets is vulnerable to the log4j attack.

## Credits and References

Author: scythe-proserve

Operating System(s): Windows

Additional credits and references:
* Porting the Log4J CVE PoC to SCYTHE: https://www.scythe.io/library/porting-the-log4j-cve-poc-to-scythe

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

```
Test a server for Log4j CVE-2021-44228E.

optional arguments:
  -h, --help            show this help message and exit
                        List of target servers to scan
  --payload PAYLOAD     Payload to try on list of servers. Default:
                        '${jndi:ldap://127.0.0.1:80/a}'
                        
scythe.log4j_scanner --targets http://localhost:8080 http://domain.com
```

## FAQ:

No questions yet!
