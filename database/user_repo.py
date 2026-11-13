# database/user_repo.py — Thao tác với collection "users"
#
# Triển khai:
#   - create_user(username, password_hash)
#       + Thêm document mới vào collection users
#       + Lưu password đã được bcrypt hash, KHÔNG lưu raw password
#   - find_by_username(username) -> dict | None
#       + Tìm user theo username để phục vụ đăng nhập

