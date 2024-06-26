---
title: RE Course - 2.3 - Bits and Bytes
date: 2024-05-06 00:02:03
categories: [Course, RE]
tags: [RE Course]
---

Computers "understand" binary (Ex. 10110010). Binary is often talked about in chunks.

* **Bit is one binary digit**. So a bit can either be 0 or 1. 
* **Byte is 8 bits**.
* **Nibble is 4 bits**. Half a byte.
* **Word is 2 bytes**. This isn't always the case, but it usually is.
* **Double Word (DWORD) is 4 bytes**. Twice the size of a word.
* **Quad Word (QWORD) is 8 bytes**. Four times the size of a word.

Before we get into other data types, let's talk about signed vs unsigned. Signed numbers can be positive or negative. Unsigned is only positive numbers. You can remember this by thinking about how you would normally write positive and negative numbers. If you're using *both* positive and negative numbers, you'll want to distinguish the negative number with a sign ("-"). If you're using only positive numbers, then no sign is needed.

### Data Type Sizes

* **Char** - 1 byte (8 bits).
* **Int** - There are 16-bit, 32-bit, and 64-bit integers. For signed integers, one bit is used to specify whether the integer is positive or negative.
  * ***Signed* Int**
    * 16 bit is -32,768 to 32,767. 
    * 32 bit is -2,147,483,648 to 2,147,483,647. 
    * 64-bit is -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807.
  * ***Unsigned* Int** - Minimum is zero, maximum is twice that of a signed int (of the same size). For example: unsigned 32-bit int goes from 0 to 4,294,967,295. That is twice the signed int maximum of 2,147,483,647, however, its minimum value is 0.
* **Bool** - 1 byte. Interestingly, a bool only *needs* 1 bit because it's either 1 or 0 but it still takes up a full byte. This is because computers don't tend to work with individual bits due to alignment (talked about later). So instead, they work in chunks such as 1 byte, 2 bytes, 4 bytes, 8 bytes, and so on. This is done to keep everything clean and eliminate as much confusion as possible. 

For more data types go here: <https://www.tutorialspoint.com/cprogramming/c_data_types.htm>

## Significance

The least significant digit has the lowest value. The most significant digit has the highest value. The least significant digit in 124 is 4. The most significant is 1 (100).

[-> Next Lesson]({% post_url/RECourse/Chapter2/2024-05-06-RECourse_CH02_04_ProgrammingLanguages %})  
[<- Previous Lesson]({% post_url/RECourse/Chapter2/2024-05-06-RECourse_CH02_02_ASCII %})  


[Chapter Home]({% post_url/RECourse/Chapter2/2024-05-06-RECourse_CH02_00_BinaryBasics %})  
