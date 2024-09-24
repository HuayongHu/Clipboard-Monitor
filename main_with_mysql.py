import time
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread, Event
import pyperclip
import datetime
import pymysql

class ClipboardMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clipboard-Monitor——支持云同步版 by MisterHuhua")
        self.clipboard_history = []
        self.stop_event = Event()
        self.monitoring = False
        self.init_ui()
        self.db_config = {
            'user': 'misterhuhua',
            'password': '你自己的数据库密码',
            'host': 'mysql.sqlpub.com',
            'port': 3306,
            'database': 'ClipboardMonitor'
        }
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

        self.sync_button = tk.Button(button_frame, text="从云端同步", command=self.sync_history)
        self.sync_button.pack(side='left', padx=10, pady=10)

        self.clear_button = tk.Button(button_frame, text="清空云端数据", command=self.clear_cloud_data)
        self.clear_button.pack(side='left', padx=10, pady=10)

        self.export_button = tk.Button(button_frame, text="导出到本地", command=self.export_clipboard_history)
        self.export_button.pack(side='right', padx=10, pady=10)

    def clear_cloud_data(self):
        if messagebox.askyesno("警告", "你确定要清空云端数据吗？这将无法恢复！"):
            try:
                conn = pymysql.connect(**self.db_config)
                cursor = conn.cursor()
                cursor.execute("DELETE FROM clipboard_data")
                conn.commit()
                cursor.close()
                conn.close()
                messagebox.showinfo("成功", "云端数据已成功清空。")
            except pymysql.MySQLError as err:
                messagebox.showerror("错误", f"清空数据时发生错误：{err}")
    def sync_history(self):
        # Disable the sync button while the operation is in progress
        self.sync_button.config(state='disabled')
        # Start a thread to perform the database synchronization
        sync_thread = Thread(target=self.download_from_cloud)
        sync_thread.start()

    def download_from_cloud(self):
        try:
            conn = pymysql.connect(**self.db_config)
            cursor = conn.cursor()
            # 修改查询以按时间戳升序排列
            query = "SELECT timestamp, content FROM clipboard_data ORDER BY timestamp ASC"
            cursor.execute(query)
            results = cursor.fetchall()
            # 清空文本框中的内容，准备显示同步的历史记录
            self.text_box.configure(state='normal')
            self.text_box.delete('1.0', tk.END)
            self.text_box.configure(state='disabled')

            # 更新文本框内容，旧的记录先展示
            for timestamp, content in results:
                self.update_text_box(f"{timestamp}: {content}\n")
            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("同步成功", "历史记录已成功同步。")
        except pymysql.MySQLError as err:
            messagebox.showerror("同步失败", f"同步时发生错误：{err}")
        finally:
            # Re-enable the sync button after the operation
            self.sync_button.config(state='normal')

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
                self.upload_to_cloud(timestamp.strftime('%Y-%m-%d %H:%M:%S'), current_clipboard_content)
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

    def upload_to_cloud(self, timestamp, content):
        try:
            conn = pymysql.connect(host='mysql.sqlpub.com',
                                   user='misterq',
                                   password='DVdaBESftbFNtgvf',
                                   db='cloudip',
                                   port=3306)
            cursor = conn.cursor()
            query = "INSERT INTO clipboard_data (timestamp, content) VALUES (%s, %s)"
            cursor.execute(query, (timestamp, content))
            conn.commit()
            cursor.close()
            conn.close()
        except pymysql.MySQLError as err:
            print(f"Error: {err}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ClipboardMonitorApp(root)
    root.mainloop()
