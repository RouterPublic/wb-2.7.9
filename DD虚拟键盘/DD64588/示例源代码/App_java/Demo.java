package com.zhc.demo;

import org.jawin.FuncPtr;
import org.jawin.ReturnFlags;
import org.jawin.io.LittleEndianOutputStream;
import org.jawin.io.NakedByteStream;

public class Demo {

	public static void main(String[] args) {
		//分别按下WIN+空格
      dydome("DD_key",601,1,-1);
      dydome("DD_key",603,1,-1);
      try {
		Thread.sleep(1000);
	} catch (InterruptedException e) {
		e.printStackTrace();
	}finally{
		   dydome("DD_key",601,2,-1);
		   dydome("DD_key",603,2,-1);
	}
      
	}
	 /**
     * Description 根据键值进行加密
     * @param method  dll里的方法名 
     * @param x  移动鼠标时传递非负数
     * @param y  移动鼠标时传递非负数
     * @param onclick  鼠标点击时传递非负数
     * @return void
     * @throws Exception
     */
	private static void dydome(String method,int x,int y,int onclick){
		NakedByteStream nbs = null;
		LittleEndianOutputStream leos  = null;
		try {
			FuncPtr fp = new FuncPtr("DD32.DLL", method);
			nbs = new NakedByteStream();
		    leos = new LittleEndianOutputStream(nbs);
			if(x >= 0){
				leos.writeInt(x);
			}
			if(y >= 0){
				leos.writeInt(y);
			}
			if(onclick >= 0){
				leos.writeInt(onclick);
			}
			fp.invoke("II32G::", 32, nbs, null, ReturnFlags.CHECK_FALSE);
			
		} catch (Exception e) {
			//e.printStackTrace();
		}finally{
			if(leos != null){
				leos = null;
			}
			if(nbs != null){
				nbs = null;
			}
		}
	}
	/*功能： 模拟鼠标点击
	参数： 1 =左键按下 ，2 =左键放开
	4 =右键按下 ，8 =右键放开
	16 =中键按下 ，32 =中键放开
	64 =4键按下 ，128 =4键放开
	256 =5键按下 ，512 =5键放开 
	例子：模拟鼠标右键 只需要连写(中间可添加延迟) dd_btn(4); dd_btn(8);*/
	private native static  void DD_btn(int onclick);
	/*功能： 模拟鼠标结对移动
	参数： 参数x , 参数y 以屏幕左上角为原点。
	例子： 把鼠标移动到分辨率1920*1080 的屏幕正中间，
	int x = 1920/2 ; int y = 1080/2;
	DD_mov(x,y) ;*/
	private native static  void DD_mov(int x,int y );
	/*	功能： 模拟鼠标相对移动
	参数： 参数dx , 参数dy 以当前坐标为原点。
	例子： 把鼠标向左移动10像素
	DD_movR(-10,0) ;*/

	private native static void DD_movR(int x,int y);

	/*	功能: 模拟鼠标滚轮
	参数: 1=前 , 2 = 后
	例子: 向前滚一格, DD_whl(1)*/
	private native static void DD_whl(int gl);

	/*	功能： 模拟键盘按键
	参数： 参数1 ，请查看[DD虚拟键盘码表]。
	参数2，1=按下，2=放开
	例子： 模拟TAB按键,只需连写(中间可添加延迟)
	DD_key(300, 1);
	DD_key(300, 2);*/
	private native static void DD_key(int code,int type);

	/*	功能： 转换Windows虚拟键码到 DD 专用键码.
	参数： Windows虚拟键码
	例子： int ddcode = DD_todc(VK_ESCAPE);
	Dim ddcode As int32 = DD_todc(27);*/
	private native static int DD_todc(int codee);

	/*	功能： 直接输入键盘上可见字符和空格
	参数： 字符串, (注意，这个参数不是int32 类型)
	例子： DD_str("MyEmail@aa.bb.cc !@#$")*/
	private native static void DD_str(String kjcode);


}
