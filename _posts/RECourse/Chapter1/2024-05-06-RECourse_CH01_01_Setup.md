---
title: RE Course - 1.1 - Setup
date: 2024-05-06 00:01:01
categories: [Course, RE]
tags: [RE Course]
---

This course will focus on 64-bit Windows, but we will talk a little about 32-bit. Note: In this course x32 and x86 both refer to 32-bit.

## Operating System

You will need a 64-bit Windows OS. You can use a virtual machine (VM) if you want. It's typically best to use a VM for security reasons, but you don't need to worry about that until the malware chapter. If you plan on making reverse engineering part of your life then you will probably want to set up a reversing VM anyways. Having a VM will allow you to better isolate the software you are reversing. This can be extremely helpful if you are analyzing a program's network traffic, disk usage, registry modifications, etc. Also, if you mess anything up you can revert the VM. Again, you don't need one for this course but in the future, I would recommend you get one.

## Reversing Tools:

Most of the software can be replaced with anything you like. The software I will be using is listed (all of it's free):  

#### Required:

* [**Microsoft Visual C++ Redistributable**](https://aka.ms/vs/16/release/vc_redist.x64.exe) will allow you to run the programs and DLLs I provide. Ideally you should install Visual Studio with the "Desktop development with C++" workload.
* [**x64dbg**](https://x64dbg.com/) - Despite the name, this is not limited to x64.
* [**ILSpy**](https://github.com/icsharpcode/ILSpy) or [**dnSpy**](https://github.com/0xd4d/dnSpy) - Used for .NET analysis.

#### Optional:

The software listed here won't be used in the course, but you might want it in the future.

* **HIGHLY RECOMMENDED:**
  * [**IDA Free**](https://hex-rays.com/ida-free/)
  * [**Ghidra**](https://ghidra-sre.org/) - Needs JDK.
  * [**Visual Studio**](https://visualstudio.microsoft.com/) with "Desktop development with C++" installed. You will also need a Windows SDK but that should be selected automatically.
* [**HxD**](https://mh-nexus.de/en/hxd/)
* [**Sysinternals Suite**](https://docs.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite) - Various tools to analyze Windows.
* [**Dependency Walker**](https://www.dependencywalker.com/) - If you want a GUI alternative to _SysInternal's_ "dumpbin".

## Target Software:

All of the target software that I wrote and is used in this course can be found in [FilesNeeded]({% link {{site.course_links.re.filesneeded}} %}).

> The files may change over time as I update the course.