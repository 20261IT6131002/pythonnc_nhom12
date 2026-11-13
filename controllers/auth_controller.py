# controllers/auth_controller.py — Xử lý logic xác thực
#
# Triển khai:
#   - register(username, password, confirm_password) -> (bool, str)
#       + Validate: username không rỗng, password >= 6 ký tự, password == confirm
#       + Hash password bằng bcrypt trước khi lưu
#       + Gọi user_repo.create_user()
#       + Trả về (True, "") nếu thành công, (False, thông báo lỗi) nếu thất bại
#
#   - login(username, password) -> (User | None, str)
#       + Gọi user_repo.find_by_username()
#       + Dùng bcrypt.checkpw() để xác minh password
#       + Trả về (User, "") nếu đúng, (None, thông báo lỗi) nếu sai
#
#   - logout()
#       + Xóa session / trạng thái user hiện tại (nếu có lưu)

