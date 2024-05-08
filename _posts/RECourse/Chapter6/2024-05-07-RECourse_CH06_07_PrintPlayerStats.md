---
title: RE Course - 6.07 - Reversing PrintPlayerStats()
date: 2024-05-07 00:06:07
img_path: /assets/RECourse/Chapter6
categories: [Course, RE]
tags: [RE Course]
---

Before we use `InitializePlayer` in our own program, let's see what other information we can find about the class. To find more information, let's look at `PrintPlayerStats`. 

![](PrintPlayerStats/PrintPlayerStats.png)

This function is actually quite simple, all it does is print information about a `Player`. I want you to try to reverse this function on your own. I challenge you to figure out what the purpose is of each line of code.

I do want to let you know something before you start. There is some extra code after the final `printf()` call. If you do not follow the `JB` after the final `printf()` call, execution goes into some memory freeing code. Feel free to reverse this if you want, but you can ignore it.

Here is the code I'm talking about (in the red box):

![](PrintPlayerStats/FreeCode.png)

Anyways, good luck and have fun! We'll be reversing one more thing and then we will implement this `Player` class in our own code.

[-> Next Lesson]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_08_MysteryFunc %})  
[<- Previous Lesson]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_06_InitializePlayer %})  

[Chapter Home]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_00_DLL %})  
