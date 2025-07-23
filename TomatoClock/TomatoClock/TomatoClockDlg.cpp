// TomatoClockDlg.cpp : implementation file

#include "pch.h"
#include "TomatoClock.h"
#include "TomatoClockDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

CTomatoClockDlg::CTomatoClockDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CTomatoClockDlg::IDD, pParent)
{
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
	m_nRemainingSeconds = 50 * 60;
	m_nTotalSeconds = 50 * 60;
	m_bIsBlinking = false;
	m_bIsResting = false;
	m_bDragging = false;
}

void CTomatoClockDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
}

BEGIN_MESSAGE_MAP(CTomatoClockDlg, CDialog)
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_WM_TIMER()
	ON_WM_LBUTTONDOWN()
	ON_WM_MOUSEMOVE()
	ON_WM_LBUTTONUP()
	ON_WM_LBUTTONDBLCLK()
	ON_WM_ERASEBKGND()
END_MESSAGE_MAP()

BOOL CTomatoClockDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	SetIcon(m_hIcon, TRUE);
	SetIcon(m_hIcon, FALSE);

	int screenWidth = GetSystemMetrics(SM_CXSCREEN);
	int screenHeight = GetSystemMetrics(SM_CYSCREEN);
	
	int xPos = screenWidth * 95 / 100 - 60;
	int yPos = screenHeight * 5 / 100;

	ModifyStyle(WS_CAPTION | WS_SYSMENU | WS_THICKFRAME, 0);
	ModifyStyleEx(0, WS_EX_TOOLWINDOW | WS_EX_TOPMOST);
	SetWindowPos(&CWnd::wndTopMost, xPos, yPos, 60, 20, SWP_SHOWWINDOW);

	SetClassLongPtr(m_hWnd, GCLP_HBRBACKGROUND, (LONG_PTR)GetSysColorBrush(COLOR_WINDOW));
	SetTimer(1, 1000, NULL);

	return TRUE;
}

void CTomatoClockDlg::OnPaint()
{
	CPaintDC dc(this);
	CRect rect;
	GetClientRect(&rect);
	
	CBrush brush(GetSysColor(COLOR_WINDOW));
	dc.FillRect(rect, &brush);
	
	dc.SetBkColor(GetSysColor(COLOR_WINDOW));
	dc.SetTextColor(GetSysColor(COLOR_WINDOWTEXT));

	CString strTime;
	int minutes = m_nRemainingSeconds / 60;
	int seconds = m_nRemainingSeconds % 60;
	strTime.Format(_T("%02d:%02d"), minutes, seconds);

	dc.DrawText(strTime, rect, DT_CENTER | DT_VCENTER | DT_SINGLELINE);
}

HCURSOR CTomatoClockDlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CTomatoClockDlg::OnTimer(UINT_PTR nIDEvent)
{
	if (m_nRemainingSeconds > 0) {
		m_nRemainingSeconds--;
		
		if (m_nRemainingSeconds == 0) {
			if (!m_bIsResting) {
				Beep();
				m_bIsBlinking = true;
				m_nRemainingSeconds = 60;
			} else {
				m_nRemainingSeconds = 50 * 60;
				m_bIsResting = false;
				m_bIsBlinking = false;
			}
		}
	} else if (m_bIsBlinking) {
		m_nRemainingSeconds = 5 * 60;
		m_bIsBlinking = false;
		m_bIsResting = true;
	}

	Invalidate();
	CDialog::OnTimer(nIDEvent);
}

void CTomatoClockDlg::OnLButtonDown(UINT nFlags, CPoint point)
{
	CPoint ptScreen;
	GetCursorPos(&ptScreen);
	
	CRect rcWindow;
	GetWindowRect(&rcWindow);
	
	m_ptDragOffset = ptScreen - rcWindow.TopLeft();
	m_bDragging = true;
	SetCapture();
	
	CDialog::OnLButtonDown(nFlags, point);
}

void CTomatoClockDlg::OnMouseMove(UINT nFlags, CPoint point)
{
	if (m_bDragging && (nFlags & MK_LBUTTON))
	{
		CPoint ptScreen;
		GetCursorPos(&ptScreen);
		
		int x = ptScreen.x - m_ptDragOffset.x;
		int y = ptScreen.y - m_ptDragOffset.y;
		
		SetWindowPos(NULL, x, y, 0, 0, SWP_NOSIZE | SWP_NOZORDER | SWP_NOREDRAW | SWP_NOSENDCHANGING);
	}
	
	CDialog::OnMouseMove(nFlags, point);
}

void CTomatoClockDlg::OnLButtonUp(UINT nFlags, CPoint point)
{
	if (m_bDragging)
	{
		m_bDragging = false;
		ReleaseCapture();
	}
	CDialog::OnLButtonUp(nFlags, point);
}

void CTomatoClockDlg::OnLButtonDblClk(UINT nFlags, CPoint point)
{
	PostMessage(WM_CLOSE);
	CDialog::OnLButtonDblClk(nFlags, point);
}

BOOL CTomatoClockDlg::OnEraseBkgnd(CDC* pDC)
{
	return TRUE;
}

void CTomatoClockDlg::Beep()
{
	MessageBeep(MB_ICONEXCLAMATION);
}

void CTomatoClockDlg::UpdateDisplay()
{
	Invalidate();
}