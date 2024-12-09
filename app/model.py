from app import app, db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Date

class User(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=True)
    sex = Column(Boolean)
    email = Column(String(50), nullable=True, unique=True)
    phone = Column(String(12), nullable=True, unique=True)
    password = Column(String(50), nullable=True)
    username = Column(String(150), nullable=True, unique=True)

class GiaoVien(db.Model):
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    boMon = Column(String(50), nullable=True)


class HocSinh(db.Model):
    maHs = Column(Integer, primary_key=True, autoincrement=True)
    tenHs = Column(String(50), nullable=True)
    ngaysinh = Column(Date, nullable=True)
    gioiTinh = Column(Boolean)
    email = Column(String(50), nullable=True, unique=True)
    phone = Column(String(12), nullable=True, unique=True)
    diaChi = Column(String(255))


class Lop(db.Model):
    maLop = Column(Integer, primary_key=True, autoincrement=True)
    tenLop = Column(String(50), nullable=True)
    siSo = Column(Integer)

class HocSinhLop(db.Model):
    maHs_id = Column(Integer, ForeignKey(HocSinh.maHs), primary_key=True)
    maLop_id = Column(Integer, ForeignKey(Lop.maLop), primary_key=True)



if __name__ == '__main__':
    with app.app_context():
        db.drop_all()
        db.create_all()
