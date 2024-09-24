import time
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread, Event
import pyperclip
import datetime

class ClipboardMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard Monitor by MisterHuhua")

        self.clipboard_history = []
        self.stop_event = Event()
        self.monitoring = False

        self.init_ui()

    def init_ui(self):
        # 设置UI布局
        self.root.geometry("600x400")  # 设置窗口大小

        # 创建文本框用于显示剪切板信息
        self.text_box = tk.Text(self.root, height=16, state='disabled')
        self.text_box.pack(fill='both', expand=True)

        # 创建按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill='x')

        # 创建按钮
        self.start_button = tk.Button(button_frame, text="开始记录", command=self.start_monitoring)
        self.start_button.pack(side='left', padx=10, pady=10)

        self.stop_button = tk.Button(button_frame, text="停止记录", command=self.stop_monitoring, state='disabled')
        self.stop_button.pack(side='left', padx=10, pady=10)

        self.clear_button = tk.Button(button_frame, text="清空剪切板", command=self.clear_clipboard)
        self.clear_button.pack(side='left', padx=10, pady=10)

        self.export_button = tk.Button(button_frame, text="导出剪切板历史", command=self.export_clipboard_history)
        self.export_button.pack(side='right', padx=10, pady=10)

    def update_text_box(self, text):
        # 更新文本框内容
        self.text_box.configure(state='normal')
        # 在每个记录之间添加分割线
        self.text_box.insert(tk.END, '---' * 28 + '\n')
        self.text_box.insert(tk.END, text + '\n')
        self.text_box.configure(state='disabled')
        self.text_box.see(tk.END)  # 自动滚动到文本框底部
    def start_monitoring(self):
        if not self.monitoring:
            self.monitoring = True
            self.stop_event.clear()
            self.monitor_thread = Thread(target=self.monitor_clipboard)
            self.monitor_thread.daemon = True
            self.monitor_thread.start()
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')

    def monitor_clipboard(self):
        last_clipboard_content = ""
        while not self.stop_event.is_set():
            current_clipboard_content = pyperclip.paste()
            if current_clipboard_content != last_clipboard_content:
                timestamp = datetime.datetime.now()
                self.clipboard_history.append((timestamp, current_clipboard_content))
                self.update_text_box(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {current_clipboard_content}")
                last_clipboard_content = current_clipboard_content
            time.sleep(1)

    def stop_monitoring(self):
        self.stop_event.set()
        self.monitoring = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')

    def clear_clipboard(self):
        pyperclip.copy('')
        self.update_text_box("剪切板已清空。")

    def export_clipboard_history(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if save_path:
            with open(save_path, 'w') as f:
                for timestamp, content in self.clipboard_history:
                    f.write(f"{timestamp.strftime('%Y-%m-%d %H:%M:%S')}: {content}\n")
            messagebox.showinfo("导出成功", "剪切板历史已成功导出。")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardMonitorApp(root)
    root.mainloop()
