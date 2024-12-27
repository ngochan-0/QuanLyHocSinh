from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from app import app


admin = Admin(app, name="Quản trị", template_mode="bootstrap4")
