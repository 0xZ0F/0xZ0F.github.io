---
title: RE Course - 6.02 - DLL Basics
date: 2024-05-07 00:06:02
img_path: /assets/RECourse/Chapter6
categories: [Course, RE]
tags: [RE Course]
---

You should already be familiar with these topics, however, just in case you're not, let's go over them.

## Dynamic Libraries

A **Dynamic Link Library** (DLL) is a library that is loaded separately from the program that uses it. The advantage of DLLs is that you can load one DLL into memory, and multiple programs can use it. This decreases the size of programs.

## Static Libraries

A **static library** is linked directly to/with the program that uses it. A library that is statically linked cannot be used by multiple programs at once. The library is part of the program it is used in. This makes the program bigger because of the extra code.

## Imports vs Exports

* **Import** - Something brought in from an external source. To use a function from a library you import that function from the library.
* **Export** - Something exposed to the outside so other sources can import it. You're able to access a function from a DLL because the DLL has exported that function. Because it's exported, your program can import it.

[-> Next Lesson]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_03_Exports %})  
[<- Previous Lesson]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_01_BeforeWeBegin %})  

[Chapter Home]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_00_DLL %})  
