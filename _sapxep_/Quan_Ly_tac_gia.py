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


def open_quan_ly_tac_gia(parent, server, database):
    win = tk.Toplevel(parent)
    win.title("Quản Lý Tác Giả")
    win.geometry("600x400")
    win.transient(parent)
    win.grab_set()
    win.configure(bg=BG_MAIN)

    tk.Label(
        win,
        text="QUẢN LÝ TÁC GIẢ",
        font=FONT_TITLE,
        bg=BG_MAIN,
        fg=FG_TITLE
    ).pack(padx=10, pady=(10, 5))

    input_frame = tk.Frame(win, bg=BG_MAIN)
    input_frame.pack(fill="x", padx=10, pady=5)

    tk.Label(input_frame, text="Mã Tác Giả:", bg=BG_MAIN).grid(row=0, column=0, sticky="e", padx=5, pady=4)
    entry_ma_tg = tk.Entry(input_frame, width=30)
    entry_ma_tg.grid(row=0, column=1, padx=5, pady=4)

    tk.Label(input_frame, text="Tên Tác Giả:", bg=BG_MAIN).grid(row=1, column=0, sticky="e", padx=5, pady=4)
    entry_ten_tg = tk.Entry(input_frame, width=30)
    entry_ten_tg.grid(row=1, column=1, padx=5, pady=4)

    tree_tg = ttk.Treeview(win, columns=("MaTacGia", "TenTacGia"), show="headings", height=10)
    tree_tg.heading("MaTacGia", text="Mã Tác Giả")
    tree_tg.column("MaTacGia", width=150, anchor=tk.W)
    tree_tg.heading("TenTacGia", text="Tên Tác Giả")
    tree_tg.column("TenTacGia", width=350, anchor=tk.W)
    tree_tg.pack(padx=10, pady=10, fill="both", expand=True)

    def tai_tac_gia():
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("SELECT MaTacGia, TenTacGia FROM TACGIA ORDER BY MaTacGia")
            rows = cur.fetchall()
            tree_tg.delete(*tree_tg.get_children())
            for row in rows:
                tree_tg.insert("", tk.END, values=row)
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể tải tác giả: {ex}")
        finally:
            conn.close()

    def them_tac_gia():
        ma = entry_ma_tg.get().strip()
        ten = entry_ten_tg.get().strip()
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên tác giả.")
            return
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO TACGIA (MaTacGia, TenTacGia) VALUES (?, ?)", (ma, ten))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm tác giả.")
            entry_ma_tg.delete(0, tk.END)
            entry_ten_tg.delete(0, tk.END)
            tai_tac_gia()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể thêm tác giả: {ex}")
        finally:
            conn.close()

    def sua_tac_gia():
        sel = tree_tg.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn tác giả để sửa.")
            return
        item_id = sel[0]
        vals = tree_tg.item(item_id, "values")
        ma_cu = vals[0]

        ma = entry_ma_tg.get().strip()
        ten = entry_ten_tg.get().strip()
        if not ma or not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã và Tên tác giả.")
            return
        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("UPDATE TACGIA SET MaTacGia = ?, TenTacGia = ? WHERE MaTacGia = ?", (ma, ten, ma_cu))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật tác giả.")
            entry_ma_tg.delete(0, tk.END)
            entry_ten_tg.delete(0, tk.END)
            tai_tac_gia()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể cập nhật tác giả: {ex}")
        finally:
            conn.close()

    def xoa_tac_gia():
        sel = tree_tg.selection()
        if not sel:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn tác giả để xóa.")
            return
        if not messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tác giả này?"):
            return
        item_id = sel[0]
        vals = tree_tg.item(item_id, "values")
        ma = vals[0]

        conn = ket_noi_db(server, database)
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM TACGIA WHERE MaTacGia = ?", (ma,))
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa tác giả.")
            tai_tac_gia()
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể xóa tác giả: {ex}")
        finally:
            conn.close()

    def on_select_tg(event=None):
        sel = tree_tg.selection()
        if not sel:
            return
        item_id = sel[0]
        vals = tree_tg.item(item_id, "values")
        entry_ma_tg.delete(0, tk.END)
        entry_ma_tg.insert(0, vals[0])
        entry_ten_tg.delete(0, tk.END)
        entry_ten_tg.insert(0, vals[1])

    tree_tg.bind("<<TreeviewSelect>>", on_select_tg)

    btn_frame = tk.Frame(win, bg=BG_MAIN)
    btn_frame.pack(fill="x", padx=10, pady=(0, 10))
    ttk.Button(btn_frame, text="Thêm", command=them_tac_gia).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Sửa", command=sua_tac_gia).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Xóa", command=xoa_tac_gia).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Đóng", command=win.destroy).pack(side="right", padx=5)

    tai_tac_gia()