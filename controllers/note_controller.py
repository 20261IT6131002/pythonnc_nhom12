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

