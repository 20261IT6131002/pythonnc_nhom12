# controllers/note_controller.py — Xử lý logic ghi chú
#
# Triển khai:
#   - get_notes(user_id, filter, keyword) -> list[Note]
#       + Gọi note_repo.get_notes()
#       + Chuyển list dict từ MongoDB thành list Note object
#
#   - create_note(user_id, title, label, content) -> (bool, str)
#       + Validate: title không được rỗng
#       + Gọi note_repo.create_note()
#       + Trả về (True, note_id) hoặc (False, thông báo lỗi)
#
#   - update_note(note_id, title, label, content) -> (bool, str)
#       + Validate: title không được rỗng
#       + Gọi note_repo.update_note()
#
#   - delete_note(note_id, permanent=False)
#       + permanent=False → gọi note_repo.soft_delete() (vào thùng rác)
#       + permanent=True  → gọi note_repo.hard_delete() (xóa vĩnh viễn)
#
#   - restore_note(note_id)
#       + Gọi note_repo.restore()
#
#   - toggle_star(note_id)
#       + Gọi note_repo.toggle_star()

from models.note import Note
from database import note_repo

VALID_LABELS = {"Công việc", "Học tập", "Cá nhân", "Khác"}


class NoteController:
    @staticmethod
    def get_notes(user_id: str, filter: str, keyword: str = "") -> list[Note]:
        if not user_id:
            return []
        try:
            docs = note_repo.get_notes(user_id, filter, keyword or "")
            return [Note.from_dict(doc) for doc in docs] if docs else []
        except Exception:
            return []

    @staticmethod
    def create_note(user_id: str, title: str, label: str, content: str) -> tuple[bool, str]:
        clean_title = (title or "").strip()
        if not clean_title:
            return False, "Tiêu đề ghi chú không được để trống."
        if not user_id:
            return False, "Thiếu thông tin người dùng."
        clean_label = label if label in VALID_LABELS else "Khác"
        try:
            note_id = note_repo.create_note(user_id, clean_title, clean_label, content or "")
            return True, str(note_id)
        except Exception as exc:
            return False, f"Không thể tạo ghi chú: {exc}"

    @staticmethod
    def update_note(note_id: str, title: str, label: str, content: str) -> tuple[bool, str]:
        clean_title = (title or "").strip()
        if not clean_title:
            return False, "Tiêu đề ghi chú không được để trống."
        if not note_id:
            return False, "Thiếu mã ghi chú."
        clean_label = label if label in VALID_LABELS else "Khác"
        try:
            note_repo.update_note(note_id, clean_title, clean_label, content or "")
            return True, ""
        except Exception as exc:
            return False, f"Không thể cập nhật ghi chú: {exc}"

    @staticmethod
    def delete_note(note_id: str, permanent: bool = False) -> None:
        if not note_id:
            return
        try:
            if permanent:
                note_repo.hard_delete(note_id)
            else:
                note_repo.soft_delete(note_id)
        except Exception:
            pass

    @staticmethod
    def restore_note(note_id: str) -> None:
        if not note_id:
            return
        try:
            note_repo.restore(note_id)
        except Exception:
            pass

    @staticmethod
    def toggle_star(note_id: str) -> None:
        if not note_id:
            return
        try:
            note_repo.toggle_star(note_id)
        except Exception:
            pass