#include "CvGameCoreDLL.h"

#include "CvGameCoreDLLUndefNew.h"

#include <new>

#include "CvGlobals.h"
#include "FProfiler.h"
#include "CvDLLInterfaceIFaceBase.h"

//
// operator global new and delete override for gamecore DLL
//
void *__cdecl operator new(size_t size)
{
	if (gDLL)
	{
		return gDLL->newMem(size, __FILE__, __LINE__);
	}
	return malloc(size);
}

void __cdecl operator delete (void *p)
{
	if (gDLL)
	{
		gDLL->delMem(p, __FILE__, __LINE__);
	}
	else
	{
		free(p);
	}
}

void* operator new[](size_t size)
{
	if (gDLL)
		return gDLL->newMemArray(size, __FILE__, __LINE__);
	return malloc(size);
}

void operator delete[](void* pvMem)
{
	if (gDLL)
	{
		gDLL->delMemArray(pvMem, __FILE__, __LINE__);
	}
	else
	{
		free(pvMem);
	}
}

void *__cdecl operator new(size_t size, char* pcFile, int iLine)
{
	return gDLL->newMem(size, pcFile, iLine);
}

void *__cdecl operator new[](size_t size, char* pcFile, int iLine)
{
	return gDLL->newMem(size, pcFile, iLine);
}

void __cdecl operator delete(void* pvMem, char* pcFile, int iLine)
{
	gDLL->delMem(pvMem, pcFile, iLine);
}

void __cdecl operator delete[](void* pvMem, char* pcFile, int iLine)
{
	gDLL->delMem(pvMem, pcFile, iLine);
}


void* reallocMem(void* a, unsigned int uiBytes, const char* pcFile, int iLine)
{
	return gDLL->reallocMem(a, uiBytes, pcFile, iLine);
}

unsigned int memSize(void* a)
{
	return gDLL->memSize(a);
}

void StartXMLUpdate();

// WTP: crash log. When the game dies with an access violation (e.g. in MSVCR71.dll) Windows tells only the module and the offset where it died, not who
// called it. This filter writes the registers and the call chain (return addresses as module + offset; the offsets are looked up with the PDB file
// of exactly this DLL) to CrashLog.txt next to CvGameCoreDLL.dll, and then hands the crash on to the handler that was there before (the game's own).
// It uses only plain Windows calls and buffers on the stack (the heap may be what is broken).
static LPTOP_LEVEL_EXCEPTION_FILTER g_pWtpPrevCrashFilter = NULL;
static char g_acWtpCrashLogPath[MAX_PATH] = "";
static volatile LONG g_iWtpCrashBusy = 0;

static void wtpCrashWrite(HANDLE hFile, const char* pcText)
{
	DWORD uiWritten = 0;
	WriteFile(hFile, pcText, (DWORD)lstrlenA(pcText), &uiWritten, NULL);
}

// one address of the code as "module+offset" (module: the name of the file the address lies in)
static void wtpCrashWriteAddress(HANDLE hFile, DWORD uiAddress)
{
	char acLine[MAX_PATH + 80];
	MEMORY_BASIC_INFORMATION kInfo;
	if (VirtualQuery((LPCVOID)uiAddress, &kInfo, sizeof(kInfo)) != 0 && kInfo.Type == MEM_IMAGE && kInfo.AllocationBase != NULL)
	{
		char acModule[MAX_PATH];
		acModule[0] = 0;
		GetModuleFileNameA((HMODULE)kInfo.AllocationBase, acModule, MAX_PATH);
		const char* pcName = acModule;
		for (const char* pc = acModule; *pc != 0; ++pc)
		{
			if (*pc == '\\' || *pc == '/')
			{
				pcName = pc + 1;
			}
		}
		wsprintfA(acLine, "  %08X  %s+0x%X\r\n", uiAddress, pcName, uiAddress - (DWORD)kInfo.AllocationBase);
	}
	else
	{
		wsprintfA(acLine, "  %08X\r\n", uiAddress);
	}
	wtpCrashWrite(hFile, acLine);
}

static bool wtpCrashIsCode(DWORD uiAddress)
{
	MEMORY_BASIC_INFORMATION kInfo;
	if (VirtualQuery((LPCVOID)uiAddress, &kInfo, sizeof(kInfo)) == 0 || kInfo.Type != MEM_IMAGE)
	{
		return false;
	}
	return (kInfo.Protect & (PAGE_EXECUTE | PAGE_EXECUTE_READ | PAGE_EXECUTE_READWRITE | PAGE_EXECUTE_WRITECOPY)) != 0;
}

static LONG WINAPI wtpCrashFilter(EXCEPTION_POINTERS* pException)
{
	if (InterlockedExchange((LONG*)&g_iWtpCrashBusy, 1) == 0 && g_acWtpCrashLogPath[0] != 0 && pException != NULL && pException->ExceptionRecord != NULL && pException->ContextRecord != NULL)
	{
		HANDLE hFile = CreateFileA(g_acWtpCrashLogPath, GENERIC_WRITE, FILE_SHARE_READ, NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
		if (hFile != INVALID_HANDLE_VALUE)
		{
			char acLine[200];
			SetFilePointer(hFile, 0, NULL, FILE_END);
			SYSTEMTIME kTime;
			GetLocalTime(&kTime);
			wsprintfA(acLine, "==== %04d-%02d-%02d %02d:%02d:%02d  CvGameCoreDLL built %s %s\r\n", kTime.wYear, kTime.wMonth, kTime.wDay, kTime.wHour, kTime.wMinute, kTime.wSecond, __DATE__, __TIME__);
			wtpCrashWrite(hFile, acLine);
			const EXCEPTION_RECORD* pRecord = pException->ExceptionRecord;
			wsprintfA(acLine, "exception code %08X at %08X", pRecord->ExceptionCode, (DWORD)pRecord->ExceptionAddress);
			wtpCrashWrite(hFile, acLine);
			if (pRecord->ExceptionCode == EXCEPTION_ACCESS_VIOLATION && pRecord->NumberParameters >= 2)
			{
				wsprintfA(acLine, " (%s address %08X)", pRecord->ExceptionInformation[0] == 0 ? "read of" : (pRecord->ExceptionInformation[0] == 1 ? "write to" : "execution of"), (DWORD)pRecord->ExceptionInformation[1]);
				wtpCrashWrite(hFile, acLine);
			}
			wtpCrashWrite(hFile, "\r\nat:\r\n");
			wtpCrashWriteAddress(hFile, (DWORD)pRecord->ExceptionAddress);
			const CONTEXT* pContext = pException->ContextRecord;
#ifdef _X86_
			wsprintfA(acLine, "eax %08X ebx %08X ecx %08X edx %08X esi %08X edi %08X ebp %08X esp %08X\r\n", pContext->Eax, pContext->Ebx, pContext->Ecx, pContext->Edx, pContext->Esi, pContext->Edi, pContext->Ebp, pContext->Esp);
			wtpCrashWrite(hFile, acLine);
			// the return addresses on the stack (the code is built without frame pointers, so the stack is searched for values that lie in
			// executable code of a module; some of them are leftovers, the first ones are the calls that led here)
			wtpCrashWrite(hFile, "call chain (return addresses found on the stack):\r\n");
			const DWORD* puiStack = (const DWORD*)pContext->Esp;
			int iFound = 0;
			for (int i = 0; i < 2048 && iFound < 80; ++i)
			{
				if (IsBadReadPtr(puiStack + i, sizeof(DWORD)))
				{
					break;
				}
				const DWORD uiValue = puiStack[i];
				// (a return address is behind a call instruction: the value must lie in code and the bytes before it must be a call: E8 with a target that
				// lies in code, FF 15 (call of a pointer), or FF with the modrm byte of a call (register, 2 bytes); a text of the stack, e.g. the letters of
				// a path, is not taken for an address by chance this way)
				if (uiValue > 0x10000 && wtpCrashIsCode(uiValue) && !IsBadReadPtr((const void*)(uiValue - 6), 6))
				{
					const unsigned char* pucCode = (const unsigned char*)uiValue;
					bool bCall = false;
					if (pucCode[-5] == 0xE8)
					{
						bCall = wtpCrashIsCode(uiValue + *(const int*)(pucCode - 4));
					}
					else if (pucCode[-6] == 0xFF && pucCode[-5] == 0x15)
					{
						bCall = true;
					}
					else if (pucCode[-2] == 0xFF && (pucCode[-1] & 0x38) == 0x10 && (pucCode[-1] & 0xC0) == 0xC0)
					{
						bCall = true;
					}
					if (bCall)
					{
						wsprintfA(acLine, "[esp+%03X]", i * 4);
						wtpCrashWrite(hFile, acLine);
						wtpCrashWriteAddress(hFile, uiValue);
						++iFound;
					}
				}
			}
#endif
			wtpCrashWrite(hFile, "\r\n");
			CloseHandle(hFile);
		}
	}
	if (g_pWtpPrevCrashFilter != NULL)
	{
		return g_pWtpPrevCrashFilter(pException);
	}
	return EXCEPTION_CONTINUE_SEARCH;
}

static void wtpInstallCrashLog(HANDLE hModule)
{
	DWORD uiLength = GetModuleFileNameA((HMODULE)hModule, g_acWtpCrashLogPath, MAX_PATH - 20);
	if (uiLength == 0 || uiLength >= MAX_PATH - 20)
	{
		g_acWtpCrashLogPath[0] = 0;
		return;
	}
	// (the name of the DLL is replaced by the name of the log)
	char* pcName = g_acWtpCrashLogPath;
	for (char* pc = g_acWtpCrashLogPath; *pc != 0; ++pc)
	{
		if (*pc == '\\' || *pc == '/')
		{
			pcName = pc + 1;
		}
	}
	lstrcpyA(pcName, "CrashLog.txt");
	g_pWtpPrevCrashFilter = SetUnhandledExceptionFilter(wtpCrashFilter);
}

// WTP: test of the crash log. If a file CrashLogTest.txt lies next to CvGameCoreDLL.dll the game dies once on purpose (the file is deleted first, so
// it happens only once) and CrashLog.txt has to appear. Called once from CvGame::update.
void wtpCrashLogSelfTest()
{
	char acTestFile[MAX_PATH];
	lstrcpyA(acTestFile, g_acWtpCrashLogPath);
	char* pcName = acTestFile;
	for (char* pc = acTestFile; *pc != 0; ++pc)
	{
		if (*pc == '\\' || *pc == '/')
		{
			pcName = pc + 1;
		}
	}
	if (g_acWtpCrashLogPath[0] == 0 || lstrlenA(acTestFile) + 8 >= MAX_PATH)
	{
		return;
	}
	lstrcpyA(pcName, "CrashLogTest.txt");
	if (GetFileAttributesA(acTestFile) != INVALID_FILE_ATTRIBUTES)
	{
		DeleteFileA(acTestFile);
		*(volatile int*)0 = 1; // access violation on purpose
	}
}

BOOL APIENTRY DllMain(HANDLE hModule,
					  DWORD  ul_reason_for_call,
					  LPVOID lpReserved)
{
	switch( ul_reason_for_call ) {
	case DLL_PROCESS_ATTACH:
		{
		// The DLL is being loaded into the virtual address space of the current process as a result of the process starting up
		OutputDebugString("DLL_PROCESS_ATTACH\n");
		wtpInstallCrashLog(hModule); // WTP: crash log (CrashLog.txt next to the DLL)

		// set timer precision
		MMRESULT iTimeSet = timeBeginPeriod(1);		// set timeGetTime and sleep resolution to 1 ms, otherwise it's 10-16ms
		FAssertMsg(iTimeSet==TIMERR_NOERROR, "failed setting timer resolution to 1 ms");
		StartXMLUpdate();
		}
		break;
	case DLL_THREAD_ATTACH:
		// OutputDebugString("DLL_THREAD_ATTACH\n");
		break;
	case DLL_THREAD_DETACH:
		// OutputDebugString("DLL_THREAD_DETACH\n");
		break;
	case DLL_PROCESS_DETACH:
		OutputDebugString("DLL_PROCESS_DETACH\n");
		timeEndPeriod(1);
		GC.setDLLIFace(NULL);
		break;
	}

	return TRUE;	// success
}

std::string GetDLLPath(bool bLoadDLLPath)
{
	char buffer[MAX_PATH];
	GetModuleFileNameA(bLoadDLLPath ? GetModuleHandle("CvGameCoreDLL.dll") : NULL, buffer, MAX_PATH);
	std::string::size_type pos = std::string(buffer).find_last_of("\\/");

	return std::string(buffer).substr(0, pos);
}
