from flask import Flask, render_template, jsonify, request, redirect, url_for
from extensions import db
import os
import models # Dể Flask biết được các Models trước khi init DB
from datetime import date
import calendar

from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash

app = Flask(__name__)
# Thiết lập secret_key để dùng session trong Flask-Login
app.config['SECRET_KEY'] = 'it-central-management-secret-key-12345'
# Cấu hình SQLite file nằm tại thư mục gốc của project
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    from models import AdminUser
    return AdminUser.query.get(int(user_id))

with app.app_context():
    db.create_all()

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/timeline')
def api_timeline():
    # Lấy parameter từ URL, mặc định là tháng và năm hiện tại
    year = request.args.get('year', default=date.today().year, type=int)
    month = request.args.get('month', default=date.today().month, type=int)
    
    # Tính số ngày trong tháng được chọn
    _, days_in_month = calendar.monthrange(year, month)
    
    # Xác định ngày bắt đầu và kết thúc của tháng
    month_start = date(year, month, 1)
    month_end = date(year, month, days_in_month)
    
    # Lấy toàn bộ thiết bị
    devices = models.Device.query.all()
    devices_data = []
    
    for device in devices:
        assignments_data = []
        for assign in device.assignments:
            # Điều kiện Overlap: 
            # - Assignment bắt đầu TRƯỚC VÀ BẰNG ngày cuối tháng
            # - Assignment kết thúc SAU VÀ BẰNG ngày đầu tháng (Hoặc chưa kết thúc = None)
            if assign.start_date <= month_end and (assign.end_date is None or assign.end_date >= month_start):
                assignments_data.append({
                    "id": assign.id,
                    "start_date": assign.start_date.isoformat(),
                    "end_date": assign.end_date.isoformat() if assign.end_date else None,
                    "employee": {
                        "name": assign.employee.full_name,
                        "nationality": assign.employee.nationality,
                        "deptName": assign.employee.dept.name,
                        "colorCode": assign.employee.dept.color_code
                    }
                })
        
        devices_data.append({
            "id": device.id,
            "serial_number": device.serial_number,
            "rent_startdate": device.rent_startdate.isoformat() if device.rent_startdate else None,
            "rent_expired": device.rent_expired.isoformat() if device.rent_expired else None,
            "model": device.model,
            "brandname": device.brandname,
            "cpu": device.cpu,
            "ram": device.ram,
            "disk": device.disk,
            "status": device.status,
            "assignments": assignments_data
        })
        
    return jsonify({
        "year": year,
        "month": month,
        "days_in_month": days_in_month,
        "devices": devices_data
    })

# --- ADMIN ROUTES ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        from models import AdminUser
        user = AdminUser.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
            
        return render_template('login.html', error='Invalid credentials')
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    # Thống kê cơ bản
    from models import Device, Employee, Assignment
    total_devices = Device.query.count()
    in_use_devices = Device.query.filter_by(status='In-Use').count()
    total_employees = Employee.query.count()
    
    return render_template('admin_layout.html', 
                          total_devices=total_devices,
                          in_use_devices=in_use_devices,
                          total_employees=total_employees)

# --- Quản lý Thiết Bị (CRUD DEVICES) ---

@app.route('/admin/devices')
@login_required
def admin_devices():
    from models import Device
    devices = Device.query.order_by(Device.rent_startdate.asc()).all()
    return render_template('admin_devices.html', devices=devices)

@app.route('/admin/device/create', methods=['GET', 'POST'])
@app.route('/admin/device/edit/<int:device_id>', methods=['GET', 'POST'])
@login_required
def admin_device_form(device_id=None):
    from models import Device
    from datetime import datetime
    
    device = Device.query.get_or_404(device_id) if device_id else None
    
    if request.method == 'POST':
        serial_number = request.form.get('serial_number')
        model = request.form.get('model')
        brandname = request.form.get('brandname')
        cpu = request.form.get('cpu')
        ram = request.form.get('ram')
        disk = request.form.get('disk')
        status = request.form.get('status')
        comment = request.form.get('comment')
        
        # Xử lý ngày tháng
        raw_start = request.form.get('rent_startdate')
        raw_exp = request.form.get('rent_expired')
        start_date = datetime.strptime(raw_start, '%Y-%m-%d').date() if raw_start else date.today()
        exp_date = datetime.strptime(raw_exp, '%Y-%m-%d').date() if raw_exp else date.today()

        if device: # Update
            device.serial_number = serial_number
            device.model = model
            device.brandname = brandname
            device.cpu = cpu
            device.ram = ram
            device.disk = disk
            device.status = status
            device.comment = comment
            device.rent_startdate = start_date
            device.rent_expired = exp_date
        else: # Create
            new_device = Device(
                serial_number=serial_number, model=model, brandname=brandname,
                cpu=cpu, ram=ram, disk=disk, status=status, comment=comment,
                rent_startdate=start_date, rent_expired=exp_date
            )
            db.session.add(new_device)
            
        db.session.commit()
        return redirect(url_for('admin_devices'))
        
    return render_template('admin_device_form.html', device=device)

@app.route('/admin/device/delete/<int:device_id>', methods=['POST'])
@login_required
def admin_device_delete(device_id):
    from models import Device, Assignment
    device = Device.query.get_or_404(device_id)
    # Cần xóa các Assignment liên quan trước (hoặc có thể setup cascade)
    Assignment.query.filter_by(device_id=device.id).delete()
    db.session.delete(device)
    db.session.commit()
    return redirect(url_for('admin_devices'))

# --- Quản lý Nhân sự (CRUD EMPLOYEES) ---

@app.route('/admin/employees')
@login_required
def admin_employees():
    from models import Employee
    employees = Employee.query.order_by(Employee.id.desc()).all()
    return render_template('admin_employees.html', employees=employees)

@app.route('/admin/employee/create', methods=['GET', 'POST'])
@app.route('/admin/employee/edit/<int:employee_id>', methods=['GET', 'POST'])
@login_required
def admin_employee_form(employee_id=None):
    from models import Employee, Dept
    employee = Employee.query.get_or_404(employee_id) if employee_id else None
    departments = Dept.query.all()
    
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        nationality = request.form.get('nationality')
        dept_id = request.form.get('dept_id')
        
        if employee: # Update
            employee.full_name = full_name
            employee.nationality = nationality
            employee.dept_id = dept_id
        else: # Create
            new_employee = Employee(
                full_name=full_name,
                nationality=nationality,
                dept_id=dept_id
            )
            db.session.add(new_employee)
            
        db.session.commit()
        return redirect(url_for('admin_employees'))
        
    return render_template('admin_employee_form.html', employee=employee, departments=departments)

@app.route('/admin/employee/delete/<int:employee_id>', methods=['POST'])
@login_required
def admin_employee_delete(employee_id):
    from models import Employee, Assignment
    employee = Employee.query.get_or_404(employee_id)
    # Xóa các assignment liên quan tới employee này
    Assignment.query.filter_by(employee_id=employee.id).delete()
    db.session.delete(employee)
    db.session.commit()
    return redirect(url_for('admin_employees'))

# --- Quản lý Cấp phát (ASSIGNMENTS) ---

@app.route('/admin/assignments')
@login_required
def admin_assignments():
    from models import Assignment
    # List tất cả lịch sử, mới nhất lên đầu
    assignments = Assignment.query.order_by(Assignment.start_date.desc(), Assignment.id.desc()).all()
    return render_template('admin_assignments.html', assignments=assignments)

@app.route('/admin/assignment/create', methods=['GET', 'POST'])
@login_required
def admin_assignment_create():
    from models import Assignment, Device, Employee
    from datetime import date, datetime
    
    # Chỉ cho phép cấp phát các máy đang trong kho (Standby)
    available_devices = Device.query.filter_by(status='Standby').all()
    employees = Employee.query.all()
    
    if request.method == 'POST':
        device_id = request.form.get('device_id')
        employee_id = request.form.get('employee_id')
        raw_start = request.form.get('start_date')
        
        start_date = datetime.strptime(raw_start, '%Y-%m-%d').date() if raw_start else date.today()
        
        # 1. Tạo Assignment mới lưu vào DB
        new_assignment = Assignment(
            device_id=device_id,
            employee_id=employee_id,
            start_date=start_date,
            end_date=None # Chưa có ngày trả
        )
        db.session.add(new_assignment)
        
        # 2. Cập nhật Status của Device thành "In-Use"
        device = Device.query.get(device_id)
        if device:
            device.status = 'In-Use'
            
        db.session.commit()
        return redirect(url_for('admin_assignments'))
        
    return render_template('admin_assignment_form.html', devices=available_devices, employees=employees)

@app.route('/admin/assignment/return/<int:assignment_id>', methods=['POST'])
@login_required
def admin_assignment_return(assignment_id):
    from models import Assignment, Device
    from datetime import date
    
    assignment = Assignment.query.get_or_404(assignment_id)
    
    # 1. Set End Date là hôm nay
    assignment.end_date = date.today()
    
    # 2. Trả Device về trạng thái kho (Standby)
    if assignment.device:
        assignment.device.status = 'Standby'
        
    db.session.commit()
    return redirect(url_for('admin_assignments'))

@app.route('/admin/assignment/delete/<int:assignment_id>', methods=['POST'])
@login_required
def admin_assignment_delete(assignment_id):
    from models import Assignment
    assignment = Assignment.query.get_or_404(assignment_id)
    db.session.delete(assignment)
    db.session.commit()
    return redirect(url_for('admin_assignments'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
