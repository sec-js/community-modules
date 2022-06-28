/*++

 Copyright (c) SCYTHE, Inc. Use is subject to agreement.

 --*/
#pragma warning(disable:4996)
#include <windows.h>
#include <WinBase.h>
#include <string.h>
#include <stdio.h>
#include <direct.h>

#include "common.h"
#include "asprintf.h"
#include "nxjson.h"


DECLARE_DBGPRINT(NULL);
PSCYTHE_CLIENT g_pClient = NULL;


// {49a111b0-ed72-11ec-8bfb-6135dc75d234}
static const GUID cdModuleId =
{ 0x49a111b0, 0xed72, 0x11ec, { 0x8b, 0xfb, 0x61, 0x35, 0xdc, 0x75, 0xd2, 0x34}};


static const SCYTHE_MODULE_TYPE cdModuleType = CATEGORY_WORKER;

struct params {
    const char* dir;
};


__checkReturn __success(return == SCYTHE_NOERROR) INT init(__in PSCYTHE_CLIENT pClient, __in_opt PVOID pvReserved)
{
    UNREFERENCED_PARAMETER(pvReserved);

    DBGPRINT("cd::init function called.\n");
    
    g_pClient = pClient;
        
    return SCYTHE_NOERROR;
}

__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T run(__in PSCYTHE_MESSAGE pMessage, __in_opt PVOID pvReserved)
{
    ERROR_T status = SCYTHE_NOERROR;

    UNREFERENCED_PARAMETER(pvReserved);
    
    DBGPRINT("cd::run function was called.");

    struct params p;
    char* resp = "";
    LPCSTR* path = (char*) pMessage->Message;
    

    TCHAR NPath[MAX_PATH];
    //GetCurrentDirectory(MAX_PATH, NPath);
    //perror(NPath);
    // Change Directory
    
    if (!SetCurrentDirectory((path))) {
        asprintf(&resp, "SetCurrentDirectory failed: (%d)",GetLastError());
    }//end
    
    _chdir(path);
    //system("dir");
    char* new_cwd = _getcwd(NULL, MAX_PATH);


    GetCurrentDirectory(MAX_PATH, NPath);
    //perror(NPath);
    asprintf(&resp, "New Directory %s\n", new_cwd);

    status = g_pClient->PostToMessagingSubsystem(pMessage->MessageId, 0, 0,
         CATEGORY_OUTPUT_COMMUNICATION,
         &cdModuleId,
         NULL,
         strlen(resp),(LPCBYTE)resp);
    
    return status;
}

__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T getinfo(__inout PSCYTHE_MODULE_INFORMATION pInformation)
{
    ERROR_T status = SCYTHE_ERROR_INVALID_PARAMETER;

    DBGPRINT("cd::getinfo function was called.");
    if (NULL != pInformation)
    {
        if (pInformation->cbSize >= sizeof(SCYTHE_MODULE_INFORMATION))
        {
            pInformation->ModuleVersion.wMajor = 1;
            pInformation->ModuleVersion.wMinor = 0;
            pInformation->ModuleType = cdModuleType;
            memcpy(&(pInformation->ModuleId), &cdModuleId, sizeof(GUID));
            status = SCYTHE_NOERROR;
        }
    }

    return status;
}

// Required function: deinit
__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T deinit(__in PVOID pvReserved)
{
    UNREFERENCED_PARAMETER(pvReserved);

    DBGPRINT("cd::deinit function was called.");
    return SCYTHE_NOERROR;
}


BOOL WINAPI DllMain(__in HINSTANCE hinstDLL, __in DWORD fdwReason, __in LPVOID lpvReserved)
{
    UNREFERENCED_PARAMETER(lpvReserved);
    UNREFERENCED_PARAMETER(hinstDLL);

    switch (fdwReason)
    {
    case DLL_PROCESS_ATTACH:
        INITIALIZE_DBGPRINT(NULL);
        DBGPRINT("cd: DLL_PROCESS_ATTACH");

        break;
    case DLL_PROCESS_DETACH:
        DBGPRINT("cd: DLL_PROCESS_DETACH");
        break;
    default:
        break;
    }

    return TRUE;
}
