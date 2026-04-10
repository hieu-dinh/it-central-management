Kế hoạch triển khai Admin Dashboard (IT Central Management)
Mục tiêu: Xây dựng khu vực bảo mật yêu cầu đăng nhập chỉ dành cho IT Admin, cho phép quản lý toàn hình (Thêm/Sửa/Xóa) thiết bị (Device), nhân viên (Employee), và các lịch sử cấp phát (Assignment).

1. Authentication (Xác thực đăng nhập)
Cài đặt thư viện Flask-Login để quản lý session đăng nhập và bảo vệ các routes.
Chỉnh sửa model AdminUser để kế thừa UserMixin từ Flask-Login.
Đảm bảo mật khẩu admin được băm mã hóa bằng werkzeug.security.
Xây dựng trang /login giao diện gọn nhẹ, với form username/password.
Thay vì tự tạo giao diện CRUD từ đầu, sử dụng thư viện nào đó nhanh chóng? Vì yêu cầu custom cao để giao diện đồng bộ TailwindCSS, ta sẽ code giao diện Admin bằng HTML/Tailwind để đẹp và đồng nhất.
2. Giao diện Admin Dashboard (UI/UX)
Tạo template vỏ bọc chung admin_layout.html (Base template):

Sidebar Menu: Liệt kê các chức năng chính:
Dashboard: Thống kê tổng số lượng thiết bị, tổng đang mượn, tổng phòng ban,... (Nâng cao: có thể link ra public timeline).
Quản lý Thiết bị (Devices): Danh sách Table, nút Add, Edit, Delete.
Quản lý Nhân sự (Employees): Table, Add, Edit, Delete.
Quản lý Bàn giao (Assignments): Giao máy mới, Xác nhận trả máy (set end_date).
Top Navbar: Nút Đăng xuất (Logout) và thông báo vắn tắt.
3. Quản lý Thiết bị (Devices CRUD)
Trang danh sách (Read): GET /admin/devices. Hiển thị Table toàn bộ thiết bị.
Trang Tạo mới (Create): GET, POST /admin/device/create. Form nhập các thông số (Brand, Model, CPU, ... dates).
Trang Cập nhật/Sửa (Update): GET, POST /admin/device/edit/<id>. Form có sẵn dữ liệu cũ, chỉnh sửa Status (In-Use, Standby, ...).
4. Quản lý Điều phối Thiết bị (Assignments CRUD)
Yêu cầu chức năng "Bàn giao máy" (Cấp phát máy): Chọn một Device còn ở kho (Standby), gán cho một Employee, nhập start_date. Khi đó status máy chuyển thành In-Use.
Yêu cầu chức năng "Thu hồi máy" (Trả máy): Khi thiết bị được trả, cập nhật end_date của assignment đó = today, đồng thời reset trạng thái của Device về Standby hoặc Reparing.
5. Khởi tạo dữ liệu Admin (Seed)
Từ lúc này, script seed_data.py cần tự động tạo ra một account admin mặc định (Ví dụ: user: admin, pass: admin123) để hỗ trợ việc đăng nhập lần đầu ngay khi DB trắng.

User Review Required
IMPORTANT

Mình sẽ cần cài thêm thư viện Flask-Login (pip install flask-login). Bạn có okay với phương án này không?
Các form Admin mình sẽ chỉ sử dụng HTML thuần + TailwindCSS để làm, không sử dụng Javascript Framework (React/Vue) để giữ Project ở chuẩn đơn giản "nhanh-nhẹ" như bạn đã yêu cầu ban đầu.
Bạn có muốn trang Admin được tích hợp luôn trong app.py hay cần tách file xử lí logic ra không? Hiện tại project nhỏ nên mình có thể gộp chung vào app.py.