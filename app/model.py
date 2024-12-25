import enum
import hashlib
from enum import unique

from app import app, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Date, Float, Enum
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

class UserRoleEnum(enum.Enum):
    ADMIN = 1
    STAFF = 2
    TEACHER = 3

class User(Base, UserMixin):
    hoTen_u = Column(String(50), nullable=False)
    gioiTinh_u = Column(Boolean)
    email_u = Column(String(50), nullable=False, unique=True)
    sdt_u = Column(String(12), nullable=False)
    matKhau_u = Column(String(50), nullable=False)
    tenDangNhap = Column(String(150), nullable=False, unique=True)#unique giong primarykey nhung duoc phep thay doi
    user_role = Column(Enum(UserRoleEnum))


class GiaoVien(User):
    giaoVien_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),unique=True)
    boMon = Column(String(50), nullable=False)
    lichDay = relationship('LichDay', backref='giaovien', lazy=True)
    diem=relationship('Diem',backref='giao_vien',lazy=True)
    lichDay = relationship('LichDay', backref='giaovien', lazy=True)

class QuanTriVien(User):
    admin_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),unique=True)
    vaiTro = Column(String(50), nullable=False)

class NhanVienTruong(User):
    nv_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),unique=True)
    vaiTro = Column(String(50), nullable=False)

class Khoi(Base):
    tenKhoi=Column(String(50),nullable=False)
    lop= relationship('Lop', backref='khoi', lazy=True)

class QuyDinh(Base):
    tenQD=Column(String(50),nullable=False)
    moTa = Column(String(50), nullable=False)

class Lop(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    tenLop = Column(String(50), nullable=False)
    khoi_id=Column(Integer,ForeignKey(Khoi.id),nullable=False)
    lichDay = relationship('LichDay', backref='lop', lazy=True)
    hs_lop = relationship('HocSinh', lazy=True, backref='lop')

class HocSinh(Base):
    tenHs = Column(String(50), nullable=False)
    ngaysinh = Column(Date, nullable=False)
    gioiTinh = Column(Enum('Nam', 'Nữ'), nullable=False)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(12),nullable=False)
    diaChi = Column(String(255),nullable=False)
    lop_id = Column(Integer, ForeignKey(Lop.id))


class MonHoc(Base):
    tenMH=Column(String(50),nullable=False)
    lichDay = relationship('LichDay', backref='monhoc', lazy=True)

class Diem(Base):
    loaiDiem=Column(String(50),nullable=False)
    diem=Column(Float,nullable=False)
    hs_mh=relationship('HocSinhMonHoc',backref='diem',lazy=True)
    gv_id=Column(Integer,ForeignKey(GiaoVien.giaoVien_id),nullable=False)

class HocKi(Base):
    tenHK=Column(String(50),nullable=False)
    namHoc=Column(String(50),nullable=False)
    hs_lop=relationship('HocSinhLop',backref='hoc_ki',lazy=True)

class HocSinhMonHoc(Base):
    mh_id  =  Column(Integer, ForeignKey(MonHoc.id))
    hs_id = Column(Integer, ForeignKey(HocSinh.id))
    diem_id =  Column( Integer, ForeignKey(Diem.id), nullable=False)


class LichDay(Base):
    lop_id = Column(Integer, ForeignKey(Lop.id))
    monhoc_id = Column(Integer, ForeignKey(MonHoc.id), nullable=False)
    giaovien_id = Column(Integer, ForeignKey(GiaoVien.giaoVien_id), nullable=False)


class HocSinhLop(Base):
    hs_id = Column( Integer, ForeignKey(HocSinh.id))
    lop_id = Column(Integer, ForeignKey(Lop.id))
    hocki_id = Column(Integer, ForeignKey(HocKi.id))

if __name__ == '__main__':
    with app.app_context():
        # pass
        # db.drop_all()
        # db.create_all()

        u1 = User(hoTen_u="Diem", gioiTinh_u=0, email_u="diem@gmail.com", sdt_u="093444111",
                  matKhau_u=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), tenDangNhap='diem', user_role='TEACHER')
        u2 = User(hoTen_u="Yen", gioiTinh_u=0, email_u="Yen@gmail.com", sdt_u="093412344",
                  matKhau_u=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), tenDangNhap='yen', user_role='ADMIN')
        u3 = User(hoTen_u="Duy", gioiTinh_u=1, email_u="duy@gmail.com", sdt_u="093412322",
                  matKhau_u=str(hashlib.md5('123'.strip().encode('utf-8')).hexdigest()), tenDangNhap='duy', user_role='STAFF')
        db.session.add_all( [u1, u2, u3])
        db.session.commit()

        grade1 = Khoi(tenKhoi='Grade 10')
        grade2 = Khoi(tenKhoi='Grade 11')
        grade3 = Khoi(tenKhoi='Grade 12')
        db.session.add_all([grade1, grade2, grade3])
        db.session.commit()

        c1 = Lop(tenLop='10A1', khoi_id=1)
        c2 = Lop(tenLop='10A2', khoi_id=1)
        c3 = Lop(tenLop='10A3', khoi_id=1)
        c4 = Lop(tenLop='11A1', khoi_id=2)
        c5 = Lop(tenLop='11A2', khoi_id=2)
        c6 = Lop(tenLop='11A3', khoi_id=2)
        c8 = Lop(tenLop='12A2', khoi_id=3)
        c7 = Lop(tenLop='12A1', khoi_id=3)
        c9 = Lop(tenLop='12A3', khoi_id=3)
        db.session.add_all([c1, c2, c3, c4, c5, c6, c7, c8, c9])
        db.session.commit()

        s1 = MonHoc(tenMH="Ngữ văn")
        s2 = MonHoc(tenMH="Toán")
        s3 = MonHoc(tenMH="Ngoại ngữ")
        s4 = MonHoc(tenMH="Vật lý")
        s5 = MonHoc(tenMH="Hóa học")
        s6 = MonHoc(tenMH="Sinh học")
        s7 = MonHoc(tenMH="Lịch sử")
        s8 = MonHoc(tenMH="Địa lý")
        s9 = MonHoc(tenMH="Giáo dục công dân")
        s10 = MonHoc(tenMH="Tin học")
        s11 = MonHoc(tenMH="Giáo dục quốc phòng và an ninh")
        s12 = MonHoc(tenMH="Công nghệ")
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8, s9, s10, s11, s12])
        db.session.commit()

        s1 = HocKi(tenHK="Học kỳ 1", namHoc=" năm học 2020-2021")
        s2 = HocKi(tenHK="Học kỳ 2 ", namHoc="năm học 2020-2021")
        s3 = HocKi(tenHK="Học kỳ 1  ", namHoc="năm học 2021-2022")
        s4 = HocKi(tenHK="Học kỳ 2  ", namHoc="năm học 2021-2022")
        s5 = HocKi(tenHK="Học kỳ 1  ", namHoc="năm học 2022-2023")
        s6 = HocKi(tenHK="Học kỳ 2  ", namHoc="năm học 2022-2023")
        s7 = HocKi(tenHK="Học kỳ 1 ", namHoc=" năm học 2023-2024")
        s8 = HocKi(tenHK="Học kỳ 2  ", namHoc="năm học 2023-2024")
        db.session.add_all([s1, s2, s3, s4, s5, s6, s7, s8])
        db.session.commit()
