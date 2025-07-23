// TomatoClockDlg.h : header file

#pragma once

#include <afxwin.h>

class CTomatoClockDlg : public CDialog
{
public:
	CTomatoClockDlg(CWnd* pParent = NULL);
	enum { IDD = IDD_TOMATOCLOCK_DIALOG };

protected:
	virtual void DoDataExchange(CDataExchange* pDX);
	virtual BOOL OnInitDialog();
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnTimer(UINT_PTR nIDEvent);
	afx_msg void OnLButtonDown(UINT nFlags, CPoint point);
	afx_msg void OnMouseMove(UINT nFlags, CPoint point);
	afx_msg void OnLButtonUp(UINT nFlags, CPoint point);
	afx_msg void OnLButtonDblClk(UINT nFlags, CPoint point);
	afx_msg BOOL OnEraseBkgnd(CDC* pDC);
	DECLARE_MESSAGE_MAP()

private:
	HICON m_hIcon;
	int m_nRemainingSeconds;
	int m_nTotalSeconds;
	bool m_bIsBlinking;
	bool m_bIsResting;
	CPoint m_ptDragStart;
	CPoint m_ptDragOffset;
	bool m_bDragging;
	void UpdateDisplay();
	void Beep();
};