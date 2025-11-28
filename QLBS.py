import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc # Thư viện kết nối phổ biến với SQL Server

# Thông tin kết nối SQL Server
# Thay đổi các giá trị này để phù hợp với môi trường của bạn
server = r'MSI\CANH'
database = 'QLBS'
username = 'TuanCanh'
password = '123'

def ket_noi_db():
    """Thiết lập và trả về kết nối đến SQL Server."""
    try:
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};'
            f'DATABASE={database};'
            f'UID={username};'
            f'PWD={password};'
        )
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as ex:
        sqlstate = ex.args[0]
        messagebox.showerror("Lỗi Kết Nối", f"Không thể kết nối đến SQL Server: \n{sqlstate}")
        return None

def tai_du_lieu(tree):
    """Truy vấn dữ liệu từ SQL Server và chèn vào Treeview."""
    conn = ket_noi_db()
    if conn is None:
        return

    for item in tree.get_children():
        tree.delete(item)

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SACH")
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]

        tree.delete(*tree.get_children())
        tree['columns'] = cols
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor=tk.W)

        for row in rows:
            vals = [("" if v is None else str(v)) for v in row]
            tree.insert('', tk.END, values=vals)

    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi Truy Vấn", f"Có lỗi khi tải dữ liệu: {ex}")
    finally:
        conn.close()

# --- Thiết kế Giao diện Tkinter ---
root = tk.Tk()
root.title("Quản Lý Bán Sách - Dữ liệu SQL Server")
root.geometry("900x600")

# Top: input form giống giao diện mẫu (sử dụng grid)
form_frame = tk.Frame(root, padx=8, pady=8)
form_frame.pack(fill='x')

labels_main = ["MaSach", "TenSach", "GiaBan", "SoLuongTon", "MaTheLoai", "MaTacGia", "MaNXB", "NamXuatBan"]
main_entries = {}

# Arrange inputs in two columns to resemble sample layout
for i, lbl in enumerate(labels_main):
    r = i // 2
    c = (i % 2) * 2
    tk.Label(form_frame, text=lbl).grid(row=r, column=c, sticky='e', padx=6, pady=6)
    e = tk.Entry(form_frame, width=30)
    e.grid(row=r, column=c+1, sticky='w', padx=6, pady=6)
    main_entries[lbl] = e

# Buttons row under form
btns_frame = tk.Frame(root, pady=6)
btns_frame.pack(fill='x', padx=8)

def clear_main_entries():
    for e in main_entries.values():
        e.delete(0, tk.END)

def them_sach_from_entries():
    """Thêm sách lấy dữ liệu trực tiếp từ các Entry trên form chính."""
    vals = [main_entries[col].get().strip() for col in labels_main]
    if not vals[0]:
        messagebox.showwarning("Thiếu dữ liệu", "Mã sách không được để trống")
        return

    cols_sql = ",".join(labels_main)
    placeholders = ",".join(["?"] * len(labels_main))
    sql = f"INSERT INTO SACH ({cols_sql}) VALUES ({placeholders})"

    conn = ket_noi_db()
    if conn is None:
        return
    try:
        cur = conn.cursor()
        cur.execute(sql, vals)
        conn.commit()
        messagebox.showinfo("Thành công", "Đã thêm sách")
        clear_main_entries()
        tai_du_lieu(tree)
    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi", f"Không thể thêm: {ex}")
    finally:
        conn.close()

def sua_sach_from_entries():
    """Cập nhật bản ghi theo MaSach (MaSach gốc phải tồn tại)."""
    vals = [main_entries[col].get().strip() for col in labels_main]
    if not vals[0]:
        messagebox.showwarning("Thiếu dữ liệu", "Mã sách không được để trống")
        return
    # UPDATE tất cả cột trừ dùng MaSach làm WHERE
    set_clause = ",".join([f"{c}=?" for c in labels_main])
    sql = f"UPDATE SACH SET {set_clause} WHERE MaSach = ?"
    params = vals + [vals[0]]  # WHERE MaSach = original MaSach (nếu user thay đổi mã, logic này dùng mã hiện tại)

    conn = ket_noi_db()
    if conn is None:
        return
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        messagebox.showinfo("Thành công", "Đã cập nhật sách")
        clear_main_entries()
        tai_du_lieu(tree)
    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi", f"Không thể cập nhật: {ex}")
    finally:
        conn.close()

def on_tree_select_fill_entries(event=None):
    sel = tree.selection()
    if not sel:
        return
    item = sel[0]
    vals = tree.item(item, 'values')
    if not vals:
        return
    # Nếu số cột trong tree khác labels_main, chỉ map tối thiểu
    for i, col in enumerate(labels_main):
        try:
            main_entries[col].delete(0, tk.END)
            main_entries[col].insert(0, "" if vals[i] is None else str(vals[i]))
        except Exception:
            main_entries[col].delete(0, tk.END)

tk.Button(btns_frame, text="Thêm", width=10, command=them_sach_from_entries).pack(side='left', padx=6)
tk.Button(btns_frame, text="Lưu (Cập nhật)", width=12, command=sua_sach_from_entries).pack(side='left', padx=6)
tk.Button(btns_frame, text="Sửa (lấy từ danh sách)", width=18, command=lambda: None).pack(side='left', padx=6)  # placeholder
tk.Button(btns_frame, text="Hủy", width=10, command=clear_main_entries).pack(side='left', padx=6)

# Search area and other action buttons (right side)
search_frame = tk.Frame(btns_frame)
search_frame.pack(side='right')
entry_search = tk.Entry(search_frame, width=28)
entry_search.pack(side='left', padx=(0,6))

def tim_kiem():
    """Tìm sách theo chuỗi nhập vào (MaSach, TenSach, MaTacGia, MaTheLoai, MaNXB)."""
    q = entry_search.get().strip()
    conn = ket_noi_db()
    if conn is None:
        return
    if q == "":
        tai_du_lieu(tree)
        return
    try:
        cur = conn.cursor()
        pattern = f"%{q}%"
        sql = """
            SELECT * FROM SACH
            WHERE MaSach LIKE ? OR TenSach LIKE ? OR MaTacGia LIKE ? OR MaTheLoai LIKE ? OR MaNXB LIKE ?
        """
        cur.execute(sql, (pattern, pattern, pattern, pattern, pattern))
        rows = cur.fetchall()
        cols = [col[0] for col in cur.description]

        for item in tree.get_children():
            tree.delete(item)
        tree['columns'] = cols
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor=tk.W)

        for row in rows:
            vals = [("" if v is None else str(v)) for v in row]
            tree.insert('', tk.END, values=vals)

    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi", f"Có lỗi khi tìm kiếm: {ex}")
    finally:
        conn.close()

def tim_lai():
    entry_search.delete(0, tk.END)
    tai_du_lieu(tree)

btn_search = tk.Button(search_frame, text="Tìm", width=8, command=tim_kiem)
btn_search.pack(side='left', padx=(0,6))
tk.Button(search_frame, text="Tìm lại", width=8, command=tim_lai).pack(side='left')

tk.Button(search_frame, text="Xóa", width=8, command=lambda: xoa_sach()).pack(side='left', padx=(12,0))
tk.Button(search_frame, text="Thoát", width=8, command=lambda: thoat_ung_dung()).pack(side='left', padx=(6,0))

# Treeview area
cot = ("MaSach", "TenSach", "GiaBan", "SoLuongTon","MaTheLoai","MaTacGia","MaNXB")
tree = ttk.Treeview(root, columns=cot, show='headings')
for c in cot:
    tree.heading(c, text=c)
    tree.column(c, width=120, anchor=tk.W)
tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Gắn sự kiện chọn dòng để đưa dữ liệu lên form
tree.bind("<<TreeviewSelect>>", on_tree_select_fill_entries)

def sua_sach():
    # giữ để tương thích với các phần khác (không dùng cửa sổ mới)
    on_tree_select_fill_entries()

def xoa_sach():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 hoặc nhiều sách để xóa")
        return

    masach_list = []
    for item in sel:
        vals = tree.item(item, 'values')
        if vals:
            masach_list.append(vals[0])

    if not masach_list:
        messagebox.showwarning("Lỗi", "Không thể xác định Mã sách để xóa")
        return

    if not messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa {len(masach_list)} sách?"):
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
        messagebox.showinfo("Thành công", "Đã xóa sách")
        tai_du_lieu(tree)
    except pyodbc.Error as ex:
        messagebox.showerror("Lỗi", f"Không thể xóa: {ex}")
    finally:
        conn.close()

def thoat_ung_dung():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát ứng dụng?"):
        root.destroy()

# Tải dữ liệu lần đầu khi ứng dụng khởi động
tai_du_lieu(tree)

root.mainloop()