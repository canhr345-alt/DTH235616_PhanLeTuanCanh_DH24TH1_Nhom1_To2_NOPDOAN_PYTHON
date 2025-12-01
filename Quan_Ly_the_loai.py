import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from app_style import BG_MAIN, FG_TITLE, FONT_TITLE


def ket_noi_db(server, database):
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={server};"
            f"DATABASE={database};"
            "Trusted_Connection=yes;"
        )
        return pyodbc.connect(conn_str)
    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi kết nối", f"Không thể kết nối: {ex}")
        return None


def open_quan_ly_the_loai(parent, server, database):
    win = tk.Toplevel(parent)
    win.title("Quản Lý Thể Loại")
    win.geometry("600x400")
    win.transient(parent)
    win.grab_set()
    win.configure(bg=BG_MAIN)

    tk.Label(
        win,
        text="QUẢN LÝ THỂ LOẠI",
        font=FONT_TITLE,
        bg=BG_MAIN,
        fg=FG_TITLE
    ).pack(padx=10, pady=(10, 5))

    input_frame = tk.Frame(win, bg=BG_MAIN)
    input_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(input_frame, text="Mã Thể Loại:", bg=BG_MAIN).grid(row=0, column=0, sticky="e", padx=5, pady=4)
    entry_ma_tl = tk.Entry(input_frame, width=30)
    entry_ma_tl.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(input_frame, text="Tên Thể Loại:", bg=BG_MAIN).grid(row=1, column=0, sticky="e", padx=5, pady=4)
    entry_ten_tl = tk.Entry(input_frame, width=30)
    entry_ten_tl.grid(row=1, column=1, padx=5, pady=4)

    tree_tl = ttk.Treeview(win, columns=("MaTheLoai", "TenTheLoai"), show="headings", height=10)
    tree_tl.heading("MaTheLoai", text="Mã Thể Loại")
    tree_tl.column("MaTheLoai", width=150, anchor=tk.W)
    tree_tl.heading("TenTheLoai", text="Tên Thể Loại")
    tree_tl.column("TenTheLoai", width=350, anchor=tk.W)
    tree_tl.pack(padx=10, pady=10, fill="both", expand=True)

    def tai_the_loai():
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MaTheLoai, TenTheLoai FROM THELOAI ORDER BY MaTheLoai")
            rows = cur.fetchall()
            tree_tl.delete(*tree_tl.get_children())
            for row in rows:
                tree_tl.insert("", tk.END, values=row)
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể tải thể loại: {ex}")
        finally:
            conn.close()

    def them_the_loai():
        ma = entry_ma_tl.get().strip()
        ten = entry_ten_tl.get().strip()
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên thể loại.")
            return
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO THELOAI (MaTheLoai, TenTheLoai) VALUES (?, ?)", (ma, ten))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm thể loại.")
            entry_ma_tl.delete(0, tk.END)
            entry_ten_tl.delete(0, tk.END)
            tai_the_loai()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể thêm thể loại: {ex}")
        finally:
            conn.close()

    def sua_the_loai():
        sel = tree_tl.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn thể loại để sửa.")
            return
        item_id = sel[0]
        vals = tree_tl.item(item_id, "values")
        ma_cu = vals[0]

        ma = entry_ma_tl.get().strip()
        ten = entry_ten_tl.get().strip()
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên thể loại.")
            return
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("UPDATE THELOAI SET MaTheLoai = ?, TenTheLoai = ? WHERE MaTheLoai = ?", (ma, ten, ma_cu))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật thể loại.")
            entry_ma_tl.delete(0, tk.END)
            entry_ten_tl.delete(0, tk.END)
            tai_the_loai()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể cập nhật thể loại: {ex}")
        finally:
            conn.close()

    def xoa_the_loai():
        sel = tree_tl.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn thể loại để xóa.")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa thể loại này?"):
            return
        item_id = sel[0]
        vals = tree_tl.item(item_id, "values")
        ma = vals[0]

        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM THELOAI WHERE MaTheLoai = ?", (ma,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa thể loại.")
            tai_the_loai()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể xóa thể loại: {ex}")
        finally:
            conn.close()

    def on_select_tl(event=None):
        sel = tree_tl.selection()
        if not sel:
            return
        item_id = sel[0]
        vals = tree_tl.item(item_id, "values")
        entry_ma_tl.delete(0, tk.END)
        entry_ma_tl.insert(0, vals[0])
        entry_ten_tl.delete(0, tk.END)
        entry_ten_tl.insert(0, vals[1])

    tree_tl.bind("<<TreeviewSelect>>", on_select_tl)

    btn_frame = tk.Frame(win, bg=BG_MAIN)
    btn_frame.pack(fill="x", padx=10, pady=(0, 10))
    ttk.Button(btn_frame, text="Thêm", command=them_the_loai).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Sửa", command=sua_the_loai).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Xóa", command=xoa_the_loai).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Đóng", command=win.destroy).pack(side="right", padx=5)

    tai_the_loai()