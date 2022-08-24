/*++

 Copyright (c) SCYTHE, Inc. Use is subject to agreement.

 --*/
#include <windows.h>
#include "common.h"

DECLARE_DBGPRINT(NULL);
PSCYTHE_CLIENT g_pClient = NULL;


// {5d519870-2250-11ed-82f7-5929505ce15b}
static const GUID echoModuleId =
{ 0x5d519870, 0x2250, 0x11ed, { 0x82, 0xf7, 0x59, 0x29, 0x50, 0x5c, 0xe1, 0x5b}};


static const SCYTHE_MODULE_TYPE echoModuleType = CATEGORY_WORKER;


__checkReturn __success(return == SCYTHE_NOERROR) INT init(__in PSCYTHE_CLIENT pClient, __in_opt PVOID pvReserved)
{
    UNREFERENCED_PARAMETER(pvReserved);

    DBGPRINT("echo::init function called.\n");
    
    g_pClient = pClient;
        
    return SCYTHE_NOERROR;
}

__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T run(__in PSCYTHE_MESSAGE pMessage, __in_opt PVOID pvReserved)
{
    ERROR_T status = SCYTHE_NOERROR;

    const CHAR szDefaultMessage[] = "Nothing to echo.";
    UNREFERENCED_PARAMETER(pvReserved);
    
    DBGPRINT("echo::run function was called.");

    if (pMessage->MessageSize > 0)
    {
        status = g_pClient->PostToMessagingSubsystem(pMessage->MessageId, 0, 0,
                                                    CATEGORY_OUTPUT_COMMUNICATION,
                                                    &echoModuleId,
                                                    NULL,
                                                    pMessage->MessageSize,
                                                    pMessage->Message);
    }
    else
    {
        status = g_pClient->PostToMessagingSubsystem(pMessage->MessageId, 0, 0,
                                                     CATEGORY_OUTPUT_COMMUNICATION,
                                                     &echoModuleId,
                                                     NULL,
                                                     ARRAYSIZE(szDefaultMessage), (LPCBYTE)szDefaultMessage);
    }


    return SCYTHE_NOERROR;
}

__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T getinfo(__inout PSCYTHE_MODULE_INFORMATION pInformation)
{
    ERROR_T status = SCYTHE_ERROR_INVALID_PARAMETER;

    DBGPRINT("echo::getinfo function was called.");
    if (NULL != pInformation)
    {
        if (pInformation->cbSize >= sizeof(SCYTHE_MODULE_INFORMATION))
        {
            pInformation->ModuleVersion.wMajor = 1;
            pInformation->ModuleVersion.wMinor = 0;
            pInformation->ModuleType = echoModuleType;
            memcpy(&(pInformation->ModuleId), &echoModuleId, sizeof(GUID));
            status = SCYTHE_NOERROR;
        }
    }

    return status;
}

// Required function: deinit
__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T deinit(__in PVOID pvReserved)
{
    UNREFERENCED_PARAMETER(pvReserved);

    DBGPRINT("echo::deinit function was called.");
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
        DBGPRINT("echo: DLL_PROCESS_ATTACH");

        break;
    case DLL_PROCESS_DETACH:
        DBGPRINT("echo: DLL_PROCESS_DETACH");
        break;
    default:
        break;
    }

    return TRUE;
}
