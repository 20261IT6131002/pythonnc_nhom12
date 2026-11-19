# database/note_repo.py — Thao tác với collection "notes"
#
# Triển khai:
#   - get_notes(user_id, filter, keyword) -> list[dict]
#       + Lọc theo filter: tất cả / nhãn / đánh dấu / thùng rác
#       + Tìm kiếm theo keyword trong title và content
#       + Chỉ lấy notes thuộc về user_id đang đăng nhập
#   - create_note(user_id, title, label, content) -> ObjectId
#       + Thêm ghi chú mới, gắn user_id, starred=False, deleted=False
#   - update_note(note_id, title, label, content)
#       + Cập nhật title, label, content theo note_id
#   - soft_delete(note_id)
#       + Đặt deleted=True (chuyển vào thùng rác)
#   - restore(note_id)
#       + Đặt deleted=False (khôi phục khỏi thùng rác)
#   - hard_delete(note_id)
#       + Xóa vĩnh viễn document khỏi collection
#   - toggle_star(note_id)
#       + Đảo giá trị starred (True ↔ False)


# database/note_repo.py
# Thao tác với collection "notes"

import re
from datetime import datetime, timezone
from bson import ObjectId

from database.connection import get_db


def get_notes(user_id, filter, keyword) -> list[dict]:
    """
    Lấy danh sách ghi chú của người dùng.

    filter:
        - all: Tất cả ghi chú
        - starred: Ghi chú đã đánh dấu
        - trash: Ghi chú trong thùng rác
        - Giá trị khác: Lọc theo nhãn (label)
    """

    db = get_db()

    query = {
        "user_id": str(user_id)
    }

    # Lọc theo trạng thái
    if filter in ("starred", "đánh dấu"):
        query["deleted"] = False
        query["starred"] = True

    elif filter in ("trash", "thùng rác"):
        query["deleted"] = True

    elif filter not in (None, "", "all", "tất cả"):
        query["deleted"] = False
        query["label"] = filter

    else:
        query["deleted"] = False

    # Tìm kiếm theo tiêu đề và nội dung
    if keyword and keyword.strip():
        search_keyword = re.escape(keyword.strip())

        query["$or"] = [
            {"title": {"$regex": search_keyword, "$options": "i"}},
            {"content": {"$regex": search_keyword, "$options": "i"}}
        ]

    return list(
        db.notes.find(query).sort("_id", -1)
    )


def create_note(user_id, title, label, content) -> ObjectId:
    """
    Tạo ghi chú mới cho người dùng.
    """

    db = get_db()

    note_data = {
    "user_id": str(user_id),
    "title": title,
    "label": label,
    "content": content,
    "starred": False,
    "deleted": False,
    "created": datetime.now(timezone.utc).isoformat()
}

    result = db.notes.insert_one(note_data)

    return result.inserted_id


def update_note(note_id, title, label, content):
    """
    Cập nhật tiêu đề, nhãn và nội dung ghi chú.
    """

    db = get_db()

    db.notes.update_one(
        {"_id": ObjectId(note_id)},
        {
            "$set": {
                "title": title,
                "label": label,
                "content": content
            }
        }
    )


def soft_delete(note_id):
    """
    Chuyển ghi chú vào thùng rác.
    """

    db = get_db()

    db.notes.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"deleted": True}}
    )


def restore(note_id):
    """
    Khôi phục ghi chú khỏi thùng rác.
    """

    db = get_db()

    db.notes.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"deleted": False}}
    )


def hard_delete(note_id):
    """
    Xóa vĩnh viễn ghi chú khỏi MongoDB.
    """

    db = get_db()

    db.notes.delete_one({
        "_id": ObjectId(note_id)
    })


def toggle_star(note_id):
    """
    Đảo trạng thái đánh dấu ghi chú.
    True thành False và False thành True.
    """

    db = get_db()

    note = db.notes.find_one({
        "_id": ObjectId(note_id)
    })

    if note is None:
        return

    current_starred = note.get("starred", False)

    db.notes.update_one(
        {"_id": ObjectId(note_id)},
        {"$set": {"starred": not current_starred}}
    )
