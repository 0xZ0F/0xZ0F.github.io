---
title: WinAFL EXE Fuzzing
date: 2025-03-01 12:00:00
categories: [Blog, Research]
tags: [Research, Programming, Fuzzing, C, CPP]
---

> The relevant code for this post can be found here: <https://github.com/0xZ0F/WinAFLEXEHarness>
{:.prompt-info}

There are a handful of great guides on performing fuzzing using WinAFL (and various other fuzzers). [The article written by Angelystor](https://medium.com/csg-govtech/starting-to-fuzz-with-winafl-ecc41661220c) has been particularly helpful, as well as [this one by 2ourc3](https://bushido-sec.com/index.php/2023/06/25/the-art-of-fuzzing-windows-binaries/) and [this one by Antonio Morales](https://github.com/antonio-morales/Fuzzing101/tree/main/Exercise%209). The major issue I was running into, however, is that existing guides for fuzzing focus on DLLs. While this is likely the most common case for most researchers, I regularly wished I could fuzz an executable.

The following writeup is how I created a harness capable of fuzzing an executable.

## Fuzzing DLLs

For the sake of brevity, I'm going to skip over creating a harness to fuzz DLLs. I would recommend reading the articles linked above for an overview.

## Attempt #1

When fuzzing a DLL it can be loaded with `LoadLibrary(...)`, an exported function can be found with `GetProcAddress(...)`, and the function can be called. If the function is not exported, some reversing is needed and an offset can be used. I was aware that you can also load executables with `LoadLibrary(...)` so that is what I did. I also knew, however, that the entry point (`DllMain(...)` for DLLs) would not be called. So, this is what I first tried.

The following loads the executable, resolves the entry point, and calls it.

> Throughout this post, code samples will have error handling removed. The usage of globals is due to reentrant fuzzing with WinAFL. For more information, see the linked articles at the top of this post.
{:.prompt-info}

```cpp
g_hExe = LoadLibraryA(EXE_PATH);

IMAGE_DOS_HEADER* dosHeader = (IMAGE_DOS_HEADER*)g_hExe;
IMAGE_NT_HEADERS* ntHeaders = (IMAGE_NT_HEADERS*)((BYTE*)g_hExe + dosHeader->e_lfanew);
DWORD entryPoint = ntHeaders->OptionalHeader.AddressOfEntryPoint;
((void(*)())((BYTE*)g_hExe + entryPoint))();
```

Running the above code results in an error.

```
Exception thrown at 0x00000000003F1516 in Harness.exe: 0xC0000005: Access violation executing location 0x00000000003F1516.
```

Thanks to my previous work with PE files ([some of which can be found here]({% post_url/blog/2024-05-07-ExtendingPESections %})) I immediately guessed as to what the issue was. It appears as though the function is failing to resolve an IAT address. Further debugging confirmed this idea.

## Fixing IAT Issues

Once again, my weeks spent getting familiar with PEs have paid off. I was fairly quickly able to get some old IAT code and modify it for this situation. The idea is simple. The executable we are loading needs to have its IAT setup to reflect the process it is loaded into, which is the harness.

The following code fixes up the target's IAT.

```cpp
bool FixImports(HMODULE hModule)
{
	PIMAGE_DOS_HEADER dosHeader = (PIMAGE_DOS_HEADER)hModule;
	PIMAGE_NT_HEADERS ntHeaders = (PIMAGE_NT_HEADERS)((BYTE*)hModule + dosHeader->e_lfanew);
	PIMAGE_IMPORT_DESCRIPTOR importDesc = (PIMAGE_IMPORT_DESCRIPTOR)((BYTE*)hModule +
		ntHeaders->OptionalHeader.DataDirectory[IMAGE_DIRECTORY_ENTRY_IMPORT].VirtualAddress);

	while(importDesc->Name)
	{
		const char* dllName = (const char*)((BYTE*)hModule + importDesc->Name);
		HMODULE hLib = GetModuleHandleA(dllName);
		if(!hLib)
		{
			printf("GetModuleHandleA() %s %lu\n", dllName, GetLastError());
			importDesc++;
			continue;
		}

		PIMAGE_THUNK_DATA thunk = (PIMAGE_THUNK_DATA)((BYTE*)hModule + importDesc->FirstThunk);
		PIMAGE_THUNK_DATA origThunk = (PIMAGE_THUNK_DATA)((BYTE*)hModule + importDesc->OriginalFirstThunk);

		while(origThunk->u1.AddressOfData)
		{
			if(origThunk->u1.Ordinal & IMAGE_ORDINAL_FLAG)
			{
				// Import by ordinal
				FARPROC func = GetProcAddress(hLib, (LPCSTR)(origThunk->u1.Ordinal & 0xFFFF));
				if(!func)
				{
					printf("Failed to resolve function by ordinal\n");
					return false;
				}
				thunk->u1.Function = (DWORD_PTR)func;
			}
			else
			{
				// Import by name
				PIMAGE_IMPORT_BY_NAME importByName = (PIMAGE_IMPORT_BY_NAME)((BYTE*)hModule + origThunk->u1.AddressOfData);
				FARPROC func = GetProcAddress(hLib, importByName->Name);
				if(!func)
				{
					printf("GetProcAddress() %s %lu\n", importByName->Name, GetLastError());
					return false;
				}

				DWORD dwOldProtect = 0;
				if(!VirtualProtect((void*)(&thunk->u1.Function), sizeof(thunk->u1.Function), PAGE_READWRITE, &dwOldProtect))
				{
					fprintf(stderr, "VirtualProtect() %lu\n", GetLastError());
					return false;
				}

				thunk->u1.Function = (DWORD_PTR)func;

				if(!VirtualProtect((void*)(&thunk->u1.Function), sizeof(thunk->u1.Function), dwOldProtect, &dwOldProtect))
				{
					fprintf(stderr, "VirtualProtect() %lu\n", GetLastError());
					return false;
				}
			}
			thunk++;
			origThunk++;
		}
		importDesc++;
	}

	return true;
}
```

Now, after I load the executable I need to pass its handle to this function which will fix the IAT. Also, this time around I won't be calling the entry point as I know it's not needed for my target (I wrote the target for testing purposes :P). The following is roughly the new code.

```cpp
using PrintHeadInfo_t = bool(*)(LPCSTR);

HMODULE g_hExe = NULL;
PrintHeadInfo_t g_fpFunc = NULL;

extern "C" __declspec(dllexport) __declspec(noinline) bool FuzzThis(char* szFilePath)
{
    if(NULL == g_fpFunc)
    {
        return false;
    }
    bool fRet = g_fpFunc(szFilePath);
    return fRet;
}

int main(...)
{
    g_hExe = LoadLibraryA(EXE_PATH);

    FixImports(g_hExe)

    g_fpFunc = (PrintHeadInfo_t)((uintptr_t)g_hExe + 0xD2C0);
    FuzzThis(NULL);
}
```

And now it... still doesn't work! I was getting `ERROR_MOD_NOT_FOUND` (126) from `GetModuleHandleA(...)` in `FixImports(...)`. It seems as though some DLLs in my target are not found through the traditional DLL load search paths. The fix was simple; manually call `LoadLibrary(...)` for DLLs as needed.

After that small fix, it worked! I was able to fuzz my target, an offset into an executable, using my harness.

I ended up using TinyInst instead of IntelPT as I was getting errors. Here is the final WinAFL command I used.

```powershell
.\afl-fuzz.exe -y `
    -i C:\Dev\Fuzzing\HeaderParse\afl_in `
    -o C:\Dev\Fuzzing\HeaderParse\Harness\afl_out `
    -t 10000 `
    -D C:\Dev\Fuzzing\dynamorio\build\bin64\ `
    -- `
    -iterations 500 `
    -instrument_module HeaderParse.exe `
    -target_module Harness.exe `
    -target_method FuzzThis `
    -nargs 2 `
    -persist `
    -loop `
    -- `
    "C:\Dev\Fuzzing\HeaderParse\x64\Debug\Harness.exe" "@@"
```

> TinyInst names some parameters differently, as is denoted below.
{:.prompt-warn}

* `-y` - Specifies the usage of TinyInst. WinAFL must also be compiled with `-DTINYINST=1`.
* `-i` - Input directory with test cases. I chose a couple of small DLLs, namely `dpapi.dll` and `wmi.dll`.
* `-o` - Output directory for fuzzer findings.
* `-t` - Timeout for each run.
* `-D` - Path to DynamoRIO.
* `--` - Instrumentation options begin.
* `-iterations` - Same as `-fuzz_iterations`. How many times to fuzz before restarting the target application.
* `-instrument_module` - Same as `-coverage_module`. Which module to instrument/measure.
* `-target_module` - Module in which the target (see next) resides.
* `-target_method` - Method within the target module which to use as the entry point for fuzzing.
* `-nargs` - Number of arguments the target function takes. I'm not sure why this is 2 and not 1, but all of the documentation is like this.
* `-persist` - Speeds up fuzzing by keeping the target alive once the target function returns. This isn't always viable, but in this case it is.
* `-loop` - Causes TinyInst to jump to the start of the target function after it returns.
* `--` - Target command line begins.
* `"C:\Dev\Fuzzing\HeaderParse\x64\Debug\Harness.exe"` - Harness.
* `@@` - Placeholder for WinAFL to fill in the file it's using as input.

More command line options can be found on the [WinAFL GitHub](https://github.com/googleprojectzero/winafl), as well as arguments for DynamoRIO, IntelPT, TinyInst, and more.

## Larger Target

Up until this point, I was fuzzing a small program I had written. However, I knew better than to assume if it worked for this target it would work for all. I decided to try to target a larger application, and I chose FileZilla. As it turns out, not much needed to be added. I ran into the `ERROR_MOD_NOT_FOUND` issue again but fixed it largely in the same way.

```cpp
SetDllDirectoryA("C:\\Program Files\\FileZilla FTP Client")

hTmp = LoadLibraryA("libfzclient-commonui-private-3-68-1.dll");
hTmp = LoadLibraryA("libfzclient-private-3-68-1.dll");
hTmp = LoadLibraryA("libfilezilla-46.dll");
hTmp = LoadLibraryA("wxbase32u_gcc_custom.dll");
hTmp = LoadLibraryA("wxmsw32u_aui_gcc_custom.dll");
hTmp = LoadLibraryA("wxmsw32u_core_gcc_custom.dll");
hTmp = LoadLibraryA("wxmsw32u_xrc_gcc_custom.dll");
hTmp = LoadLibraryA("libsqlite3-0.dll");
hTmp = LoadLibraryA("MPR.dll");
hTmp = LoadLibraryA("NETAPI32.dll");
hTmp = LoadLibraryA("ole32.dll");
hTmp = LoadLibraryA("POWRPROF.dll");
hTmp = LoadLibraryA("SHELL32.dll");
hTmp = LoadLibraryA("SHLWAPI.dll");
hTmp = LoadLibraryA("USER32.dll");
hTmp = LoadLibraryA("libgcc_s_seh-1.dll");
hTmp = LoadLibraryA("libstdc++-6.dll");

// Reset DLL load path.
SetDllDirectoryA(NULL)
```

I ran it, and it worked. I didn't think it would.

As I continue to fuzz I will likely run into a target that doesn't play nice. As I found in my [previous PE extravaganza]({% post_url/blog/2024-05-07-ExtendingPESections %}) there is likely to be an executable that needs further efforts to get working.

## Tips

Along the way, I found some useful information to make life a little bit easier. First off, I wanted it to be faster. As is documented by WinAFL, it will only use one core. It is, however, fairly easy to get it going on multiple. There is a full guide to parallel fuzzing [here on the WinAFL GitHub](https://github.com/googleprojectzero/winafl/blob/master/afl_docs/parallel_fuzzing.txt). The following is a brief introduction.

* WinAFL supports setting up a master and secondary fuzzer.
1. Set up the master fuzzer by passing `-M <NAME>` to `afl-fuzz.exe`.
2. For the second fuzzer, pass `-S <NAME>` to `afl-fuzz.exe`.
3. The names should be distinguishable such as fuzzer01 and fuzzer02.

Thats it! The output directories will now also be treated as sync directories.

Now I have a new issue, how can I easily check on the progress of these fuzzers? As it turns out WinAFL ships with `winafl-whatsup.py` which is used for this exact reason. All it needs is a sync dir.

> I initially ran the fuzzer without a master/secondary and as such there was no sync setup. Running `winafl-whatsup.py` presented me with no output, even with both a master and secondary running. To get it working I had to delete the output directory and allow the master/secondary fuzzers to set up a new output directory with sync. I will keep this in mind in the future, and try to always run with at least a master fuzzer.
{:.prompt-tip}

This next issue came up first, but was sort of fixed with `winafl-whatsup.py`. The problem was my target was printing to the console, making it difficult to track progress. My workaround was to silence `stdout`.

```cpp
FILE* fp = NULL;
if(freopen_s(&fp, "NUL", "w", stdout))
{
    fprintf(stderr, "freopen_s() %lu\n", GetLastError());
    return 5;
}
```

This sort of worked. There was still a good amount of output caused by TinyInst itself. In the end, `winafl-whatsup.py` is the best solution. However, this script is a one-shot and doesn't monitor. No worries, a little PowerShell fixed that issue as well.

```powershell
while (1) {python .\winafl-whatsup.py C:\Dev\Fuzzing\HeaderParse\afl_out\; sleep 1}
```

## Fin

Getting the fuzzing going only took a couple of days. But I must admit, it was quite a bumpy road and I don't like the solution even though it works. I will likely explore other fuzzers, but for now, I have something.

> The final harness, target, and commands can be found here: <https://github.com/0xZ0F/WinAFLEXEHarness>
{:.prompt-info}