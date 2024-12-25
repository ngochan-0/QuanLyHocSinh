from app.model import User, HocSinh
from app import login

def check_login(username, password, role):
    return User.query.filter(User.tenDangNhap.__eq__(username),
                             User.matKhau_u.__eq__(password),
                             User.user_role.__eq__(role)).first()

@login.user_loader
def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_student_by_class(lop_id):
    return HocSinh.query.filter(HocSinh.lop_id.__eq__(lop_id)).all()


def get_student():
    return HocSinh.query.all()


def get_student_by_name(name):
    return HocSinh.query.filter(HocSinh.name.icontains(name)).all()


def get_student_by_id(id):
    return HocSinh.query.get(id)
