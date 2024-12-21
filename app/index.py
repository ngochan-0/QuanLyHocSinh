from app import app, dao, db
from flask import render_template, request, redirect, session, jsonify
import dao
from flask_login import login_user, current_user, logout_user
from datetime import datetime
import hashlib
from app.model import Test, MonHoc, HocKi, Lop, HocSinh, UserRoleEnum


@app.route('/', methods=['get'])
def home():
    return render_template('home.html')


@app.route('/nhanvien')
def nhanvien():
    return render_template('nhanvien.html')


@app.route('/giaovien')
def giaovien():
    return render_template('giaovien.html')


@app.route('/tiepnhan')
def tiepnhan():
    return render_template('tiepnhan.html')


@app.route('/dieuchinhlop')
def dieuchinhlop():
    return render_template('dieuchinhlop.html')


@app.route("/nhapdiem")
def nhapdiem():
    return render_template('nhapdiem.html', lops=dao.get_Lop(), MonHocs=dao.get_MonHoc(), HocKis=dao.get_HocKi())


@app.route("/xuatdiem")
def xuatdiem():
    return render_template('xuatdiem.html', lops=dao.get_Lop(), HocKis=dao.get_HocKi())


@app.route('/login', methods=['post', 'get'])
def signin():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        if role:
            if role.__eq__('GIAOVIEN'):
                role = UserRoleEnum.TEACHER
                u = dao.check_login(username=username, password=password, role=role)
                login_user(u)
                return redirect('/')
            else:
                if role.__eq__('ADMIN'):
                    role = UserRoleEnum.ADMIN
                    u = dao.check_login(username=username, password=password, role=role)
                    login_user(u)
                    return redirect('/')
                else:
                    role = UserRoleEnum.STAFF
                    u = dao.check_login(username=username, password=password, role=role)
                    login_user(u)
                    return redirect('/nhanvien')
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect('/login')


@app.route('/api/luudiem', methods=['post'])
def LuuDiem():
    stu = request.json.get('scores')
    monHoc_id = request.json.get('MonHoc.id')
    hocKi_id = request.json.get('HocKi.id')
    lop_id = request.json.get('Lop.id')
    num_row_15m = len(session['num_test']['num_row_15m'])
    num_row_45m = len(session['num_test']['num_row_45m'])
    HocSinh = dao.get_student_by_class(session['num_test']['lop_id'])

    # Validate input scores
    for i in range(len(stu)):
        for j in range(num_row_15m + num_row_45m + 1):
            if not stu[i][j]:
                return jsonify({'content': 'Có học sinh chưa nhập điểm. Vui lòng kiểm tra lại!'})
            elif float(stu[i][j]) > 10 or float(stu[i][j]) < 0:
                return jsonify({'content': 'Điểm không hợp lệ. Vui lòng kiểm tra lại!'})

    # Delete existing test records
    for s in HocSinh:
        tests = Test.query.filter(Test.hs_id == s.id, Test.monHoc_id == monHoc_id, Test.hocKi_id == hocKi_id).all()
        for t in tests:
            db.session.delete(t)
            db.session.commit()

    # Insert new test records
    for i in range(len(stu)):
        for j in range(num_row_15m + num_row_45m + 1):
            type = ''
            if j < num_row_15m:
                type = '15 phút'
            elif j < (num_row_15m + num_row_45m):
                type = '1 tiết'
            else:
                type = 'Cuối kỳ'
            test = Test(type=type, score=round(float(stu[i][j]), 1), hs_id=HocSinh[i].id,
                        monHoc_id=monHoc_id, hocKi_id=hocKi_id)
            db.session.add(test)
            db.session.commit()

    return jsonify({'content': 'Lưu thành công'})


@app.route('/api/XuatDiem', methods=['post'])
def XuatDiem():
    lop_id = request.json.get('Lop.id')
    hocKi_id = request.json.get('HocKi.id')
    semester_1 = dao.calc_semester_score_average(lop_id=lop_id, hocKi_id=hocKi_id)
    semester_2 = dao.calc_semester_score_average(lop_id=lop_id, hocKi_id=int(hocKi_id) + 1)
    schoolyear = ''
    if hocKi_id == '1':
        schoolyear = 'Năm học 2020-2021'
    elif hocKi_id == '3':
        schoolyear = 'Năm học 2021-2022'
    elif hocKi_id == '5':
        schoolyear = 'Năm học 2022-2023'
    elif hocKi_id == '7':
        schoolyear = 'Năm học 2023-2024'
    result = {}
    result[0] = {
        'quantity': len(semester_1),
        'class': dao.get_class_by_id(lop_id).tenLop,
        'schoolyear': schoolyear
    }
    for i in range(len(semester_1)):
        result[i + 1] = {
            'tenHS': dao.get_student_by_id(semester_1[i]['hs_id']).name,
            'semester_1': semester_1[i]['diemm'],
            'semester_2': semester_2[i]['diemm']
        }

    return result


@app.route('/api/timkiemlop', methods=['post'])
def timkiemlop():
    lop_id = request.json.get('timkiemlop')
    students = dao.get_student_by_class(lop_id)
    stu = {}

    stu[0] = {
        "tenLop": students[0].Lop.tenLop,
        "num_row_15m": request.json.get('num_row_15m'),
        "num_row_45m": request.json.get('num_row_45m'),
        "quantity": len(students)
    }

    for i in range(1, len(students) + 1):
        stu[i] = {
            "id": students[i - 1].id,
            "name": students[i - 1].tenHs
        }

    session['num_test'] = {
        "num_row_15m": request.json.get('num_row_15m'),
        "num_row_45m": request.json.get('num_row_45m'),
        "lop_id": lop_id
    }

    return stu


@app.route('/api/Xuatdiem', methods=['post'])
def Xuatdiem():
    lop_id = request.json.get('lop_id')
    hocKi_id = request.json.get('hocKi_id')
    semester_1 = dao.calc_semester_score_average(lop_id=lop_id, hocKi_id=hocKi_id)
    semester_2 = dao.calc_semester_score_average(lop_id=lop_id, hocKi_id=int(hocKi_id) + 1)
    schoolyear = ''
    if hocKi_id == '1':
        schoolyear = 'Năm học 2020-2021'
    elif hocKi_id == '3':
        schoolyear = 'Năm học 2021-2022'
    elif hocKi_id == '5':
        schoolyear = 'Năm học 2022-2023'
    elif hocKi_id == '7':
        schoolyear = 'Năm học 2023-2024'
    result = {}
    result[0] = {
        'quantity': len(semester_1),
        'class': dao.get_class_by_id(lop_id).tenLop,
        'schoolyear': schoolyear
    }
    for i in range(len(semester_1)):
        result[i + 1] = {
            'tennHS': dao.get_student_by_id(semester_1[i]['hs_id']).name,
            'semester_1': semester_1[i]['diemm'],
            'semester_2': semester_2[i]['diemm']
        }

    return result


@app.route("/Themhocsinh", methods=['POST'])
def Themhocsinh():
    err_msg = ''
    tenHs = request.form.get('tenHs')
    gioiTinh = request.form.get('gioiTinh')
    ngaysinh = request.form.get('ngaysinh')


    diaChi = str(request.form.get('diaChi'))
    phone = request.form.get('phone')
    email = request.form.get('email')
    khoi = request.form.get('khoi')
    substring = email[(len(email) - 10):]
    if len(phone) != 10:
        err_msg = 'Số điện thoại sai. Vui lòng nhập lại!'
        return render_template('tiepnhan.html', err_msg=err_msg)
    if not substring.__eq__('@gmail.com'):
        err_msg = 'Email sai. Vui lòng nhập lại!'
        return render_template('tiepnhan.html', err_msg=err_msg)
    try:
        birthdate = datetime.strptime(ngaysinh, '%Y-%m-%d')
    except:
        err_msg = 'Bạn chưa nhập ngày sinh. Vui lòng thử lại!'
        return render_template('tiepnhan.html', err_msg=err_msg)
    if (app.config['nambatdau'] - birthdate.year) < app.config['mintuoi'] or (
            app.config['nambatdau'] - birthdate.year) > app.config['maxtuoi']:
        err_msg = 'Ngày sinh không hợp lệ. Vui lòng thử lại!'
        return render_template('tiepnhan.html', err_msg=err_msg)

    student = HocSinh(tenHs=tenHs, gioiTinh=gioiTinh, ngaysinh=ngaysinh, diaChi=diaChi, phone=phone,
              email=email, khoi_id=khoi)
    db.session.add(student)
    db.session.commit()
    err_msg = 'Lưu thành công'
    return render_template('tiepnhan.html', err_msg=err_msg)

if __name__ == '__main__':
    app.run(debug=True)
