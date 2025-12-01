import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc
from Quan_Ly_tac_gia import open_quan_ly_tac_gia
from Quan_Ly_the_loai import open_quan_ly_the_loai
from Quan_Ly_nha_xuat_ban import open_quan_ly_nha_xuat_ban
from app_style import setup_style, BG_MAIN, FG_TITLE, FONT_TITLE

setup_style()

SERVER = r"MSI\CANH"
DATABASE = "QLBSS"


def ket_noi_db():
    try:
        conn_str = (
            "DRIVER={ODBC Driver 17 for SQL Server};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            "Trusted_Connection=yes;"
        )
        return pyodbc.connect(conn_str)
    except pyodbc.Error as ex:
        messagebox.showerror(
            "Lỗi kết nối",
            f"Không thể kết nối đến SQL Server.\nChi tiết: {ex}"
        )
        return None


def tai_du_lieu(tree: ttk.Treeview):
    conn = ket_noi_db()
    if conn is None:
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SACH")
        rows = cursor.fetchall()

        cols = [col[0] for col in cursor.description]

        tree.delete(*tree.get_children())
        tree["columns"] = cols

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor=tk.W)

        for row in rows:
            vals = ["" if v is None else str(v) for v in row]
            tree.insert("", tk.END, values=vals)

    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi truy vấn", f"Có lỗi khi tải dữ liệu: {ex}")
    finally:
        conn.close()


root = tk.Tk()
root.title("HỆ THỐNG QUẢN LÝ BÁN SÁCH")
root.geometry("1000x600")
root.configure(bg=BG_MAIN)

COT_MAC_DINH = ("MaSach", "TenSach", "GiaBan", "SoLuongTon",
                "MaTheLoai", "MaTacGia", "MaNXB")

title_frame = tk.Frame(root, bg=BG_MAIN)
title_frame.pack(fill="x", padx=10, pady=(10, 5))

lbl_title = tk.Label(
    title_frame,
    text="HỆ THỐNG QUẢN LÝ BÁN SÁCH",
    font=FONT_TITLE,
    bg=BG_MAIN,
    fg=FG_TITLE
)
lbl_title.pack(side="left")

search_frame = tk.Frame(root, bg=BG_MAIN)
search_frame.pack(fill="x", padx=10, pady=(0, 5))

tk.Label(
    search_frame,
    text="Tìm kiếm:",
    bg=BG_MAIN,
    font=("Segoe UI", 10)
).pack(side="left")

entry_search = tk.Entry(search_frame, width=30)
entry_search.pack(side="left", padx=(5, 5))

btn_search = tk.Button(search_frame, text="Tìm", width=10)
btn_search.pack(side="left")

btn_reload = tk.Button(search_frame, text="Tải lại", width=10)
btn_reload.pack(side="left", padx=(5, 0))

table_frame = tk.Frame(root)
table_frame.pack(fill="both", expand=True, padx=10, pady=(0, 5))

tree = ttk.Treeview(table_frame, columns=COT_MAC_DINH, show="headings")

scroll_y = tk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scroll_y.set)
scroll_y.pack(side="right", fill="y")

tree.pack(side="left", fill="both", expand=True)

tree.heading("MaSach", text="Mã Sách")
tree.column("MaSach", width=80, anchor=tk.E)

tree.heading("TenSach", text="Tên Sách")
tree.column("TenSach", width=350, anchor=tk.W)

tree.heading("GiaBan", text="Giá Bán")
tree.column("GiaBan", width=120, anchor=tk.E)

tree.heading("SoLuongTon", text="Tồn Kho")
tree.column("SoLuongTon", width=80, anchor=tk.E)

tree.heading("MaTheLoai", text="Mã Thể Loại")
tree.column("MaTheLoai", width=100, anchor=tk.W)

tree.heading("MaTacGia", text="Mã Tác Giả")
tree.column("MaTacGia", width=100, anchor=tk.W)

tree.heading("MaNXB", text="Mã Nhà Xuất Bản")
tree.column("MaNXB", width=120, anchor=tk.W)


def them_sach():
    win = tk.Toplevel(root)
    win.title("Thêm Sách")
    win.geometry("450x400")
    win.transient(root)
    win.grab_set()
    win.configure(bg="#ffffff")

    cols = list(tree["columns"]) or list(COT_MAC_DINH)
    entries = {}

    tk.Label(
        win,
        text="THÔNG TIN SÁCH",
        font=("Segoe UI", 12, "bold"),
        bg="#ffffff",
        fg=FG_TITLE
    ).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10))

    start_row = 1
    for i, col in enumerate(cols):
        tk.Label(
            win,
            text=col + ":",
            bg="#ffffff",
            anchor="e"
        ).grid(row=start_row + i, column=0, padx=10, pady=4, sticky="e")

        e = tk.Entry(win, width=35)
        e.grid(row=start_row + i, column=1, padx=10, pady=4, sticky="w")
        entries[col] = e

    def submit():
        vals = [entries[c].get().strip() for c in cols]

        if not vals[0]:
            messagebox.showwarning("Thiếu dữ liệu", "Mã sách không được để trống.")
            return

        cols_sql = ",".join(cols)
        placeholders = ",".join(["?"] * len(cols))
        sql = f"INSERT INTO SACH ({cols_sql}) VALUES ({placeholders})"

        conn = ket_noi_db()
        if conn is None:
            return

        try:
            cur = conn.cursor()
            cur.execute(sql, vals)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm sách mới.")
            win.destroy()
            tai_du_lieu(tree)
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể thêm sách: {ex}")
        finally:
            conn.close()

    btn_frame = tk.Frame(win, bg="#ffffff")
    btn_frame.grid(row=start_row + len(cols), column=0, columnspan=2, pady=10)

    tk.Button(btn_frame, text="Lưu", width=10, command=submit).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Đóng", width=10, command=win.destroy).pack(side="left", padx=5)


def sua_sach():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 sách để sửa.")
        return
    if len(sel) > 1:
        messagebox.showwarning("Chọn 1 bản ghi", "Vui lòng chỉ chọn một sách.")
        return

    item_id = sel[0]
    vals = tree.item(item_id, "values")
    cols = list(tree["columns"]) or list(COT_MAC_DINH)

    win = tk.Toplevel(root)
    win.title("Sửa Sách")
    win.geometry("450x400")
    win.transient(root)
    win.grab_set()
    win.configure(bg="#ffffff")

    entries = {}

    tk.Label(
        win,
        text="CẬP NHẬT THÔNG TIN SÁCH",
        font=("Segoe UI", 12, "bold"),
        bg="#ffffff",
        fg=FG_TITLE
    ).grid(row=0, column=0, columnspan=2, padx=10, pady=(10, 10))

    start_row = 1
    for i, col in enumerate(cols):
        tk.Label(
            win,
            text=col + ":",
            bg="#ffffff",
            anchor="e"
        ).grid(row=start_row + i, column=0, padx=10, pady=4, sticky="e")

        e = tk.Entry(win, width=35)
        e.grid(row=start_row + i, column=1, padx=10, pady=4, sticky="w")
        try:
            e.insert(0, "" if vals[i] is None else str(vals[i]))
        except Exception:
            pass
        entries[col] = e

    original_ma = vals[0] if vals else None

    def submit_edit():
        new_vals = [entries[c].get().strip() for c in cols]

        if not new_vals[0]:
            messagebox.showwarning("Thiếu dữ liệu", "Mã sách không được để trống.")
            return

        set_clause = ",".join([f"{c}=?" for c in cols])
        sql = f"UPDATE SACH SET {set_clause} WHERE MaSach = ?"
        params = new_vals + [original_ma]

        conn = ket_noi_db()
        if conn is None:
            return

        try:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã cập nhật sách.")
            win.destroy()
            tai_du_lieu(tree)
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể cập nhật sách: {ex}")
        finally:
            conn.close()

    btn_frame = tk.Frame(win, bg="#ffffff")
    btn_frame.grid(row=start_row + len(cols), column=0, columnspan=2, pady=10)

    tk.Button(btn_frame, text="Lưu", width=10, command=submit_edit).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Đóng", width=10, command=win.destroy).pack(side="left", padx=5)


def xoa_sach():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 hoặc nhiều sách để xóa.")
        return

    masach_list = []
    for item_id in sel:
        vals = tree.item(item_id, "values")
        if vals:
            masach_list.append(vals[0])

    if not masach_list:
        messagebox.showwarning("Lỗi", "Không thể xác định Mã sách để xóa.")
        return

    if not messagebox.askyesno(
        "Xác nhận",
        f"Bạn có chắc muốn xóa {len(masach_list)} sách đã chọn?"
    ):
        return

    conn = ket_noi_db()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        sql = "DELETE FROM SACH WHERE MaSach = ?"
        for m in masach_list:
            cur.execute(sql, (m,))
        conn.commit()
        messagebox.showinfo("Thành công", "Đã xóa sách.")
        tai_du_lieu(tree)
    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi", f"Không thể xóa sách: {ex}")
    finally:
        conn.close()


def tim_kiem():
    q = entry_search.get().strip()

    if q == "":
        tai_du_lieu(tree)
        return

    conn = ket_noi_db()
    if conn is None:
        return

    try:
        cur = conn.cursor()
        pattern = f"%{q}%"
        sql = """
            SELECT * FROM SACH
            WHERE MaSach LIKE ?
               OR TenSach LIKE ?
               OR MaTacGia LIKE ?
               OR MaTheLoai LIKE ?
               OR MaNXB LIKE ?
        """
        cur.execute(sql, (pattern, pattern, pattern, pattern, pattern))
        rows = cur.fetchall()
        cols = [col[0] for col in cur.description]

        tree.delete(*tree.get_children())
        tree["columns"] = cols

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor=tk.W)

        for row in rows:
            vals = ["" if v is None else str(v) for v in row]
            tree.insert("", tk.END, values=vals)

    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi", f"Có lỗi khi tìm kiếm: {ex}")
    finally:
        conn.close()


def thoat_ung_dung():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát ứng dụng?"):
        root.destroy()


btn_search.config(command=tim_kiem)
btn_reload.config(command=lambda: tai_du_lieu(tree))

btn_frame_actions = tk.Frame(root, bg=BG_MAIN)
btn_frame_actions.pack(fill="x", padx=10, pady=(0, 10))

tk.Button(btn_frame_actions, text="Thêm sách", width=12,
          command=them_sach).pack(side="left", padx=3)
tk.Button(btn_frame_actions, text="Sửa sách", width=12,
          command=sua_sach).pack(side="left", padx=3)
tk.Button(btn_frame_actions, text="Xóa sách", width=12,
          command=xoa_sach).pack(side="left", padx=3)

ttk.Button(btn_frame_actions, text="Quản Lý Tác Giả",
          command=lambda: open_quan_ly_tac_gia(root, SERVER, DATABASE)).pack(side="left", padx=3)

ttk.Button(btn_frame_actions, text="Quản Lý Thể Loại",
          command=lambda: open_quan_ly_the_loai(root, SERVER, DATABASE)).pack(side="left", padx=3)

ttk.Button(btn_frame_actions, text="Quản Lý NXB",
          command=lambda: open_quan_ly_nha_xuat_ban(root, SERVER, DATABASE)).pack(side="left", padx=3)

tk.Button(btn_frame_actions, text="Thoát", width=12,
          command=thoat_ung_dung).pack(side="right", padx=3)

tai_du_lieu(tree)

root.mainloop()