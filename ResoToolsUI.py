"""
本代码由[Tkinter布局助手]生成
官网:https://www.pytk.net
QQ交流群:905019785
在线反馈:https://support.qq.com/product/618914
"""
import random
from tkinter import *
from tkinter.ttk import *
from tokenize import Single

from utils.UserLog import obj_log as log
from utils.CommonUtils import *
from utils.GameExceptions import *
from utils.cvTools import *

from game.ResoGame import ResoadbObj
from game.ResoGoodsCal import *

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
        self.tk_text_textLog = self.__tk_text_textLog(self)
        self.tk_button_btnAutoStart = self.__tk_button_btnAutoStart(self)
        # self.tk_button_btnAutoStop = self.__tk_button_btnAutoStop(self)
        self.tk_button_fgtHundunXB = self.__tk_button_fgtHundunXB(self)
        self.tk_button_tieanju = self.__tk_button_tieanju(self)
        self.tk_button_autorunbusiness = self.__tk_button_autorunbusiness(self)
        self.tk_label_ltx3qkfa = self.__tk_label_ltx3qkfa(self)
        self.tk_label_ltx3rfde = self.__tk_label_ltx3rfde(self)
        self.tk_select_box_startcity = self.__tk_select_box_startcity(self)
        self.tk_select_box_endcity = self.__tk_select_box_endcity(self)
        self.tk_button_activity = self.__tk_button_activity(self)
        self.tk_select_box_activity = self.__tk_select_box_activity(self)
        self.tk_check_button_autotili = self.__tk_check_button_autotili(self)
        self.tk_check_button_autopilao = self.__tk_check_button_autopilao(self)
        self.tk_label_pushupprice = self.__tk_label_pushupprice(self)
        self.tk_select_box_lucjoop6 = self.__tk_select_box_lucjoop6(self)
        self.tk_label_haggle = self.__tk_label_haggle(self)
        self.tk_select_box_lucjq694 = self.__tk_select_box_lucjq694(self)
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
    def __tk_text_textLog(self,parent):
        text = Text(parent)
        text.place(x=0, y=211, width=800, height=289)
        return text
    def __tk_button_btnAutoStart(self,parent):
        btn = Button(parent, text="自动巡航", takefocus=False,)
        btn.place(x=0, y=0, width=156, height=30)
        return btn
    # def __tk_button_btnAutoStop(self,parent):
    #     btn = Button(parent, text="关闭自动巡航", takefocus=False,)
    #     btn.place(x=0, y=49, width=155, height=30)
    #     return btn
    def __tk_button_fgtHundunXB(self,parent):
        btn = Button(parent, text="混沌信标挑战", takefocus=False,)
        btn.place(x=290, y=0, width=80, height=30)
        return btn
    def __tk_button_tieanju(self,parent):
        btn = Button(parent, text="铁安局", takefocus=False,)
        btn.place(x=283, y=50, width=80, height=30)
        return btn
    def __tk_button_autorunbusiness(self,parent):
        btn = Button(parent, text="自动跑商", takefocus=False,)
        btn.place(x=0, y=100, width=80, height=30)
        return btn
    def __tk_label_ltx3qkfa(self,parent):
        label = Label(parent,text="始发地：",anchor="center", )
        label.place(x=0, y=136, width=50, height=30)
        return label
    def __tk_label_ltx3rfde(self,parent):
        label = Label(parent,text="目的地：",anchor="center", )
        label.place(x=0, y=173, width=50, height=30)
        return label
    def __tk_select_box_startcity(self,parent):
        cb = Combobox(parent, state="readonly", )
        # cb['values'] = ("列表框","Python","Tkinter Helper")
        cb.place(x=54, y=136, width=150, height=30)
        return cb
    def __tk_select_box_endcity(self,parent):
        cb = Combobox(parent, state="readonly", )
        # cb['values'] = ("列表框","Python","Tkinter Helper")
        cb.place(x=54, y=173, width=150, height=30)
        return cb
    def __tk_button_activity(self,parent):
        btn = Button(parent, text="活动", takefocus=False,)
        btn.place(x=402, y=4, width=50, height=30)
        return btn
    def __tk_select_box_activity(self,parent):
        cb = Combobox(parent, state="readonly", )
        # cb['values'] = ("列表框","Python","Tkinter Helper")
        cb.place(x=309, y=90, width=150, height=30)
        return cb
    def __tk_check_button_autotili(self,parent):
        cb = Checkbutton(parent,text="自动体力",)
        cb.place(x=677, y=1, width=119, height=30)
        return cb
    def __tk_check_button_autopilao(self,parent):
        cb = Checkbutton(parent,text="自动疲劳",)
        cb.place(x=674, y=43, width=121, height=30)
        return cb
    def __tk_label_pushupprice(self,parent):
        label = Label(parent,text="抬价",anchor="center", )
        label.place(x=93, y=96, width=35, height=30)
        return label
    def __tk_select_box_lucjoop6(self,parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = [str(x) for x in range(1, 11)]
        cb.place(x=139, y=102, width=41, height=30)
        return cb
    def __tk_label_haggle(self,parent):
        label = Label(parent,text="讲价",anchor="center", )
        label.place(x=190, y=100, width=35, height=30)
        return label
    def __tk_select_box_lucjq694(self,parent):
        cb = Combobox(parent, state="readonly", )
        cb['values'] = [str(x) for x in range(1, 11)]
        cb.place(x=229, y=102, width=37, height=30)
        return cb

    
class WinMan():
    def __init__(self):        
        self.threadObjs = threadsManager()
        
        self.leftclick_fgtHundunXB_num = 0
        self.leftclick_tieanju_num = 0
        self.leftclick_autocruise_num = 0
        # self.__event_bind()
        # self.__style_config()
        # self.ctl.init(self)
        self.lattest_leftclick_time = 0
        self.lattest_leftclick_name = ""
    
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
        
    def global_click_count(self, evt):
        clicktime = getNowTime()
        clickname = evt.widget.cget("text")  # 获取点击控件的名称
        if clickname == self.lattest_leftclick_name and (clicktime - self.lattest_leftclick_time) < 60:
            self.resoobj.adb_obj.reconnect()
        
        log.info("亲，在为您在准备【{}】了，请勿频繁点击哟~~~~~".format(clickname))
        
        self.lattest_leftclick_time = clicktime
        self.lattest_leftclick_name = clickname
        
        
    def btnAutoStart(self, evt):
        self.global_click_count(evt)
        if evt.num == 1:
            if self.leftclick_autocruise_num % 2 == 0:
                self.threadObjs.startNewThread(self.resoobj.autoDetectExcute, "autoxunhang")
            else:
                if not self.threadObjs.killTthread("autoxunhang"):
                    self.threadObjs.startNewThread(self.resoobj.autoDetectExcute, "autoxunhang")
            self.leftclick_autocruise_num += 1
            # self.winui.tk_button_btnAutoStart.config(state=DISABLED)
            # self.winui.tk_button_btnAutoStop.config(state=NORMAL)
        
    # def btnAutoStop(self, evt):
    #     self.threadObjs.killTthread("autoxunhang")
    #     self.winui.tk_button_btnAutoStart.config(state=NORMAL)
    #     self.winui.tk_button_btnAutoStop.config(state=DISABLED)
    
    def fgtHundunXB(self, evt):
        self.global_click_count(evt)
        if evt.num == 1:
            if self.leftclick_fgtHundunXB_num % 2 == 0:
                self.threadObjs.startNewThread(self.resoobj.fightFloatTree, "hundunxb")
            else:
                if not self.threadObjs.killTthread("hundunxb"):
                    self.threadObjs.startNewThread(self.resoobj.fightFloatTree, "hundunxb")
                    
            self.leftclick_fgtHundunXB_num += 1
            
    def btnAutoIronSecurity(self, evt):
        self.global_click_count(evt)
        if evt.num == 1:
            if self.leftclick_tieanju_num % 2 == 0:
                self.threadObjs.startNewThread(self.resoobj.autoIronSecurity, "autoIronSecurity")
            else:
                if not self.threadObjs.killTthread("autoIronSecurity"):
                    self.threadObjs.startNewThread(self.resoobj.autoIronSecurity, "autoIronSecurity")
            self.leftclick_tieanju_num += 1
            
    def btnAutoRunBusiness(self,evt):
        self.global_click_count(evt)
        startcity = self.winui.tk_select_box_startcity.get()
        endcity = self.winui.tk_select_box_endcity.get()
        
        assert startcity != "" and startcity is not None
        assert endcity != "" and endcity is not None
        if evt.num == 1:
            if self.leftclick_tieanju_num % 2 == 0:
                self.threadObjs.startNewThread(self.resoobj.autoRunningBusiness, "autoRunBusiness", startcity, endcity)
            else:
                self.threadObjs.killTthread("autoRunBusiness")
            self.leftclick_tieanju_num += 1   
            
    def __timeThread(self):
        self.threadObjs.startNewTimeThread(301, staticResoGoodCal.getGoodsinfo, "updategoods")     
    
    def __event_bind(self):
        # self.winui.bind_all("<Button-1>", self.global_click_count)
        self.winui.tk_button_btnAutoStart.bind('<Button-1>', self.btnAutoStart)
        # self.winui.tk_button_btnAutoStop.bind('<Button-1>', self.btnAutoStop)
        self.winui.tk_button_fgtHundunXB.bind('<Button-1>', self.fgtHundunXB)
        self.winui.tk_button_tieanju.bind('<Button-1>', self.btnAutoIronSecurity)
        self.winui.tk_button_autorunbusiness.bind('<Button-1>', self.btnAutoRunBusiness)
        
        # self.winui.tk_button_btnAutoStop.config(state=DISABLED)
        
        self.winui.tk_select_box_startcity["values"] = self.resoobj.city_list
        self.winui.tk_select_box_endcity["values"] = self.resoobj.city_list
        # 将日志和文本框绑定
        handler = TkinterLogHandler(self.winui.tk_text_textLog)
        log.add(handler, level="INFO")
        
    def start(self):
        self.__event_bind()
        self.__timeThread()
        self.winui.mainloop()


def on_select(event, combobox:Combobox, entry:Entry):
    selected_item = combobox.get()
    entry.delete(0, END)
    entry.insert(END, selected_item)
    
if __name__ == "__main__":
    # 启动脚本相关的数据
    resoobj = ResoadbObj()
    resoobj.setAdbInfo("127.0.0.1", "16384", os.path.join(os.getcwd(),"connection/adb.exe"), "tmp" )
    winctl = WinGUI()
    winmain = WinMan()
    winmain.setGameObj(resoobj, winctl)
    
    winmain.start()