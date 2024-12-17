from enum import unique

from app import app, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Date,Float
from sqlalchemy.orm import relationship
from flask_login import UserMixin

class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

class User(Base, UserMixin):
    hoTen_u = Column(String(50), nullable=False)
    gioiTinh_u = Column(Boolean)
    email_u = Column(String(50), nullable=False, unique=True)
    sdt_u = Column(String(12), nullable=False)
    matKhau_u = Column(String(50), nullable=False)
    tenDangNhap = Column(String(150), nullable=False, unique=True)#unique giong primarykey nhung duoc phep thay doi


class GiaoVien(User):
    giaoVien_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),unique=True)
    boMon = Column(String(50), nullable=False)
    lichDay = relationship('lich_day', backref='giaovien', lazy=True)
    diem=relationship('Diem',backref='giao_vien',lazy=True)

class QuanTriVien(User):
    admin_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),unique=True)
    vaiTro = Column(String(50), nullable=False)

class NhanVienTruong(User):
    nv_id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id),unique=True)
    vaiTro = Column(String(50), nullable=False)


class HocSinh(Base):
    tenHs = Column(String(50), nullable=False)
    ngaysinh = Column(Date, nullable=False)
    gioiTinh = Column(Boolean)
    email = Column(String(50), nullable=False, unique=True)
    phone = Column(String(12),nullable=False)
    diaChi = Column(String(255),nullable=False)


class Khoi(Base):
    tenKhoi=Column(String(50),nullable=False)
    lop= relationship('lop', backref='khoi', lazy=True)

class QuyDinh(Base):
    tenQD=Column(String(50),nullable=False)
    moTa = Column(String(50), nullable=False)
    lop = relationship('lop', backref='quydinh', lazy=True)

class Lop(Base):
    tenLop = Column(String(50), nullable=False)
    siSo = Column(Integer,nullable=False)
    khoi_id=Column(Integer,ForeignKey(Khoi.id),nullable=False)
    lichDay = relationship('MonHoc', secondary='lich_day', lazy='subquery',
                                         backref='lop')
    hs_lop = relationship('HocSinh', secondary='hs_lop', lazy='subquery',
                           backref='lop')
    quydinh_id = Column(Integer, ForeignKey(QuyDinh.id), nullable=False)

class MonHoc(Base):
    tenMH=Column(String(50),nullable=False)

class Diem(Base):
    loaiDiem=Column(String(50),nullable=False)
    diem=Column(Float,nullable=False)
    hs_mh=relationship('HS_MH',backref='diem',lazy=True)
    gv_id=Column(Integer,ForeignKey(GiaoVien.giaoVien_id),nullable=False)

class HocKi(Base):
    tenHK=Column(String(50),nullable=False)
    namHoc=Column(String(50),nullable=False)
    hs_lop=relationship('hoc_sinh_lop',backref='hoc_ki',lazy=True)

HS_MH = db.Table('HS_MH',
                    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                    Column('mh_id',Integer,ForeignKey(MonHoc.id)),
                    Column('hs_id',Integer,ForeignKey(HocSinh.id)),
                    Column('diem_id',Integer,ForeignKey(Diem.id), nullable=False),)

lich_day = db.Table('lich_day',
                    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                    Column('lop_id', Integer, ForeignKey(Lop.id)),
                    Column('monHoc_id', Integer, ForeignKey(MonHoc.id)),
                    Column('giaoVien_id', Integer, ForeignKey(GiaoVien.giaoVien_id)))

hoc_sinh_lop= db.Table('hoc_sinh_lop',
                    Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
                    Column('hs_id', Integer, ForeignKey(HocSinh.id)),
                    Column('lop_id', Integer, ForeignKey(Lop.id)),
                    Column('hocKi_id', Integer, ForeignKey(HocKi.id)))

if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()

