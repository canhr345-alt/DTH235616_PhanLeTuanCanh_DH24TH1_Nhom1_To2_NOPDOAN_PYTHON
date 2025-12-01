import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def open_child():
    win = tk.Toplevel(root)
    win.title("Cửa sổ con")
    win.transient(root)   # gắn liên quan với cửa sổ chính
    win.grab_set()        # modal: khóa tương tác với cửa sổ chính
    win.geometry("300x120")

    tk.Label(win, text="Nhập nội dung:").pack(pady=(10,0))
    entry = tk.Entry(win, width=30)
    entry.pack(pady=6)
    entry.focus_set()

    def on_ok():
        win.result = entry.get().strip()
        messagebox.showinfo("Thông báo", f"Nội dung đã nhập: {win.result}")
        win.destroy()

    def on_cancel():
        win.result = None
        win.destroy()

    btn_frame = tk.Frame(win)
    btn_frame.pack(pady=8)
    tk.Button(btn_frame, text="OK", width=8, command=on_ok).pack(side="left", padx=6)
    tk.Button(btn_frame, text="Cancel", width=8, command=on_cancel).pack(side="left", padx=6)

    win.protocol("WM_DELETE_WINDOW", on_cancel)  # xử lý đóng cửa sổ
    root.wait_window(win)  # chờ cửa sổ con đóng

    # Sau khi đóng, đọc kết quả
    result = win.result
    if result:
        lbl_result.config(text=f"Kết quả: {result}")
    else:
        lbl_result.config(text="Đã hủy hoặc không có dữ liệu")

root = tk.Tk()
root.title("Ví dụ cửa sổ con")
root.geometry("320x160")

tk.Button(root, text="Mở cửa sổ con", command=open_child).pack(pady=20)
lbl_result = tk.Label(root, text="Kết quả: ")
lbl_result.pack()

root.mainloop()