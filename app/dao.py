from app.model import User
from app import login

def check_login(username, password, role):
    return User.query.filter(User.tenDangNhap.__eq__(username),
                             User.matKhau_u.__eq__(password),
                             User.user_role.__eq__(role)).first()


@login.user_loader
def get_user_by_id(user_id):
    return User.query.get(user_id)