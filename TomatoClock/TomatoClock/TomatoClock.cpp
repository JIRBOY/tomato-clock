// TomatoClock.cpp : Defines the class behaviors for the application.
//

#include "pch.h"
#include "TomatoClock.h"
#include "TomatoClockDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif

// CTomatoClockApp

BEGIN_MESSAGE_MAP(CTomatoClockApp, CWinApp)
END_MESSAGE_MAP()

// CTomatoClockApp construction

CTomatoClockApp::CTomatoClockApp()
{
}

// The one and only CTomatoClockApp object

CTomatoClockApp theApp;

// CTomatoClockApp initialization

BOOL CTomatoClockApp::InitInstance()
{
	CWinApp::InitInstance();

	CTomatoClockDlg dlg;
	m_pMainWnd = &dlg;
	INT_PTR nResponse = dlg.DoModal();

	return FALSE;
}