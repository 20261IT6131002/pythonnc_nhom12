"""Quản lý kết nối MongoDB theo mô hình Singleton."""

from threading import Lock
from typing import Optional

from pymongo import MongoClient
from pymongo.database import Database

from config import DB_NAME, MONGODB_URI


_client: Optional[MongoClient] = None
_db: Optional[Database] = None
_lock = Lock()


def get_db() -> Database:
    """Trả về Database MongoDB dùng chung."""

    global _client, _db

    if _db is None:
        with _lock:
            if _db is None:
                client = MongoClient(
                    MONGODB_URI,
                    serverSelectionTimeoutMS=5000
                )

                try:
                    client.admin.command("ping")

                    _client = client
                    _db = client[DB_NAME]

                except Exception:
                    client.close()
                    raise

    return _db


def close_db() -> None:
    """Đóng kết nối MongoDB."""

    global _client, _db

    with _lock:
        if _client is not None:
            _client.close()

        _client = None
        _db = None
