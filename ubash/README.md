# Ubash

Run unmanaged `bash` and `shell` scripts from memory without invoking `bash -c`. 

## Credits and References

Author: SCYTHE / ProServe
Operating System(s): Linux

## Installation

Please reference our module [installation guide](https://github.com/scythe-io/community-modules/wiki) on the wiki.

##  Manual

```bash
loader --load scythe.ubash
scythe.ubash --filename "VFS:/users/BUILTIN/scythe/enum.sh
# You can also run inline shell commands;
scythe.ubash --filename "#!/bin/bash\n whoami\n ip a\n cat /etc/passwd\n w"
```
All scripts must include `#!/bin/bash or #!/bin/sh` at the top of the file. 

**NOTE: Scripts which require user interaction or parameters are not supported right now, they must be hardcoded into the script before running on target. **

## FAQ:

No questions yet!
