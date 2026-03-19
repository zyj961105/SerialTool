#---------------------------------
# 安卓串口调试工具 (货道/贩卖机专用)
# 指令大全 0x01~0x95 + 串口可配置
#---------------------------------
from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
import serial
import threading
import time

class SerialApp(App):
    def build(self):
        self.ser = None
        self.title = "货道调试工具(安卓版)"
        
        # 主标签页
        tabs = TabbedPanel(do_default_tab=False)
        tab1 = TabbedPanelItem(text="串口调试")
        tab2 = TabbedPanelItem(text="指令大全")
        
        # --------- 标签1：串口配置 ---------
        root = BoxLayout(orientation="vertical", padding=10, spacing=5)
        
        # 串口参数
        p = BoxLayout(size_hint_y=0.15)
        self.port_spn = Spinner(text="ttyS3", values=["ttyS3","ttyS4","ttyMT1","ttyMT2","ttyUSB0"])
        self.baud_spn = Spinner(text="115200", values=["9600","115200","460800","921600"])
        self.bit_spn = Spinner(text="8", values=["5","6","7","8"])
        self.stop_spn = Spinner(text="1", values=["1","2"])
        self.parity_spn = Spinner(text="N", values=["N","O","E"])
        
        p.add_widget(Label(text="串口:"))
        p.add_widget(self.port_spn)
        p.add_widget(Label(text="波特:"))
        p.add_widget(self.baud_spn)
        p.add_widget(self.bit_spn)
        p.add_widget(self.stop_spn)
        p.add_widget(self.parity_spn)
        root.add_widget(p)
        
        # 开关按钮
        btn_box = BoxLayout(size_hint_y=0.1)
        self.open_btn = Button(text="打开串口", background_color=(0,1,0,1))
        self.open_btn.bind(on_press=self.toggle_serial)
        btn_box.add_widget(self.open_btn)
        root.add_widget(btn_box)
        
        # 日志
        self.log = TextInput(readonly=True, font_size=14)
        root.add_widget(self.log)
        
        tab1.add_widget(root)
        
        # --------- 标签2：指令大全 0x01~0x95 ---------
        cmd_layout = GridLayout(cols=3, padding=10, spacing=8)
        cmds = [
            ("系统复位 0x01","5A FF 01 00 00 00 0D 0A"),
            ("版本号 0x02","5A FF 02 00 00 00 0D 0A"),
            ("锁控制 0x40","5A FF 40 00 00 00 0D 0A"),
            ("工作模式 0x50","5A FF 50 00 00 00 0D 0A"),
            ("自动出货 0x60","5A FF 60 01 01 00 00 0D 0A"),
            ("停止 0x65","5A FF 65 01 00 00 00 0D 0A"),
            ("归位 0x81","5A FF 81 01 00 00 00 0D 0A"),
            ("出厂设置 0x95","5A FF 95 00 00 00 0D 0A"),
        ]
        for name, hexstr in cmds:
            b = Button(text=name, size_hint_y=None, height=80)
            b.bind(on_press=lambda x,h=hexstr: self.send(h))
            cmd_layout.add_widget(b)
        tab2.add_widget(cmd_layout)
        
        tabs.add_widget(tab1)
        tabs.add_widget(tab2)
        return tabs
    
    def toggle_serial(self, instance):
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.open_btn.text = "打开串口"
            self.log("串口已关闭\n")
        else:
            try:
                self.ser = serial.Serial(
                    port=self.port_spn.text,
                    baudrate=int(self.baud_spn.text),
                    bytesize=int(self.bit_spn.text),
                    stopbits=int(self.stop_spn.text),
                    parity=self.parity_spn.text,
                    timeout=1
                )
                self.open_btn.text = "关闭串口"
                self.log_insert("串口已打开\n")
                threading.Thread(target=self.read_task, daemon=True).start()
            except:
                self.log_insert("打开失败\n")
    
    def send(self, hexstr):
        if not self.ser or not self.ser.is_open:
            self.log_insert("未打开串口\n")
            return
        try:
            data = bytes.fromhex(hexstr.replace(" ",""))
            self.ser.write(data)
            self.log_insert(f"发送:{hexstr}\n")
        except:
            self.log_insert("发送失败\n")
    
    def read_task(self):
        while self.ser and self.ser.is_open:
            try:
                d = self.ser.read(100)
                if d:
                    self.log_insert(f"接收:{d.hex()}\n")
            except:
                break
            time.sleep(0.05)
    
    def log_insert(self, msg):
        self.log.text += msg

if __name__ == "__main__":
    SerialApp().run()