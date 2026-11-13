# models/note.py — Dataclass đại diện cho ghi chú
#
# Triển khai:
#   - Dataclass Note với các field:
#       + id: str
#       + user_id: str
#       + title: str
#       + label: str       ("Công việc" | "Học tập" | "Cá nhân" | "Khác")
#       + content: str
#       + starred: bool
#       + deleted: bool
#       + created: str     (định dạng "YYYY-MM-DD HH:MM")
#   - Hàm from_dict(doc: dict) -> Note
#       + Chuyển MongoDB document thành Note object

