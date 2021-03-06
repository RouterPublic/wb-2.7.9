#include "StdAfx.h"
#include "DD.h"

CDD::CDD(void)
{
	m_hModule = NULL;
}

CDD::~CDD(void)
{
	if (m_hModule)
	{
		::FreeLibrary(m_hModule);
	}
}

int CDD::GetFunAddr(CString dllfile)
{
	if ( -1 == ::GetFileAttributes(dllfile))
	{
		return -11; //文件不存在
	}

	m_hModule = ::LoadLibrary(dllfile);

	if ( m_hModule==NULL)
	{
		return -12; // 载入库错误
	}

	// 函数使用说明 g or b
	DD_btn = (pDD_btn )GetProcAddress(m_hModule,"DD_btn"); 
	DD_whl = (pDD_whl )GetProcAddress(m_hModule,"DD_whl"); 
	DD_key = (pDD_key )GetProcAddress(m_hModule,"DD_key"); 
	DD_mov = (pDD_mov)GetProcAddress(m_hModule,"DD_mov"); 
	DD_chk = (pDD_chk)GetProcAddress(m_hModule,"DD_chk"); 
	DD_str  = (pDD_str)GetProcAddress(m_hModule,"DD_str"); 
	DD_todc  = (pDD_todc)GetProcAddress(m_hModule,"DD_todc"); 
	DD_movR = (pDD_movR)GetProcAddress(m_hModule,"DD_movR"); 

	DD_MouseMove  = (pDD_MouseMove)GetProcAddress(m_hModule,"DD_MouseMove"); 
	DD_SnapPic  = (pDD_SnapPic)GetProcAddress(m_hModule,"DD_SnapPic"); 
	DD_PickColor  = (pDD_PickColor)GetProcAddress(m_hModule,"DD_PickColor"); 
	DD_GetActiveWindow  = (pDD_GetActiveWindow)GetProcAddress(m_hModule,"DD_GetActiveWindow"); 

	//判断一下，是否正确获取了函数地址
	if ( DD_btn && DD_whl && DD_key && DD_mov && DD_chk && DD_str  && DD_todc && DD_movR)
	{
		//再判断一下，增强函数地址
		if (DD_MouseMove && DD_SnapPic && DD_PickColor && DD_GetActiveWindow)
		{
			return 2;
		}
		return 1; // 成功
	}
	else
	{
		return -13; // 获取函数地址错误
	}
}

