import pandas as pd
import sqlite3
import os

# 1. Cấu hình đường dẫn
excel_file = 'data.xlsx'
db_file = 'appdata/app.db'
table_name = 'user'  # Tên bảng trong database của bạn

# 2. Đọc file Excel bằng Pandas
# Bạn có thể chọn sheet cụ thể bằng sheet_name='Sheet1'
df = pd.read_excel(excel_file)

# Xử lý dữ liệu thô nếu cần (Ví dụ: xóa dòng trống)
df = df.dropna(how='all')

# 3. Kết nối và đổ dữ liệu vào SQLite
conn = sqlite3.connect(db_file)

try:
    # if_exists='append': Thêm dữ liệu vào bảng đã có
    # if_exists='replace': Xóa bảng cũ tạo lại bảng mới
    # index=False: Không copy cột số thứ tự của Pandas vào DB
    df.to_sql(table_name, conn, if_exists='append', index=False)
    print(f"Thành công! Đã đổ {len(df)} dòng vào bảng {table_name}.")
except Exception as e:
    print(f"Lỗi rồi: {e}")
finally:
    conn.close()