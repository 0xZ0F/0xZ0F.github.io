---
title: RE Course - 8.00 - Generic Table
date: 2024-05-07 00:08:00
img_path: /assets/RECourse/Chapter8
categories: [Course, RE]
tags: [RE Course]
---

> Work in Progress
{.prompt-danger}

This chapter is going to cover reversing parts of a real DLL. The DLL we're going to look at is NTDLL.dll. It's quite a big DLL so we won't reverse the whole thing. We'll focus on the Generic Table (GT) functions. I'm choosing the generic table functions because they are semi-documented (so we can check our work), there are multiple functions, and they cover a variety of concepts.

> The generic table data structure is publicly documented, however, for the purpose of learning you should avoid the documentation.
{:.prompt-warning}

{% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_00_GenericTable %}
{% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_01_InitializeTable %}
{% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_02_NumberGenericTableElements %}
{% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_03_IsGenericTableEmpty %}
{% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_04_GetElement %}

### [Chapter 8 - Generic Table]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_00_GenericTable %})
* [8.00 - Generic Table.md]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_00_GenericTable %})
* [8.01 - InitializeTable]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_01_InitializeTable %})
* [8.02 - NumberGenericTableElements.md]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_02_NumberGenericTableElements %})
* [8.03 - IsGenericTableEmpty.md]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_03_IsGenericTableEmpty %})
* [8.04 - GetElement.md]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_04_GetElement %})

[-> Next Lesson]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_01_InitializeTable %})
[<- Previous Lesson]({% post_url/RECourse/Chapter7/2024-05-07-RECourse_CH07_00_Windows %}) - WIP  

[Chapter Home]({% post_url/RECourse/Chapter8/2024-05-07-RECourse_CH08_00_GenericTable %})

##### Sources:

Eldad Eilam, and Elliot J Chikofsky. Reversing : Secrets of Reverse Engineering. Indianapolis, In, Wiley, 2005.
