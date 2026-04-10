from app import app, db
from models import Dept, Employee, Device, Assignment, AdminUser
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

def seed():
    with app.app_context():
        # Reset toàn bộ dữ liệu
        db.drop_all()
        db.create_all()

        # Tạo Admin mặc định
        admin = AdminUser(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()

        # Tạo dummy phòng ban (DEPT)
        dept_admin = Dept(name='ADMIN', color_code='#45B7D1') #xanh dương sáng
        dept_pink = Dept(name='PINK', color_code='#FF3EB5') #hồng cánh sen
        dept_vs = Dept(name='VS', color_code='#FF9F43') #cam sáng
        dept_walmart = Dept(name='WALMART', color_code='#FFE66D') #vàng tươi
        dept_uniqlo = Dept(name='UNIQLO', color_code='#10AC84') #xanh lục tươi
        dept_carter = Dept(name="CARTER'S",color_code='#4ECDC4') #xanh ngọc sáng
        dept_FT = Dept(name='FIT-TECH', color_code='#1DD1A1') #xanh mint rực
        dept_qa = Dept(name='QA', color_code='#6A4C93') #tím rực

        
        db.session.add_all([dept_admin, dept_pink, dept_vs, dept_walmart, dept_uniqlo, dept_carter, dept_FT, dept_qa])
        db.session.commit()

        # Tạo dummy nhân viên (EMPLOYEE)
        emp1 = Employee(full_name='Nguyễn Văn A', nationality='vn', dept_id=dept_pink.id)
        emp2 = Employee(full_name='Kim Min-su', nationality='kr', dept_id= dept_walmart.id)
        emp3 = Employee(full_name='Rahul Sharma', nationality='in', dept_id=dept_qa.id)
        emp4 = Employee(full_name='John Doe', nationality='in', dept_id=dept_carter.id)
        emp5 = Employee(full_name='Tran Thi B', nationality='vn', dept_id=dept_FT.id)
        emp6 = Employee(full_name='Hieu Dinh', nationality='vn', dept_id=dept_admin.id)
        emp7 = Employee(full_name='Man Nguyen', nationality='kr', dept_id=dept_admin.id)
        emp8 = Employee(full_name='Nguyen Thi Cam C', nationality='kr', dept_id=dept_vs.id)
        emp9 = Employee(full_name='Lee Ducksoo', nationality='kr', dept_id=dept_uniqlo.id)
        db.session.add_all([emp1, emp2, emp3, emp4, emp5, emp6, emp7, emp8, emp9])
        db.session.commit()

        # Tạo dummy thiết bị (DEVICE)
        dev1 = Device(
            serial_number='SN-MAC-001',
            rent_startdate=date(2023, 1, 1),
            rent_expired=date(2026, 1, 1),
            model='MacBook Pro 16',
            brandname='Apple',
            cpu='M2 Max',
            ram='32GB',
            disk='1TB SSD',
            status='In-Use'
        )
        dev2 = Device(
            serial_number='SN-LEN-002',
            rent_startdate=date(2024, 6, 1),
            rent_expired=date(2027, 6, 1),
            model='ThinkPad T14 Gen 4',
            brandname='Lenovo',
            cpu='Intel Core i7 13th Gen',
            ram='16GB',
            disk='512GB SSD',
            status='In-Use'
        )
        # Máy trong kho dự phòng
        dev3 = Device(
            serial_number='SN-DEL-003',
            rent_startdate=date(2025, 1, 1),
            rent_expired=date(2028, 1, 1),
            model='Dell XPS 15',
            brandname='Dell',
            cpu='Intel Core i9',
            ram='32GB',
            disk='1TB SSD',
            status='Standby'
        )
        # Máy đang hỏng
        dev4 = Device(
            serial_number='SN-HP-004',
            rent_startdate=date(2022, 1, 1),
            rent_expired=date(2025, 1, 1),
            model='HP EliteBook',
            brandname='HP',
            cpu='Intel Core i5',
            ram='16GB',
            disk='512GB SSD',
            status='Reparing'
        )
        dev5 = Device(
            serial_number='SN-HP-005',
            rent_startdate=date(2023, 3, 10),
            rent_expired=date(2026, 3, 10),
            model='HP ProBook 450',
            brandname='HP',
            cpu='Intel Core i7',
            ram='16GB',
            disk='1TB SSD',
            status='In-Use'
        )

        dev6 = Device(
            serial_number='SN-LN-006',
            rent_startdate=date(2021, 7, 5),
            rent_expired=date(2024, 7, 5),
            model='Lenovo ThinkPad X1 Carbon',
            brandname='Lenovo',
            cpu='Intel Core i5',
            ram='8GB',
            disk='256GB SSD',
            status='Standby'
        )

        dev7 = Device(
            serial_number='SN-DELL-007',
            rent_startdate=date(2022, 11, 1),
            rent_expired=date(2025, 11, 1),
            model='Dell Latitude 5420',
            brandname='Dell',
            cpu='Intel Core i7',
            ram='16GB',
            disk='512GB SSD',
            status='In-Use'
        )

        dev8 = Device(
            serial_number='SN-MS-008',
            rent_startdate=date(2023, 1, 20),
            rent_expired=date(2026, 1, 20),
            model='Microsoft Surface Laptop 4',
            brandname='Microsoft',
            cpu='Intel Core i5',
            ram='8GB',
            disk='512GB SSD',
            status='Standby'
        )

        dev9 = Device(
            serial_number='SN-HP-009',
            rent_startdate=date(2020, 6, 15),
            rent_expired=date(2023, 6, 15),
            model='HP EliteBook 840',
            brandname='HP',
            cpu='Intel Core i7',
            ram='32GB',
            disk='1TB SSD',
            status='Reparing'
        )

        dev10 = Device(
            serial_number='SN-AS-010',
            rent_startdate=date(2021, 9, 30),
            rent_expired=date(2024, 9, 30),
            model='ASUS ZenBook 14',
            brandname='ASUS',
            cpu='Intel Core i5',
            ram='16GB',
            disk='512GB SSD',
            status='In-Use'
        )

        dev11 = Device(
            serial_number='SN-LN-011',
            rent_startdate=date(2022, 4, 18),
            rent_expired=date(2025, 4, 18),
            model='Lenovo ThinkBook 15',
            brandname='Lenovo',
            cpu='Intel Core i3',
            ram='8GB',
            disk='256GB SSD',
            status='Standby'
        )

        dev12 = Device(
            serial_number='SN-DELL-012',
            rent_startdate=date(2023, 8, 1),
            rent_expired=date(2026, 8, 1),
            model='Dell XPS 13',
            brandname='Dell',
            cpu='Intel Core i7',
            ram='16GB',
            disk='1TB SSD',
            status='In-Use'
        )

        dev13 = Device(
            serial_number='SN-MS-013',
            rent_startdate=date(2020, 2, 25),
            rent_expired=date(2023, 2, 25),
            model='Microsoft Surface Pro 7',
            brandname='Microsoft',
            cpu='Intel Core i5',
            ram='8GB',
            disk='128GB SSD',
            status='Reparing'
        )

        dev14 = Device(
            serial_number='SN-AS-014',
            rent_startdate=date(2022, 12, 12),
            rent_expired=date(2025, 12, 12),
            model='ASUS VivoBook 15',
            brandname='ASUS',
            cpu='Intel Core i7',
            ram='16GB',
            disk='512GB SSD',
            status='Standby'
        )
        db.session.add_all([dev1, dev2, dev3, dev4, dev5, dev6, dev7, dev8, dev9, dev10, dev11, dev12, dev13, dev14])
        db.session.commit()

        # Tạo dummy dữ liệu phân bổ (ASSIGNMENT)
        today = date.today()
        # Tính ngày đầu và cuối của tháng hiện tại
        current_year = today.year
        current_month = today.month
        
        # 1. Device 1 được giao cho emp1 từ đầu tháng đến hiện tại chưa trả (end_date=None)
        assign1 = Assignment(
            device_id=dev1.id,
            employee_id=emp1.id,
            start_date=date(current_year, current_month, 2),
            end_date=None
        )
        
        # 2. Device 2 được xài bởi emp3 từ mùng 5 đến mùng 15
        assign2 = Assignment(
            device_id=dev2.id,
            employee_id=emp3.id,
            start_date=date(current_year, current_month, 5),
            end_date=date(current_year, current_month, 15)
        )
        # 3. Sau đó Device 2 lại được giao cho emp2 từ ngày 18 đến cuối tháng
        assign3 = Assignment(
            device_id=dev2.id,
            employee_id=emp2.id,
            start_date=date(current_year, current_month, 18),
            end_date=None
        )
        assign4 = Assignment(
            device_id=dev3.id,
            employee_id=emp1.id,
            start_date=date(2026, 2, 3),
            end_date=None
        )

        assign5 = Assignment(
            device_id=dev4.id,
            employee_id=emp5.id,
            start_date=date(2026, 2, 15),
            end_date=date(2026, 3, 10)
        )

        assign6 = Assignment(
            device_id=dev5.id,
            employee_id=emp7.id,
            start_date=date(2026, 3, 1),
            end_date=None
        )

        assign7 = Assignment(
            device_id=dev6.id,
            employee_id=emp3.id,
            start_date=date(2026, 3, 20),
            end_date=date(2026, 4, 5)
        )

        # assign8 = Assignment(
        #     device_id=dev7.id,
        #     employee_id=emp4.id,
        #     start_date=date(2026, 4, 2),
        #     end_date=None
        # )

        assign9 = Assignment(
            device_id=dev8.id,
            employee_id=emp9.id,
            start_date=date(2026, 4, 15),
            end_date=date(2026, 5, 1)
        )

        assign10 = Assignment(
            device_id=dev9.id,
            employee_id=emp6.id,
            start_date=date(2026, 5, 1),
            end_date=None
        )

        assign11 = Assignment(
            device_id=dev10.id,
            employee_id=emp2.id,
            start_date=date(2026, 5, 10),
            end_date=date(2026, 6, 3)
        )

        assign12 = Assignment(
            device_id=dev11.id,
            employee_id=emp8.id,
            start_date=date(2026, 2, 28),
            end_date=None
        )

        assign13 = Assignment(
            device_id=dev12.id,
            employee_id=emp1.id,
            start_date=date(2026, 3, 7),
            end_date=date(2026, 5, 20)
        )

        assign14 = Assignment(
            device_id=dev13.id,
            employee_id=emp2.id,
            start_date=date(2026, 4, 18),
            end_date=None
        )

        assign15 = Assignment(
            device_id=dev14.id,
            employee_id=emp3.id,
            start_date=date(2026, 5, 5),
            end_date=date(2026, 6, 1)
        )

        assign16 = Assignment(
            device_id=dev1.id,
            employee_id=emp4.id,
            start_date=date(2026, 6, 1),
            end_date=None
        )

        assign17 = Assignment(
            device_id=dev2.id,
            employee_id=emp5.id,
            start_date=date(2026, 2, 22),
            end_date=date(2026, 4, 12)
        )

        assign18 = Assignment(
            device_id=dev3.id,
            employee_id=emp6.id,
            start_date=date(2026, 3, 29),
            end_date=None
        )

        assign19 = Assignment(
            device_id=dev4.id,
            employee_id=emp7.id,
            start_date=date(2026, 4, 8),
            end_date=date(2026, 6, 5)
        )

        assign20 = Assignment(
            device_id=dev5.id,
            employee_id=emp8.id,
            start_date=date(2026, 6, 10),
            end_date=None
        )
        db.session.add_all([assign1, assign2, assign3, assign4, assign5, assign6, assign7, assign9, assign10, assign11, assign12, assign13, assign14, assign15, assign16, assign17, assign18, assign19, assign20])
        db.session.commit()
        print("Đã tạo Dummy Data thành công vào file app.db !")

if __name__ == '__main__':
    seed()
