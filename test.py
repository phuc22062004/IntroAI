import threading
import time
import tkinter as tk
from tkinter import messagebox

# Hàm thuật toán cần chạy
def long_running_algorithm(callback):
    time.sleep(5)  # Giả lập thời gian chạy thuật toán
    callback("Thuật toán đã hoàn thành!")
import tkinter as tk
from tkinter import ttk
import time
import threading

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Main Application")

        # Nút bắt đầu để mở Splash Screen
        self.start_button = tk.Button(root, text="Start", command=self.show_splash)
        self.start_button.pack(pady=20)

    def show_splash(self):
        # Tạo cửa sổ Splash Screen
        splash = tk.Toplevel(self.root)
        splash.title("Loading...")
        splash.geometry("300x150")

        # Thêm Progressbar vào cửa sổ Splash Screen
        progress = ttk.Progressbar(splash, orient="horizontal", length=200, mode="indeterminate")
        progress.pack(pady=30)
        progress.start()

        # Hàm để đóng Splash Screen sau khi xong
        def close_splash():
            splash.destroy()
            self.show_main_window()

        # Giả lập một tác vụ dài (ví dụ, tải dữ liệu, tính toán)
        threading.Thread(target=self.long_running_task, args=(close_splash,)).start()

    def long_running_task(self, callback):
        # Giả lập công việc lâu dài (tải dữ liệu, tính toán)
        time.sleep(5)  # Thời gian chờ giả lập
        callback()  # Khi xong, gọi hàm để đóng Splash Screen và mở cửa sổ chính

    def show_main_window(self):
        # Tạo cửa sổ chính
        main_label = tk.Label(self.root, text="Welcome to the main application!")
        main_label.pack(pady=20)


# Khởi tạo GUI
root = tk.Tk()
app = App(root)
root.mainloop()

# Hàm bắt đầu luồng chạy thuật toán
def start_algorithm():
    # Tạo một luồng riêng để chạy thuật toán
    threading.Thread(target=long_running_algorithm, args=(on_algorithm_complete,)).start()

# Hàm được gọi khi thuật toán hoàn thành
def on_algorithm_complete(message):
    # Sử dụng hàm after() để gửi tín hiệu cập nhật giao diện chính
    root.after(0, lambda: messagebox.showinfo("Thông báo", message))

# Thiết lập GUI
root = tk.Tk()
root.title("Multi-threaded Tkinter Example")

# Nút bắt đầu thuật toán
start_button = tk.Button(root, text="Bắt đầu thuật toán", command=start_algorithm)
start_button.pack(pady=20)

# Chạy GUI
root.mainloop()
