---
title: RE Course - 6.09 - Implementing the Player Class
date: 2024-05-07 00:06:09
img_path: /assets/RECourse/Chapter6
categories: [Course, RE]
tags: [RE Course]
---

> This part is optional but it gives our efforts purpose. And it's fun.
{:.prompt-tip}

Now that we've reversed the `Player` class, let's write our own program that makes a `Player` class and uses the functions related to the class.

![](Player/FinalCode.png)

The player's name doesn't have to be a `std::string`, it can probably be a `const* char` as well.

# Copy/Paste Code

```cpp
#include <iostream>
#include <Windows.h>

class Player {
public:
	int score;
	float health;
	std::string name;
};

//void __cdecl InitializePlayer(class Player * __ptr64)
typedef void(WINAPI* IInitializePlayer)(Player*); // ?InitializePlayer@@YAXPEAVPlayer@@@Z
//void PrintPlayerStats(Player);
typedef void(WINAPI* IPrintPlayerStats)(Player); // PrintPlayerStats

int main()
{
	Player player;
	HMODULE dll = LoadLibraryA("DLL.DLL"); //Load our DLL.
	if (dll != NULL)
	{
		//Initialize Player
		IInitializePlayer InitializePlayer = (IInitializePlayer)GetProcAddress(dll, "?InitializePlayer@@YAXPEAVPlayer@@@Z");
		if (InitializePlayer != NULL) {
			InitializePlayer(&player);
		}
		else { printf("Can't load the function."); }

		//PrintPlayerStats
		IPrintPlayerStats PrintPlayerStats = (IPrintPlayerStats)GetProcAddress(dll, "PrintPlayerStats");
		if (InitializePlayer != NULL) {
			PrintPlayerStats(player);
		}
		else { printf("Can't load the function."); }
		
	}
}
```

[-> Next Lesson]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_10_FinalNotes %})  
[<- Previous Lesson]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_08_MysteryFunc %})  

[Chapter Home]({% post_url/RECourse/Chapter6/2024-05-07-RECourse_CH06_00_DLL %})  
