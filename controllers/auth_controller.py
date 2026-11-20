# controllers/auth_controller.py — Xử lý logic xác thực (đăng ký / đăng nhập / đăng xuất)
#
# Luồng: View -> AuthController -> user_repo -> MongoDB
# View chỉ gọi các staticmethod bên dưới, không gọi trực tiếp Repo.

import re

import bcrypt
from pymongo.errors import DuplicateKeyError, PyMongoError

from database import user_repo
from models.user import User

USERNAME_MIN = 3
USERNAME_MAX = 30
PASSWORD_MIN = 6
PASSWORD_MAX_BYTES = 72          # giới hạn của bcrypt
FULLNAME_MAX = 60
_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.]+$")

# Hash giả để vẫn tốn thời gian bcrypt khi username không tồn tại
# (tránh lộ việc username có tồn tại hay không qua thời gian phản hồi).
_DUMMY_HASH = bcrypt.hashpw(b"dummy-password", bcrypt.gensalt())

_DB_ERROR = "Không thể kết nối cơ sở dữ liệu. Vui lòng thử lại sau."


class AuthController:
    # Người dùng đang đăng nhập (None nếu chưa đăng nhập)
    _current_user: User | None = None

    # ── Đăng ký ──────────────────────────────────────────────────────────────
    @staticmethod
    def register(username: str, fullname: str, password: str, confirm: str) -> tuple[bool, str]:
        """Trả về (True, "") nếu thành công, (False, thông báo lỗi) nếu thất bại."""
        username = (username or "").strip().lower()
        fullname = " ".join((fullname or "").split())   # bỏ khoảng trắng thừa
        password = password or ""
        confirm = confirm or ""

        err = AuthController._validate_register(username, fullname, password, confirm)
        if err:
            return False, err

        try:
            if user_repo.find_by_username(username) is not None:
                return False, "Tên đăng nhập đã tồn tại."

            password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            user_repo.create_user(username, fullname, password_hash)
        except DuplicateKeyError:
            # Hai người đăng ký cùng lúc: unique index của MongoDB chặn lại
            return False, "Tên đăng nhập đã tồn tại."
        except PyMongoError:
            return False, _DB_ERROR

        return True, ""

    # ── Đăng nhập ────────────────────────────────────────────────────────────
    @staticmethod
    def login(username: str, password: str) -> tuple[User | None, str]:
        """Trả về (User, "") nếu đúng thông tin, (None, thông báo lỗi) nếu sai."""
        username = (username or "").strip().lower()
        password = password or ""

        if not username or not password:
            return None, "Vui lòng nhập tên đăng nhập và mật khẩu."

        try:
            doc = user_repo.find_by_username(username)
        except PyMongoError:
            return None, _DB_ERROR

        stored_hash = (doc or {}).get("password_hash") or (doc or {}).get("password")
        if isinstance(stored_hash, str):
            stored_hash = stored_hash.encode("utf-8")

        try:
            valid = bcrypt.checkpw(password.encode("utf-8"), stored_hash or _DUMMY_HASH)
        except ValueError:          # hash hỏng / password quá dài
            valid = False

        if not doc or not stored_hash or not valid:
            # Cùng một thông báo cho cả "sai username" và "sai password"
            return None, "Tên đăng nhập hoặc mật khẩu không chính xác."

        user = User.from_dict(doc)
        AuthController._current_user = user
        return user, ""

    # ── Đăng xuất ────────────────────────────────────────────────────────────
    @staticmethod
    def logout() -> None:
        AuthController._current_user = None

    @staticmethod
    def get_current_user() -> User | None:
        return AuthController._current_user

    # ── Validate ─────────────────────────────────────────────────────────────
    @staticmethod
    def _validate_register(username: str, fullname: str, password: str, confirm: str) -> str:
        """Trả về thông báo lỗi đầu tiên gặp phải, hoặc "" nếu hợp lệ."""
        if not username:
            return "Vui lòng nhập tên đăng nhập."
        if not USERNAME_MIN <= len(username) <= USERNAME_MAX:
            return f"Tên đăng nhập phải từ {USERNAME_MIN} đến {USERNAME_MAX} ký tự."
        if not _USERNAME_RE.match(username):
            return "Tên đăng nhập chỉ gồm chữ cái, số, dấu gạch dưới (_) và dấu chấm (.)."
        if not fullname:
            return "Vui lòng nhập họ và tên."
        if len(fullname) > FULLNAME_MAX:
            return f"Họ và tên không được quá {FULLNAME_MAX} ký tự."
        if not password:
            return "Vui lòng nhập mật khẩu."
        if len(password) < PASSWORD_MIN:
            return f"Mật khẩu phải có ít nhất {PASSWORD_MIN} ký tự."
        if len(password.encode("utf-8")) > PASSWORD_MAX_BYTES:
            return "Mật khẩu quá dài (tối đa 72 byte)."
        if password != confirm:
            return "Mật khẩu xác nhận không khớp."
        return ""
