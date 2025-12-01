use QLBS;
-- Bảng 1: THỂ LOẠI
go
CREATE TABLE THELOAI (
    MaTheLoai INT PRIMARY KEY,
    TenTheLoai NVARCHAR(100) NOT NULL
);
go
-- Bảng 2: TÁC GIẢ
CREATE TABLE TACGIA (
    MaTacGia INT PRIMARY KEY,
    TenTacGia NVARCHAR(150) NOT NULL,
    DiaChi NVARCHAR(255),
    DienThoai NVARCHAR(20)
);
go
-- Bảng 3: NHÀ XUẤT BẢN
CREATE TABLE NXB (
    MaNXB INT PRIMARY KEY,
    TenNXB NVARCHAR(150) NOT NULL,
    DiaChi NVARCHAR(255),
    DienThoai NVARCHAR(20)
);
go
-- Bảng 4: KHÁCH HÀNG (Tùy chọn)
CREATE TABLE KHACHHANG (
    MaKhachHang INT PRIMARY KEY,
    HoTenKH NVARCHAR(150) NOT NULL,
    DiaChi NVARCHAR(255),
    DienThoai NVARCHAR(20) UNIQUE
);
go
-- Bảng 5: SÁCH (Liên kết với TACGIA, THELOAI, NXB)
CREATE TABLE SACH (
    MaSach INT PRIMARY KEY,
    TenSach NVARCHAR(255) NOT NULL,
    MaTacGia INT,
    MaTheLoai INT,
    MaNXB INT,
    GiaBan DECIMAL(10, 2) NOT NULL CHECK (GiaBan >= 0),
    SoLuongTon INT NOT NULL CHECK (SoLuongTon >= 0),
    NamXuatBan INT,

    -- Thiết lập Khóa ngoại
    FOREIGN KEY (MaTacGia) REFERENCES TACGIA(MaTacGia),
    FOREIGN KEY (MaTheLoai) REFERENCES THELOAI(MaTheLoai),
    FOREIGN KEY (MaNXB) REFERENCES NXB(MaNXB)
);
go
-- Bảng 6: HÓA ĐƠN
CREATE TABLE HOADON (
    MaHD INT PRIMARY KEY,
    MaKhachHang INT,
    NgayBan DATE NOT NULL,
    TongTien DECIMAL(12, 2) NOT NULL CHECK (TongTien >= 0),

    -- Thiết lập Khóa ngoại
    FOREIGN KEY (MaKhachHang) REFERENCES KHACHHANG(MaKhachHang)
);
go
-- Bảng 7: CHI TIẾT HÓA ĐƠN (Khóa tổng hợp từ MaHD và MaSach)
CREATE TABLE CHITIETHOADON (
    MaHD INT,
    MaSach INT,
    SoLuong INT NOT NULL CHECK (SoLuong > 0),
    DonGia DECIMAL(10, 2) NOT NULL CHECK (DonGia >= 0),
    
    -- Thiết lập Khóa chính tổng hợp
    PRIMARY KEY (MaHD, MaSach), 
    
    -- Thiết lập Khóa ngoại
    FOREIGN KEY (MaHD) REFERENCES HOADON(MaHD),
    FOREIGN KEY (MaSach) REFERENCES SACH(MaSach)
);
use QLBS
go

go
INSERT INTO THELOAI (MaTheLoai, TenTheLoai) VALUES
(1, N'Tiểu thuyết'),
(2, N'Khoa học viễn tưởng'),
(3, N'Sách kinh doanh');
go
INSERT INTO TACGIA (MaTacGia, TenTacGia, DiaChi, DienThoai) VALUES
(101, N'Nguyễn Nhật Ánh', N'Hồ Chí Minh', N'0901111111'),
(102, N'Yuval Noah Harari', N'Israel', N'0902222222'),
(103, N'James Clear', N'New York', N'0903333333'),
(104, N'Haruki Murakami', N'Tokyo', N'0904444444');
go
INSERT INTO NXB (MaNXB, TenNXB, DiaChi, DienThoai) VALUES
(201, N'NXB Trẻ', N'Hà Nội', N'0241234567'),
(202, N'NXB Thế Giới', N'Hồ Chí Minh', N'0289876543');
go
INSERT INTO KHACHHANG (MaKhachHang, HoTenKH, DiaChi, DienThoai) VALUES
(301, N'Trần Văn An', N'Quận 1, HCM', N'0981112223'),
(302, N'Lê Thị Bình', N'Quận Ba Đình, HN', N'0984445556');
go
/*delete from SACH
delete from TACGIA
delete from THELOAI
delete from NXB
delete from KHACHHANG
delete from HOADON
delete from CHITIETHOADON*/
go
INSERT INTO SACH (MaSach, TenSach, MaTacGia, MaTheLoai, MaNXB, GiaBan, SoLuongTon, NamXuatBan) VALUES
-- Tiểu thuyết (MaTheLoai = 1)
(1, N'Tôi Thấy Hoa Vàng Trên Cỏ Xanh', 101, 1, 201, 120000.00, 50, 2010),
(2, N'Rừng Na Uy', 104, 1, 201, 150000.00, 35, 1987),
(3, N'Kafka Trên Bờ Biển', 104, 1, 201, 195000.00, 20, 2002),
(4, N'Mắt Biếc', 101, 1, 201, 110000.00, 45, 2015),
-- Khoa học viễn tưởng (MaTheLoai = 2)
(5, N'Sapiens: Lược Sử Loài Người', 102, 2, 202, 250000.00, 60, 2011),
(6, N'Homo Deus: Lược Sử Tương Lai', 102, 2, 202, 280000.00, 30, 2015),
(7, N'21 Bài Học cho Thế Kỷ 21', 102, 2, 202, 230000.00, 40, 2018),
-- Sách kinh doanh (MaTheLoai = 3)
(8, N'Atomic Habits', 103, 3, 201, 180000.00, 70, 2018),
(9, N'The Lean Startup', 103, 3, 202, 160000.00, 25, 2011),
(10, N'Rich Dad Poor Dad', 103, 3, 201, 140000.00, 55, 1997);
go
INSERT INTO HOADON (MaHD, MaKhachHang, NgayBan, TongTien) VALUES
(5001, 301, '2025-11-20', 610000.00);
go
INSERT INTO CHITIETHOADON (MaHD, MaSach, SoLuong, DonGia) VALUES
(5001, 4, 1, 110000.00),   -- Mắt Biếc
(5001, 8, 2, 180000.00),   -- Atomic Habits
(5001, 10, 1, 140000.00);  -- Rich Dad Poor Dad

go
SELECT * FROM SACH;