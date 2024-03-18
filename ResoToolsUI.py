"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *

from utils.UserLog import obj_log as log
from utils.CommonUtils import *
from utils.GameExceptions import *
from utils.cvTools import *

from game.ResoGame import ResoadbObj

class TkinterLogHandler:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(END, message)
        self.text_widget.see(END)  # Scroll to the end


class WinGUI(Tk):
    def __init__(self):
        super().__init__()
        self.__win()
        self.tk_label_ltpr0f75 = self.__tk_label_ltpr0f75(self)
        self.tk_text_textLog = self.__tk_text_textLog(self)
        self.tk_label_ltpr1pz9 = self.__tk_label_ltpr1pz9(self)
        self.tk_button_btnAutoStart = self.__tk_button_btnAutoStart(self)
        self.tk_label_ltpr4mos = self.__tk_label_ltpr4mos(self)
        self.tk_label_ltpr54it = self.__tk_label_ltpr54it(self)
        self.tk_button_btnAutoStop = self.__tk_button_btnAutoStop(self)
        self.tk_button_fgtHundunXB = self.__tk_button_fgtHundunXB(self)
        self.tk_input_fgthdxbNum = self.__tk_input_fgthdxbNum(self)
        self.tk_label_ltpr9q0z = self.__tk_label_ltpr9q0z(self)
        self.tk_button_tieanju = self.__tk_button_tieanju(self)
        self.tk_label_ltx3p6yw = self.__tk_label_ltx3p6yw(self)
        self.tk_button_autorunbusiness = self.__tk_button_autorunbusiness(self)
        self.tk_label_ltx3qkfa = self.__tk_label_ltx3qkfa(self)
        self.tk_input_ltx3qygc = self.__tk_input_ltx3qygc(self)
        self.tk_label_ltx3rfde = self.__tk_label_ltx3rfde(self)
        self.tk_input_ltx3s9jb = self.__tk_input_ltx3s9jb(self)
    def __win(self):
        self.title("Reso Tools")
        # 设置窗口大小、居中
        width = 800
        height = 500
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        
        self.resizable(width=False, height=False)
        
    def scrollbar_autohide(self,vbar, hbar, widget):
        """自动隐藏滚动条"""
        def show():
            if vbar: vbar.lift(widget)
            if hbar: hbar.lift(widget)
        def hide():
            if vbar: vbar.lower(widget)
            if hbar: hbar.lower(widget)
        hide()
        widget.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Enter>", lambda e: show())
        if vbar: vbar.bind("<Leave>", lambda e: hide())
        if hbar: hbar.bind("<Enter>", lambda e: show())
        if hbar: hbar.bind("<Leave>", lambda e: hide())
        widget.bind("<Leave>", lambda e: hide())
    
    def v_scrollbar(self,vbar, widget, x, y, w, h, pw, ph):
        widget.configure(yscrollcommand=vbar.set)
        vbar.config(command=widget.yview)
        vbar.place(relx=(w + x) / pw, rely=y / ph, relheight=h / ph, anchor='ne')
    def h_scrollbar(self,hbar, widget, x, y, w, h, pw, ph):
        widget.configure(xscrollcommand=hbar.set)
        hbar.config(command=widget.xview)
        hbar.place(relx=x / pw, rely=(y + h) / ph, relwidth=w / pw, anchor='sw')
    def create_bar(self,master, widget,is_vbar,is_hbar, x, y, w, h, pw, ph):
        vbar, hbar = None, None
        if is_vbar:
            vbar = Scrollbar(master)
            self.v_scrollbar(vbar, widget, x, y, w, h, pw, ph)
        if is_hbar:
            hbar = Scrollbar(master, orient="horizontal")
            self.h_scrollbar(hbar, widget, x, y, w, h, pw, ph)
        self.scrollbar_autohide(vbar, hbar, widget)
    def __tk_label_ltpr0f75(self,parent):
        label = Label(parent,text="Reso Tools",anchor="center", )
        label.place(x=0, y=0, width=72, height=30)
        return label
    def __tk_text_textLog(self,parent):
        text = Text(parent)
        text.place(x=0, y=211, width=800, height=289)
        return text
    def __tk_label_ltpr1pz9(self,parent):
        label = Label(parent,text="日志记录",anchor="center", )
        label.place(x=0, y=178, width=63, height=30)
        return label
    def __tk_button_btnAutoStart(self,parent):
        btn = Button(parent, text="开启自动巡航", takefocus=False,)
        btn.place(x=0, y=27, width=156, height=30)
        return btn
    def __tk_label_ltpr4mos(self,parent):
        label = Label(parent,text="--------------------------------------------",anchor="center", )
        label.place(x=0, y=104, width=212, height=30)
        return label
    def __tk_label_ltpr54it(self,parent):
        label = Label(parent,text="--------------------------------------------",anchor="center", )
        label.place(x=0, y=0, width=212, height=30)
        return label
    def __tk_button_btnAutoStop(self,parent):
        btn = Button(parent, text="关闭自动巡航", takefocus=False,)
        btn.place(x=0, y=67, width=155, height=30)
        return btn
    def __tk_button_fgtHundunXB(self,parent):
        btn = Button(parent, text="混沌信标挑战", takefocus=False,)
        btn.place(x=275, y=0, width=80, height=30)
        return btn
    def __tk_input_fgthdxbNum(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=371, y=0, width=95, height=30)
        return ipt
    def __tk_label_ltpr9q0z(self,parent):
        label = Label(parent,text="次数",anchor="center", )
        label.place(x=476, y=0, width=50, height=30)
        return label
    def __tk_button_tieanju(self,parent):
        btn = Button(parent, text="铁安局", takefocus=False,)
        btn.place(x=275, y=40, width=80, height=30)
        return btn
    def __tk_label_ltx3p6yw(self,parent):
        label = Label(parent,text="--------------------------------------------",anchor="center", )
        label.place(x=275, y=62, width=212, height=30)
        return label
    def __tk_button_autorunbusiness(self,parent):
        btn = Button(parent, text="自动跑商", takefocus=False,)
        btn.place(x=275, y=100, width=80, height=30)
        return btn
    def __tk_label_ltx3qkfa(self,parent):
        label = Label(parent,text="始发地：",anchor="center", )
        label.place(x=360, y=104, width=50, height=30)
        return label
    def __tk_input_ltx3qygc(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=420, y=104, width=117, height=30)
        return ipt
    def __tk_label_ltx3rfde(self,parent):
        label = Label(parent,text="目的地：",anchor="center", )
        label.place(x=360, y=140, width=50, height=30)
        return label
    def __tk_input_ltx3s9jb(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=420, y=140, width=117, height=30)
        return ipt
    
class WinMan():
    def __init__(self):        
        self.threadObjs = threadsManager()
        
        self.leftclick_fgtHundunXB_num = 0
        
        # self.__event_bind()
        # self.__style_config()
        # self.ctl.init(self)
    
    def convert_to_number(self, text):
        number = 0
        if text.isdigit():  # 检查输入是否为整数
            number = int(text)  # 转换为整数
        elif text.replace('.', '', 1).isdigit():  # 检查输入是否为浮点数
            number = float(text)  # 转换为浮点数
        else:
            log.error("请输入整数")
            return 0
        return number
        
    def setGameObj(self, gameobj:ResoadbObj, gui:WinGUI):
        self.resoobj = gameobj
        self.winui = gui
        # self.ctl.init(self)
        
    def btnAutoStart(self, evt):
        if evt.num == 1:
            self.threadObjs.startNewThread(self.resoobj.autoDetectExcute, "autoxunhang")
            self.winui.tk_button_btnAutoStart.config(state=DISABLED)
            self.winui.tk_button_btnAutoStop.config(state=NORMAL)
        
    def btnAutoStop(self, evt):
        self.threadObjs.killTthread("autoxunhang")
        self.winui.tk_button_btnAutoStart.config(state=NORMAL)
        self.winui.tk_button_btnAutoStop.config(state=DISABLED)
    
    def fgtHundunXB(self, evt):
        if evt.num == 1:
            if self.leftclick_fgtHundunXB_num % 2 == 0:
                text = self.winui.tk_input_fgthdxbNum.get()
                fnum = self.convert_to_number(text)
                self.threadObjs.startNewThread(self.resoobj.fightFloatTree, "hundunxb", fnum)
            else:
                self.threadObjs.killTthread("hundunxb")
            self.leftclick_fgtHundunXB_num += 1
    
    def __event_bind(self):
        self.winui.tk_button_btnAutoStart.bind('<Button-1>', self.btnAutoStart)
        self.winui.tk_button_btnAutoStop.bind('<Button-1>', self.btnAutoStop)
        self.winui.tk_button_fgtHundunXB.bind('<Button-1>', self.fgtHundunXB)
        
        self.winui.tk_button_btnAutoStop.config(state=DISABLED)
        
        # 将日志和文本框绑定
        handler = TkinterLogHandler(self.winui.tk_text_textLog)
        log.add(handler, level="INFO")
        
    def start(self):
        self.__event_bind()
        self.winui.mainloop()
        
    
if __name__ == "__main__":
    # 启动脚本相关的数据
    resoobj = ResoadbObj()
    resoobj.setAdbInfo("127.0.0.1", "16384", os.path.join(os.getcwd(),"connection/adb.exe"), "tmp" )
    winctl = WinGUI()
    winmain = WinMan()
    winmain.setGameObj(resoobj, winctl)
    
    winmain.start()