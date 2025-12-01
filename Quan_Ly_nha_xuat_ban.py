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


def open_quan_ly_nha_xuat_ban(parent, server, database):
    win = tk.Toplevel(parent)
    win.title("Quản Lý Nhà Xuất Bản")
    win.geometry("700x450")
    win.transient(parent)
    win.grab_set()
    win.configure(bg=BG_MAIN)

    tk.Label(
        win,
        text="QUẢN LÝ NHÀ XUẤT BẢN",
        font=FONT_TITLE,
        bg=BG_MAIN,
        fg=FG_TITLE
    ).pack(padx=10, pady=(10, 5))

    input_frame = tk.Frame(win, bg=BG_MAIN)
    input_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(input_frame, text="Mã NXB:", bg=BG_MAIN).grid(row=0, column=0, sticky="e", padx=5, pady=4)
    entry_ma_nxb = tk.Entry(input_frame, width=30)
    entry_ma_nxb.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(input_frame, text="Tên NXB:", bg=BG_MAIN).grid(row=1, column=0, sticky="e", padx=5, pady=4)
    entry_ten_nxb = tk.Entry(input_frame, width=30)
    entry_ten_nxb.grid(row=1, column=1, padx=5, pady=4)

    tk.Label(input_frame, text="Địa chỉ:", bg=BG_MAIN).grid(row=2, column=0, sticky="e", padx=5, pady=4)
    entry_dia_chi = tk.Entry(input_frame, width=30)
    entry_dia_chi.grid(row=2, column=1, padx=5, pady=4)

    tree_nxb = ttk.Treeview(win, columns=("MaNXB", "TenNXB", "DiaChi"), show="headings", height=12)
    tree_nxb.heading("MaNXB", text="Mã NXB")
    tree_nxb.column("MaNXB", width=100, anchor=tk.W)
    tree_nxb.heading("TenNXB", text="Tên NXB")
    tree_nxb.column("TenNXB", width=200, anchor=tk.W)
    tree_nxb.heading("DiaChi", text="Địa chỉ")
    tree_nxb.column("DiaChi", width=300, anchor=tk.W)
    tree_nxb.pack(padx=10, pady=10, fill="both", expand=True)

    def tai_nxb():
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MaNXB, TenNXB, DiaChi FROM NHAXUATBAN ORDER BY MaNXB")
            rows = cur.fetchall()
            tree_nxb.delete(*tree_nxb.get_children())
            for row in rows:
                vals = [row[0], row[1], "" if row[2] is None else row[2]]
                tree_nxb.insert("", tk.END, values=vals)
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể tải NXB: {ex}")
        finally:
            conn.close()

    def them_nxb():
        ma = entry_ma_nxb.get().strip()
        ten = entry_ten_nxb.get().strip()
        dia_chi = entry_dia_chi.get().strip()
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên NXB.")
            return
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO NHAXUATBAN (MaNXB, TenNXB, DiaChi) VALUES (?, ?, ?)",
                       (ma, ten, dia_chi if dia_chi else None))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm NXB.")
            entry_ma_nxb.delete(0, tk.END)
            entry_ten_nxb.delete(0, tk.END)
            entry_dia_chi.delete(0, tk.END)
            tai_nxb()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể thêm NXB: {ex}")
        finally:
            conn.close()

    def sua_nxb():
        sel = tree_nxb.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn NXB để sửa.")
            return
        item_id = sel[0]
        vals = tree_nxb.item(item_id, "values")
        ma_cu = vals[0]

        ma = entry_ma_nxb.get().strip()
        ten = entry_ten_nxb.get().strip()
        dia_chi = entry_dia_chi.get().strip()
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên NXB.")
            return
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("UPDATE NHAXUATBAN SET MaNXB = ?, TenNXB = ?, DiaChi = ? WHERE MaNXB = ?",
                       (ma, ten, dia_chi if dia_chi else None, ma_cu))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật NXB.")
            entry_ma_nxb.delete(0, tk.END)
            entry_ten_nxb.delete(0, tk.END)
            entry_dia_chi.delete(0, tk.END)
            tai_nxb()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể cập nhật NXB: {ex}")
        finally:
            conn.close()

    def xoa_nxb():
        sel = tree_nxb.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn NXB để xóa.")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa NXB này?"):
            return
        item_id = sel[0]
        vals = tree_nxb.item(item_id, "values")
        ma = vals[0]

        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM NHAXUATBAN WHERE MaNXB = ?", (ma,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa NXB.")
            tai_nxb()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể xóa NXB: {ex}")
        finally:
            conn.close()

    def on_select_nxb(event=None):
        sel = tree_nxb.selection()
        if not sel:
            return
        item_id = sel[0]
        vals = tree_nxb.item(item_id, "values")
        entry_ma_nxb.delete(0, tk.END)
        entry_ma_nxb.insert(0, vals[0])
        entry_ten_nxb.delete(0, tk.END)
        entry_ten_nxb.insert(0, vals[1])
        entry_dia_chi.delete(0, tk.END)
        entry_dia_chi.insert(0, vals[2] if len(vals) > 2 else "")

    tree_nxb.bind("<<TreeviewSelect>>", on_select_nxb)

    btn_frame = tk.Frame(win, bg=BG_MAIN)
    btn_frame.pack(fill="x", padx=10, pady=(0, 10))
    ttk.Button(btn_frame, text="Thêm", command=them_nxb).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Sửa", command=sua_nxb).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Xóa", command=xoa_nxb).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Đóng", command=win.destroy).pack(side="right", padx=5)

    tai_nxb()