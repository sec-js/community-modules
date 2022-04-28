# ProcList

List Processes running on an implant. Filter by User, PID, and PPID for Linux and MacOS. 

## Credits and References

Author: SCYTHE/ProServe
Operating System(s): Linux, MacOS

Additional credits and references:

- [simpletable](github.com/alexeyco/simpletable)
- [gopsutil](github.com/shirou/gopsutil/process)
- [Process Icon by Icons8](https://icons8.com)

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

```
usage: proclist [-h] [--ppid PPID] [--pid PID] [--user USER] [--format FORMAT]
Show running processes on an implant.
optional arguments:
  -h, --help       show this help message and exit
  --ppid PPID      PPID to filter by
  --pid PID        Return |Name|PID|PPID|Mem|Nice|Priority|CPU|User|Cwd|Env|Cm
                   dline|CreateTime|Exe| for a given process
  --user USER      User to filter results by
  --format FORMAT  Return data as JSON or as ASCII table {'table','json'}
scythe.proclist"
```

## FAQ:

No questions yet!
