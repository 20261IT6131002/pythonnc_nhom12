
from threading import Lock

from pymongo import MongoClient
from pymongo.database import Database

from config import MONGODB_URI, DB_NAME


_client = None
_db = None
_lock = Lock()


def get_db() -> Database:
    """Lấy kết nối MongoDB theo mô hình Singleton."""

    global _client, _db

    if _db is None:
        with _lock:
            if _db is None:
                client = MongoClient(
                    MONGODB_URI,
                    serverSelectionTimeoutMS=5000
                )

                try:
                    # Kiểm tra kết nối MongoDB
                    client.admin.command("ping")

                    # Lấy database
                    db = client[DB_NAME]

                    # Tạo index cho collection users
                    db.users.create_index(
                        "username",
                        unique=True
                    )

                    # Tạo index cho collection notes
                    db.notes.create_index("user_id")

                    _client = client
                    _db = db

                except Exception:
                    client.close()
                    raise

    return _db


def close_db() -> None:
    """Đóng kết nối MongoDB khi thoát ứng dụng."""

    global _client, _db

    with _lock:
        if _client is not None:
            _client.close()

        _client = None
        _db = None
