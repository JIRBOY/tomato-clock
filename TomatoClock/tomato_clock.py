import tkinter as tk
import time
import threading

class TomatoClock:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("番茄钟")
        
        # 计算屏幕右上角位置，距离边缘5%
        screen_width = self.root.winfo_screenwidth()
        x_pos = int(screen_width * 0.95) - 60  # 60是窗口宽度
        y_pos = int(self.root.winfo_screenheight() * 0.05)
        
        self.root.geometry(f"60x20+{x_pos}+{y_pos}")
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
        
        # Variables for window dragging
        self.drag_data = {"x": 0, "y": 0}
        
        self.remaining = 50 * 60  # 50 minutes
        self.total = 50 * 60
        self.is_blinking = False
        self.is_resting = False
        self.is_paused = False
        self.original_time = 50 * 60
        
        # 获取Windows系统背景颜色
        try:
            import ctypes
            # 获取系统颜色 (COLOR_WINDOW = 5)
            color = ctypes.windll.user32.GetSysColor(5)
            # 转换为RGB格式
            r = color & 0xFF
            g = (color >> 8) & 0xFF
            b = (color >> 16) & 0xFF
            self.bg_color = f'#{r:02x}{g:02x}{b:02x}'
        except:
            self.bg_color = '#F0F0F0'  # 默认Windows背景色
        
        self.label = tk.Label(self.root, text="50:00", font=('Arial', 12), bg=self.bg_color)
        self.label.pack(fill=tk.BOTH, expand=True)
        
        # Bind events for dragging
        self.label.bind('<Button-1>', self.start_drag)
        self.label.bind('<B1-Motion>', self.do_drag)
        self.root.bind('<Double-Button-1>', lambda e: self.root.quit())
        
        # 键盘快捷键
        self.root.bind('<space>', self.toggle_pause)
        self.root.bind('<r>', self.reset_timer)
        self.root.bind('<s>', self.skip_rest)
        
        self.update_timer()
    
    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def do_drag(self, event):
        x = self.root.winfo_x() + (event.x - self.drag_data["x"])
        y = self.root.winfo_y() + (event.y - self.drag_data["y"])
        self.root.geometry(f"+{x}+{y}")

    def toggle_pause(self, event=None):
        """切换暂停/继续"""
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.label.config(fg='red')  # 暂停时显示红色
        else:
            self.label.config(fg='black')  # 继续时恢复黑色
    
    def reset_timer(self, event=None):
        """重置计时器"""
        self.remaining = self.original_time
        self.is_blinking = False
        self.is_resting = False
        self.is_paused = False
        self.label.config(fg='black')
    
    def skip_rest(self, event=None):
        """跳过休息时间"""
        if self.is_resting:
            self.remaining = self.original_time
            self.is_resting = False
            self.is_blinking = False
            self.is_paused = False
            self.label.config(fg='black')
    
    def update_timer(self):
        if not self.is_paused and self.remaining > 0:
            self.remaining -= 1
            if self.remaining == 0:
                if not self.is_resting:
                    # 50分钟到了，开始1分钟蜂鸣
                    self.root.bell()
                    self.is_blinking = True
                    self.remaining = 60  # 1分钟蜂鸣
                else:
                    # 休息完了，重新开始50分钟
                    self.remaining = self.original_time
                    self.is_resting = False
                    self.is_blinking = False
        elif not self.is_paused and self.is_blinking:
            # 1分钟蜂鸣后，开始5分钟休息
            self.remaining = 5 * 60
            self.is_blinking = False
            self.is_resting = True
        
        minutes = self.remaining // 60
        seconds = self.remaining % 60
        
        # 闪烁效果
        if self.is_blinking and int(time.time()) % 2 == 0:
            self.label.config(text=f"{minutes:02d}:{seconds:02d}", fg='red')
        else:
            self.label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        self.root.after(1000, self.update_timer)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    clock = TomatoClock()
    clock.run()