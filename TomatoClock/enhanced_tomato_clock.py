import tkinter as tk
from tkinter import messagebox
import time
import threading
import json
import os
import locale
import sys

class EnhancedTomatoClock:
    def __init__(self):
        self.root = tk.Tk()
        
        # 自动检测系统语言
        self.detect_language()
        
        self.root.title(self.texts['title'])
        
        # 配置文件路径
        self.config_file = os.path.join(os.path.expanduser("~"), ".tomato_config.json")
        self.load_config()
        
        # 窗口设置
        self.setup_window()
        
        # 计时器状态
        self.remaining = self.config.get("work_time", 25) * 60
        self.total = self.remaining
        self.is_blinking = False
        self.is_resting = False
        self.is_paused = False
        self.session_count = 0
        
        # 创建UI
        self.create_widgets()
        
        # 绑定事件
        self.bind_events()
        
        self.update_timer()
    
    def detect_language(self):
        """自动检测系统语言并设置对应文本"""
        try:
            # 获取系统默认语言
            system_lang = locale.getdefaultlocale()[0]
            
            # 中文语言包
            self.texts_cn = {
                'title': '🍅 超级番茄钟',
                'work_status': '工作中',
                'short_break_status': '短休息',
                'long_break_status': '长休息',
                'paused_status': '已暂停',
                'settings': '设置',
                'work_time': '工作时长 (分钟):',
                'short_break': '短休息时长 (分钟):',
                'long_break': '长休息时长 (分钟):',
                'sessions_interval': '长休息间隔 (番茄数):',
                'save': '保存',
                'error': '错误',
                'invalid_number': '请输入有效的数字',
                'pause_continue': '暂停/继续 (空格)',
                'reset': '重置 (R)',
                'skip': '跳过 (S)',
                'config': '设置',
                'exit': '退出',
                'session_text': '第 {} 个番茄'
            }
            
            # 英文语言包
            self.texts_en = {
                'title': '🍅 Enhanced Tomato Clock',
                'work_status': 'Working',
                'short_break_status': 'Short Break',
                'long_break_status': 'Long Break',
                'paused_status': 'Paused',
                'settings': 'Settings',
                'work_time': 'Work Time (minutes):',
                'short_break': 'Short Break (minutes):',
                'long_break': 'Long Break (minutes):',
                'sessions_interval': 'Long Break Interval (sessions):',
                'save': 'Save',
                'error': 'Error',
                'invalid_number': 'Please enter valid numbers',
                'pause_continue': 'Pause/Continue (Space)',
                'reset': 'Reset (R)',
                'skip': 'Skip (S)',
                'config': 'Settings',
                'exit': 'Exit',
                'session_text': 'Session {}'
            }
            
            # 根据系统语言选择
            if system_lang and ('zh' in system_lang.lower() or 'cn' in system_lang.lower()):
                self.texts = self.texts_cn
                self.language = 'zh'
            else:
                self.texts = self.texts_en
                self.language = 'en'
                
        except Exception:
            # 默认使用英文
            self.texts = self.texts_en
            self.language = 'en'

    def load_config(self):
        """加载配置文件"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = {
                    "work_time": 25 if self.language == 'en' else 35,
                    "short_break": 5,
                    "long_break": 10,
                    "sessions_before_long_break": 4 if self.language == 'en' else 5,
                    "window_x": None,
                    "window_y": None,
                    "always_on_top": True,
                    "language": self.language
                }
                self.save_config()
        except Exception as e:
            print(f"加载配置失败: {e}")
            self.config = self.get_default_config()
            
        # 更新当前语言
        if 'language' in self.config:
            self.language = self.config['language']
            if self.language == 'zh':
                self.texts = self.texts_cn
            else:
                self.texts = self.texts_en
    
    def get_default_config(self):
        return {
            "work_time": 25 if self.language == 'en' else 35,
            "short_break": 5,
            "long_break": 10,
            "sessions_before_long_break": 4 if self.language == 'en' else 5,
            "window_x": None,
            "window_y": None,
            "always_on_top": True,
            "language": self.language
        }
    
    def save_config(self):
        """保存配置文件"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"保存配置失败: {e}")
    
    def setup_window(self):
        """设置窗口"""
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        if self.config["window_x"] is None:
            x_pos = int(screen_width * 0.95) - 120
            y_pos = int(screen_height * 0.05)
        else:
            x_pos = self.config["window_x"]
            y_pos = self.config["window_y"]
        
        self.root.geometry(f"120x100+{x_pos}+{y_pos}")
        self.root.attributes('-topmost', self.config["always_on_top"])
        self.root.overrideredirect(True)
        self.root.attributes('-alpha', 0.9)
        
        # 窗口拖动变量
        self.drag_data = {"x": 0, "y": 0}
    
    def create_widgets(self):
        """创建UI控件"""
        # 主框架
        self.main_frame = tk.Frame(self.root, bg='#2c3e50')
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 时间标签
        self.time_label = tk.Label(
            self.main_frame,
            text="25:00",
            font=('Arial', 24, 'bold'),
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        self.time_label.pack(pady=5)
        
        # 状态标签
        self.status_label = tk.Label(
            self.main_frame,
            text=self.texts['work_status'],
            font=('Arial', 10),
            fg='#3498db',
            bg='#2c3e50'
        )
        self.status_label.pack()
        
        # 会话计数
        self.session_label = tk.Label(
            self.main_frame,
            text=self.texts['session_text'].format(0),
            font=('Arial', 8),
            fg='#95a5a6',
            bg='#2c3e50'
        )
        self.session_label.pack()
    
    def bind_events(self):
        """绑定事件"""
        # 鼠标事件
        self.time_label.bind('<Button-1>', self.start_drag)
        self.time_label.bind('<B1-Motion>', self.do_drag)
        self.root.bind('<Double-Button-1>', lambda e: self.show_menu())
        
        # 键盘快捷键
        self.root.bind('<space>', self.toggle_pause)
        self.root.bind('<r>', self.reset_timer)
        self.root.bind('<s>', self.skip_phase)
        self.root.bind('<n>', self.next_phase)
        self.root.bind('<q>', lambda e: self.root.quit())
        self.root.bind('<c>', self.show_config)
    
    def start_drag(self, event):
        """开始拖动"""
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
    
    def do_drag(self, event):
        """拖动窗口"""
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")
        
        # 保存位置
        self.config["window_x"] = x
        self.config["window_y"] = y
        self.save_config()
    
    def toggle_pause(self, event=None):
        """切换暂停/继续"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.status_label.config(text=self.texts['paused_status'], fg='#e74c3c')
        else:
            self.update_status_text()
    
    def reset_timer(self, event=None):
        """重置计时器"""
        self.remaining = self.get_current_phase_time() * 60
        self.is_blinking = False
        self.is_paused = False
        self.update_status_text()
    
    def skip_phase(self, event=None):
        """跳过当前阶段"""
        if self.is_resting:
            self.start_work()
        else:
            self.start_break()
    
    def next_phase(self, event=None):
        """进入下一阶段"""
        self.skip_phase()
    
    def get_current_phase_time(self):
        """获取当前阶段时间（分钟）"""
        if self.is_resting:
            if self.session_count % self.config["sessions_before_long_break"] == 0:
                return self.config["long_break"]
            else:
                return self.config["short_break"]
        else:
            return self.config["work_time"]
    
    def start_work(self):
        """开始工作"""
        self.remaining = self.config["work_time"] * 60
        self.is_resting = False
        self.is_blinking = False
        self.is_paused = False
        self.update_status_text()
    
    def start_break(self):
        """开始休息"""
        if not self.is_resting:
            self.session_count += 1
        
        if self.session_count % self.config["sessions_before_long_break"] == 0:
            self.remaining = self.config["long_break"] * 60
        else:
            self.remaining = self.config["short_break"] * 60
        
        self.is_resting = True
        self.is_blinking = False
        self.is_paused = False
        self.update_status_text()
    
    def update_status_text(self):
        """更新状态文本"""
        if self.is_paused:
            self.status_label.config(text=self.texts['paused_status'], fg='#e74c3c')
        elif self.is_resting:
            if self.session_count % self.config["sessions_before_long_break"] == 0:
                self.status_label.config(text=self.texts['long_break_status'], fg='#9b59b6')
            else:
                self.status_label.config(text=self.texts['short_break_status'], fg='#2ecc71')
        else:
            self.status_label.config(text=self.texts['work_status'], fg='#3498db')
        
        self.session_label.config(text=self.texts['session_text'].format(self.session_count))
    
    def show_menu(self):
        """显示右键菜单"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label=self.texts['pause_continue'], command=self.toggle_pause)
        menu.add_command(label=self.texts['reset'], command=self.reset_timer)
        menu.add_command(label=self.texts['skip'], command=self.skip_phase)
        menu.add_separator()
        menu.add_command(label=self.texts['config'], command=self.show_config)
        menu.add_separator()
        menu.add_command(label=self.texts['exit'], command=self.root.quit)
        
        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        menu.post(x, y)
    
    def show_config(self, event=None):
        """显示配置窗口"""
        config_window = tk.Toplevel(self.root)
        config_window.title(self.texts['settings'])
        
        # 计算屏幕居中位置
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        window_width = 160
        window_height = 280
        
        x_pos = (screen_width - window_width) // 2
        y_pos = (screen_height - window_height) // 2
        
        config_window.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")
        config_window.transient(self.root)
        config_window.grab_set()
        
        # 工作时长
        tk.Label(config_window, text=self.texts['work_time']).pack(pady=5)
        work_entry = tk.Entry(config_window)
        work_entry.insert(0, str(self.config["work_time"]))
        work_entry.pack()
        
        # 短休息时长
        tk.Label(config_window, text=self.texts['short_break']).pack(pady=5)
        short_entry = tk.Entry(config_window)
        short_entry.insert(0, str(self.config["short_break"]))
        short_entry.pack()
        
        # 长休息时长
        tk.Label(config_window, text=self.texts['long_break']).pack(pady=5)
        long_entry = tk.Entry(config_window)
        long_entry.insert(0, str(self.config["long_break"]))
        long_entry.pack()
        
        # 长休息间隔
        tk.Label(config_window, text=self.texts['sessions_interval']).pack(pady=5)
        interval_entry = tk.Entry(config_window)
        interval_entry.insert(0, str(self.config["sessions_before_long_break"]))
        interval_entry.pack()
        
        def save_changes():
            try:
                self.config["work_time"] = int(work_entry.get())
                self.config["short_break"] = int(short_entry.get())
                self.config["long_break"] = int(long_entry.get())
                self.config["sessions_before_long_break"] = int(interval_entry.get())
                self.save_config()
                
                # 重置当前计时器
                self.reset_timer()
                config_window.destroy()
            except ValueError:
                messagebox.showerror(self.texts['error'], self.texts['invalid_number'])
        
        tk.Button(config_window, text=self.texts['save'], command=save_changes).pack(pady=20)
    
    def update_timer(self):
        """更新计时器"""
        if not self.is_paused and self.remaining > 0:
            self.remaining -= 1
            
            if self.remaining == 0:
                if not self.is_resting:
                    # 工作结束，开始休息
                    self.root.bell()
                    self.start_break()
                else:
                    # 休息结束，开始工作
                    self.start_work()
        
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        
        # 更新显示
        if self.is_blinking and int(time.time()) % 2 == 0:
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}", fg='#e74c3c')
        else:
            self.time_label.config(text=f"{minutes:02d}:{seconds:02d}")
            if not self.is_paused:
                self.time_label.config(fg='#ecf0f1')
        
        self.root.after(1000, self.update_timer)
    
    def run(self):
        """运行应用"""
        self.root.mainloop()

if __name__ == "__main__":
    clock = EnhancedTomatoClock()
    clock.run()