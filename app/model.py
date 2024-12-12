from app import app, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Date


class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    hoTen_u = Column(String(50), nullable=True)
    gioiTinh_u = Column(Boolean)
    email_u = Column(String(50), nullable=True, unique=True)
    sdt_u = Column(String(12), nullable=True, unique=True)
    matKhau_u = Column(String(50), nullable=True)
    tenDangNhap = Column(String(150), nullable=True, unique=True)


class GiaoVien(User):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    boMon = Column(String(50), nullable=True)

class QuanTriVien(User):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    vaiTro = Column(String(50), nullable=False)

class NhanVienTruong(User):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    vaiTro = Column(String(50), nullable=False)


# class HocSinh(db.Model):
#     maHs = Column(Integer, primary_key=True, autoincrement=True)
#     tenHs = Column(String(50), nullable=True)
#     ngaysinh = Column(Date, nullable=True)
#     gioiTinh = Column(Boolean)
#     email = Column(String(50), nullable=True, unique=True)
#     phone = Column(String(12), nullable=True, unique=True)
#     diaChi = Column(String(255))
#
#
# class Lop(db.Model):
#     maLop = Column(Integer, primary_key=True, autoincrement=True)
#     tenLop = Column(String(50), nullable=True)
#     siSo = Column(Integer)
#
# class HocSinh_Lop(db.Model):
#     maHs_id = Column(Integer, ForeignKey(HocSinh.maHs), primary_key=True)
#     maLop_id = Column(Integer, ForeignKey(Lop.maLop), primary_key=True)

# class



if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

