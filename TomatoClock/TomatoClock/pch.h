// pch.h: This is a precompiled header file.
// Files listed below are compiled only once, improving build performance for future builds.
// This also affects IntelliSense performance, including code completion and many code browsing features.
// However, files listed here are ALL re-compiled if any one of them is modified.
// Do not add files here that you will be modifying frequently.

#pragma once
#ifndef PCH_H
	#define PCH_H

	// 定义Windows版本
	#define _WIN32_WINNT 0x0601
	#define WINVER 0x0601

	// add headers that you want to pre-compile here
	#include "framework.h"

#endif //PCH_H