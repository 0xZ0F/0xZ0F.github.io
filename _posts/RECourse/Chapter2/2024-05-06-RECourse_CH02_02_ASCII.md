---
title: RE Course - 2.2 - ASCII
date: 2024-05-06 00:02:02
categories: [Course, RE]
tags: [RE Course]
---

Computers only understand numbers. So how are you seeing this text on your screen? It's simple, and it's a technique used constantly. It all depends on how it's interpreted. The letter "AAAA" (capitalization matters) is 0x41414141 or 1000001010000010100000101000001. 0x41414141 could be a memory address, or it could be a series of four A's. In this case "AAAA" is presented as four letters because the software has decided to present is that way. There are various other things that determine how data gets represented which we will talk about later. 

## How Does It Work?

In order for 0x41414141 to be "AAAA" we need to have some sort of standard. This standard is called ASCII. When you interpret something as ASCII you are assigning values to some other form. For example, in ASCII, 0x41 is "A", 0x42 is "B", etc. This standard allows any software using ASCII to see and present the same thing. There are, of course, many different standards that are used in different scenarios.

Here's a full ASCII table: <https://www.asciitable.com>

[-> Next Lesson]({% post_url/RECourse/Chapter2/2024-05-06-RECourse_CH02_03_BitsAndBytes %})  
[<- Previous Lesson]{% post_url/RECourse/Chapter2/2024-05-06-RECourse_CH02_01_NumberSystems %})  


[Chapter Home]({% post_url/RECourse/Chapter2/2024-05-06-RECourse_CH02_00_BinaryBasics %})  
