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

