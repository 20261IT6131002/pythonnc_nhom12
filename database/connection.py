# database/connection.py — Kết nối MongoDB
#
# Triển khai:
#   - Singleton MongoClient: chỉ tạo 1 lần duy nhất trong suốt vòng đời app
#   - Hàm get_db() trả về database instance
#   - Hàm close_db() đóng kết nối khi thoát app
#   - Tạo index khi khởi động:
#       + db.users.create_index("username", unique=True)
#       + db.notes.create_index("user_id")

