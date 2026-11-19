# database/user_repo.py — Thao tác với collection "users"
#
# Triển khai:
#   - create_user(username, password_hash)
#       + Thêm document mới vào collection users
#       + Lưu password đã được bcrypt hash, KHÔNG lưu raw password
#   - find_by_username(username) -> dict | None
#       + Tìm user theo username để phục vụ đăng nhập


# database/user_repo.py
# Thao tác với collection "users"

from database.connection import get_db


def create_user(username: str, password_hash: str) -> str:
    """
    Tạo tài khoản người dùng mới.

    Args:
        username: Tên đăng nhập.
        password_hash: Mật khẩu đã được mã hóa bằng bcrypt.

    Returns:
        ID của người dùng vừa tạo.
    """

    db = get_db()

    user_data = {
        "username": username,
        "password_hash": password_hash
    }

    result = db.users.insert_one(user_data)

    return str(result.inserted_id)


def find_by_username(username: str) -> dict | None:
    """
    Tìm người dùng theo username.

    Args:
        username: Tên đăng nhập cần tìm.

    Returns:
        Document người dùng nếu tìm thấy, ngược lại trả về None.
    """

    db = get_db()

    user = db.users.find_one({
        "username": username
    })

    return user
