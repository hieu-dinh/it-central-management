from extensions import db
from datetime import date
from flask_login import UserMixin

class AdminUser(UserMixin, db.Model):
    __tablename__ = 'admin_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

class Dept(db.Model):
    __tablename__ = 'dept'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    color_code = db.Column(db.String(7), nullable=False) # VD: #ff0000
    
    # Quan hệ 1-Nhiều với Employee
    employees = db.relationship('Employee', backref='dept', lazy=True)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150), nullable=False)
    nationality = db.Column(db.String(2), nullable=False) # 'vn', 'kr', 'in'
    dept_id = db.Column(db.Integer, db.ForeignKey('dept.id'), nullable=False)
    
    # Quan hệ 1-Nhiều với Assignment
    assignments = db.relationship('Assignment', backref='employee', lazy=True)

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), unique=True, nullable=False)
    rent_startdate = db.Column(db.Date, nullable=False)
    rent_expired = db.Column(db.Date, nullable=False)
    model = db.Column(db.String(100), nullable=False)
    brandname = db.Column(db.String(100), nullable=False)
    cpu = db.Column(db.String(100))
    ram = db.Column(db.String(50))
    disk = db.Column(db.String(50))
    status = db.Column(db.String(50), nullable=False, default="Active")
    comment = db.Column(db.Text)
    
    # Quan hệ 1-Nhiều với Assignment
    assignments = db.relationship('Assignment', backref='device', lazy=True)

class Assignment(db.Model):
    __tablename__ = 'assignment'
    id = db.Column(db.Integer, primary_key=True)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True) # Bằng NULL nghĩa là đang còn giữ máy
