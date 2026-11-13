# models/user.py — Dataclass đại diện cho người dùng
#
# Triển khai:
#   - Dataclass User với các field:
#       + id: str          (ObjectId chuyển sang string)
#       + username: str
#   - Hàm from_dict(doc: dict) -> User
#       + Chuyển MongoDB document thành User object

