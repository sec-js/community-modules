# JXA Loader

Execute arbitrary JavaScript for Automation on a macOS target. 

## Credits and References

Author: SCYTHE / ProServe
Operating System(s): MacOS

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

To run a script already present on the target macOS. 
```bash
loader --load scythe.jxa_loader
scythe.jxa_loader --filename "Absolute Path to file"
```
or if you want to run a path from VFS. 
```bash
loader --load scythe.jxa_loader
scythe.jxa_loader --filename "VFS:/shared/<path>/<to>/<file>"
```

## FAQ:

No questions yet!
