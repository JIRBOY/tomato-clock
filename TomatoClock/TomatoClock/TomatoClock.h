// TomatoClock.h : main header file for the TomatoClock application
//

#pragma once

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

// CTomatoClockApp:
// See TomatoClock.cpp for the implementation of this class
//

class CTomatoClockApp : public CWinApp
{
public:
	CTomatoClockApp();

// Overrides
public:
	virtual BOOL InitInstance();

// Implementation
	DECLARE_MESSAGE_MAP()
};

extern CTomatoClockApp theApp;