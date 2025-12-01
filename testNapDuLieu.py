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
        # Chuỗi kết nối sử dụng SQL Server Authentication (Phổ biến)
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

    # 1. Xóa dữ liệu cũ trong Treeview
    for item in tree.get_children():
        tree.delete(item)

    # 2. Thực hiện truy vấn
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM SACH")
        rows = cursor.fetchall()
        # Lấy tên cột từ cursor.description
        cols = [col[0] for col in cursor.description]

        # Cấu hình Treeview: đặt columns động và headings
        tree.delete(*tree.get_children())  # xóa rows cũ
        tree['columns'] = cols
        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor=tk.W)

        # Chèn dữ liệu (chuyển None -> '' và cast sang str để tránh lỗi)
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

# Tạo Treeview (đóng vai trò như DataGridview)
 #Định nghĩa các cột cho Treeview
cot = ("MaSach", "TenSach", "GiaBan", "SoLuongTon","MaTheLoai","MaTacGia","MaNXB")
tree = ttk.Treeview(root, columns=cot, show='headings') # show='headings' để ẩn cột mặc định đầu tiên

 #Cấu hình tiêu đề và độ rộng của từng cột
# tree.heading("MaSach", text="Mã Sách")
# tree.column("MaSach", width=80, anchor=tk.E)
# tree.heading("TenSach", text="Tên Sách")
# tree.column("TenSach", width=350, anchor=tk.E)
# tree.heading("GiaBan", text="Giá Bán")
# tree.column("GiaBan", width=120, anchor=tk.E)
# tree.heading("SoLuongTon", text="Tồn Kho")
# tree.column("SoLuongTon", width=80, anchor=tk.E)
# tree.heading("MaTheLoai", text="Mã Thể Loại")
# tree.column("MaTheLoai", width=100, anchor=tk.E)
# tree.heading("MaTacGia", text="Mã Tác Giả") 
# tree.column("MaTacGia", width=100, anchor=tk.E)
# tree.heading("MaNXB", text="Mã Nhà Xuất Bản")
# tree.column("MaNXB", width=100, anchor=tk.E)

tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

def them_sach():
    win = tk.Toplevel(root)
    win.title("Thêm Sách")
    win.transient(root)
    win.grab_set()

    labels = ["MaSach", "TenSach", "GiaBan", "SoLuongTon", "MaTheLoai", "MaTacGia", "MaNXB","NamXuatBan"]
    entries = {}

    for i, lbl in enumerate(labels):
        tk.Label(win, text=lbl).grid(row=i, column=0, padx=6, pady=4, sticky='e')
        e = tk.Entry(win, width=40)
        e.grid(row=i, column=1, padx=6, pady=4, sticky='w')
        entries[lbl] = e

    def submit():
        vals = [entries[col].get().strip() for col in labels]
        if not vals[0]:
            messagebox.showwarning("Thiếu dữ liệu", "Mã sách không được để trống")
            return
        # Chuỗi chèn động an toàn (parameterized)
        cols_sql = ",".join(labels)
        placeholders = ",".join(["?"] * len(labels))
        sql = f"INSERT INTO SACH ({cols_sql}) VALUES ({placeholders})"
        conn = ket_noi_db()
        if conn is None:
            return
        try:
            cur = conn.cursor()
            cur.execute(sql, vals)
            conn.commit()
            messagebox.showinfo("Thành công", "Đã thêm sách")
            win.destroy()
            tai_du_lieu(tree)  # refresh
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể thêm: {ex}")
        finally:
            conn.close()

    btn_frame = tk.Frame(win)
    btn_frame.grid(row=len(labels), column=0, columnspan=2, pady=8)
    tk.Button(btn_frame, text="Thêm", command=submit).pack(side='left', padx=6)
    tk.Button(btn_frame, text="Hủy", command=win.destroy).pack(side='left', padx=6)

def sua_sach():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 sách để sửa")
        return
    if len(sel) > 1:
        messagebox.showwarning("Chọn 1 bản ghi", "Vui lòng chỉ chọn một sách để sửa")
        return

    item = sel[0]
    vals = tree.item(item, 'values')
    cols = list(tree['columns']) if tree['columns'] else list(cot)
    # tạo cửa sổ sửa
    win = tk.Toplevel(root)
    win.title("Sửa Sách")
    win.transient(root)
    win.grab_set()

    entries = {}
    for i, col in enumerate(cols):
        tk.Label(win, text=col).grid(row=i, column=0, padx=6, pady=4, sticky='e')
        e = tk.Entry(win, width=40)
        e.grid(row=i, column=1, padx=6, pady=4, sticky='w')
        # điền giá trị hiện có (nếu có)
        try:
            e.insert(0, "" if vals[i] is None else str(vals[i]))
        except Exception:
            pass
        entries[col] = e

    original_ma = vals[0] if vals else None

    def submit_edit():
        new_vals = [entries[c].get().strip() for c in cols]
        if not new_vals[0]:
            messagebox.showwarning("Thiếu dữ liệu", "Mã sách không được để trống")
            return

        # Tạo câu lệnh UPDATE (gồm tất cả cột) và WHERE theo MaSach cũ
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
            messagebox.showinfo("Thành công", "Đã cập nhật sách")
            win.destroy()
            tai_du_lieu(tree)
        except pyodbc.Error as ex:
            messagebox.showerror("Lỗi", f"Không thể cập nhật: {ex}")
        finally:
            conn.close()

    btn_frame = tk.Frame(win)
    btn_frame.grid(row=len(cols), column=0, columnspan=2, pady=8)
    tk.Button(btn_frame, text="Lưu", command=submit_edit).pack(side='left', padx=6)
    tk.Button(btn_frame, text="Hủy", command=win.destroy).pack(side='left', padx=6)


def xoa_sach():
    sel = tree.selection()
    if not sel:
        messagebox.showwarning("Chưa chọn", "Vui lòng chọn 1 hoặc nhiều sách để xóa")
        return

    # Lấy MaSach từ các hàng được chọn
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

def tim_kiem():
    """Tìm sách theo chuỗi nhập vào (tim theo MaSach, TenSach, MaTacGia, MaTheLoai, MaNXB)."""
    q = entry_search.get().strip()
    conn = ket_noi_db()
    if conn is None:
        return
    # nếu ô trống thì tải lại toàn bộ
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

        # cập nhật tree
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

def thoat_ung_dung():
    if messagebox.askyesno("Xác nhận", "Bạn có chắc muốn thoát ứng dụng?"):
        root.destroy()

btn_frame_main = tk.Frame(root)
btn_frame_main.pack(fill='x', padx=10, pady=(0,10))

search_frame = tk.Frame(btn_frame_main)
search_frame.pack(side='left', padx=(0,8))
entry_search = tk.Entry(search_frame, width=28)
entry_search.pack(side='left', padx=(0,6))
btn_search = tk.Button(search_frame, text="Tìm", command=tim_kiem)
btn_search.pack(side='left')

# Nút gọi form
btn_frame_main = tk.Frame(root)
btn_frame_main.pack(fill='x', padx=10, pady=(0,10))
tk.Button(btn_frame_main, text="Thêm sách", command=them_sach).pack(side='left')
tk.Button(btn_frame_main, text="Xóa sách", command=xoa_sach).pack(side='left', padx=6)
tk.Button(btn_frame_main, text="Thoát", command=thoat_ung_dung).pack(side='right')
tk.Button(btn_frame_main, text="Sửa sách", command=sua_sach).pack(side='left', padx=6)
# Tải dữ liệu lần đầu khi ứng dụng khởi động (tùy chọn)
tai_du_lieu(tree)



root.mainloop()