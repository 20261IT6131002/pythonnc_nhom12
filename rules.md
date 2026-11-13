# 📋 Quy tắc phát triển — MyNote

> Đọc kỹ trước khi bắt đầu code. Tuân thủ để tránh conflict và tích hợp trơn tru.

---

## 1. Phân công module

| Module | File | Người phụ trách |
|--------|------|-----------------|
| Kết nối DB | `database/connection.py` | Trần Văn Trọng |
| Repo người dùng | `database/user_repo.py` | Bùi Anh Duy |
| Repo ghi chú | `database/note_repo.py` | Bùi Anh Duy |
| Model | `models/user.py`, `models/note.py` | Trần Văn Trọng |
| Xác thực | `controllers/auth_controller.py` | Nguyễn Minh Tú |
| Ghi chú | `controllers/note_controller.py` | Nguyễn Đình Trung |
| View đăng nhập / đăng ký | `views/login_view.py`, `views/register_view.py` | Nguyễn Minh Tú, Nguyễn Đình Trung |
| View chính | `views/main_view.py` | Nguyễn Đình Trung |
| Điều hướng & tích hợp | `main.py` _(chỉ chứa class `App`)_, `config.py` | Đặng Quang Anh |

> **Quy tắc:** mỗi người **chỉ chỉnh sửa file được phân công**. Không tự ý sửa `main.py` hay `config.py`.
>
> **Lưu ý cấu trúc:** mỗi View nằm trong file riêng tại `views/`. `main.py` chỉ import và điều hướng giữa chúng, không chứa code UI.

---

## 2. Luồng dữ liệu

```
View  →  Controller  →  Repo  →  MongoDB
               ↑                     ↓
            Model  ←  from_dict(doc)
```

- **View** chỉ hiển thị và thu thập input từ người dùng. Không được gọi trực tiếp Repo hay MongoDB.
- **Controller** xử lý validate và nghiệp vụ, gọi Repo, trả kết quả về View.
- **Repo** chỉ thực hiện CRUD thuần trên MongoDB, không chứa logic nghiệp vụ.
- **Model** là dataclass thuần — không có logic, không import controller hay repo.

---

## 3. Interface Controller → View

### 3.1 `AuthController`

```python
# Đăng ký
register(username: str, fullname: str, password: str, confirm: str) -> (bool, str)
# Trả về:
#   (True,  "")              — thành công
#   (False, "thông báo lỗi") — thất bại (username trùng, password không khớp, v.v.)

# Đăng nhập
login(username: str, password: str) -> (User | None, str)
# Trả về:
#   (User, "")               — đúng thông tin
#   (None, "thông báo lỗi")  — sai username hoặc password

# Đăng xuất (không có return)
logout() -> None
```

**View dùng như sau:**
```python
# Trong LoginView — khi bấm nút "Đăng nhập":
user, err = AuthController.login(username, password)
if user:
    self.on_login(user)        # callback truyền từ App → chuyển sang MainView
else:
    self.lbl_error.configure(text=err)

# Trong RegisterView — khi bấm nút "Đăng ký":
ok, err = AuthController.register(username, fullname, password, confirm)
if ok:
    self.on_register()         # callback → về LoginView
else:
    self.lbl_error.configure(text=err)
```

---

### 3.2 `NoteController`

```python
# Lấy danh sách ghi chú
get_notes(user_id: str, filter: str, keyword: str = "") -> list[Note]
# filter nhận một trong: "Tất cả ghi chú" | "Công việc" | "Học tập"
#                        "Cá nhân" | "Khác" | "Đánh dấu" | "Thùng rác"

# Thêm ghi chú
create_note(user_id: str, title: str, label: str, content: str) -> (bool, str)
# Trả về (True, note_id) hoặc (False, "thông báo lỗi")

# Sửa ghi chú
update_note(note_id: str, title: str, label: str, content: str) -> (bool, str)

# Xóa (mềm → thùng rác)
delete_note(note_id: str, permanent: bool = False) -> None

# Khôi phục khỏi thùng rác
restore_note(note_id: str) -> None

# Đánh dấu / bỏ đánh dấu
toggle_star(note_id: str) -> None
```

**View dùng như sau:**
```python
# Trong MainView — load danh sách:
notes = NoteController.get_notes(self.user.id, self.active_filter, keyword)
# → dùng list[Note] để render card

# Thêm / sửa ghi chú:
ok, err = NoteController.create_note(user_id, title, label, content)
if ok:
    self.refresh()
else:
    err_label.configure(text=err)
```

---

## 4. Model — cấu trúc dataclass

```python
# models/user.py
@dataclass
class User:
    id:       str
    username: str
    fullname: str

    @staticmethod
    def from_dict(doc: dict) -> "User": ...

# models/note.py
@dataclass
class Note:
    id:      str
    user_id: str
    title:   str
    label:   str      # "Công việc" | "Học tập" | "Cá nhân" | "Khác"
    content: str
    starred: bool
    deleted: bool
    created: str      # "YYYY-MM-DD HH:MM"

    @staticmethod
    def from_dict(doc: dict) -> "Note": ...
```

> `id` luôn là **string** (convert từ MongoDB `ObjectId`). Không truyền `ObjectId` thô lên Controller hay View.

---

## 5. Database — Repo interface

### `user_repo.py`
```python
create_user(username: str, fullname: str, password_hash: str) -> str  # trả về user_id
find_by_username(username: str) -> dict | None
```

### `note_repo.py`
```python
get_notes(user_id: str, filter: str, keyword: str) -> list[dict]
create_note(user_id: str, title: str, label: str, content: str) -> str  # note_id
update_note(note_id: str, title: str, label: str, content: str) -> None
soft_delete(note_id: str) -> None
hard_delete(note_id: str) -> None
restore(note_id: str) -> None
toggle_star(note_id: str) -> None
```

### `connection.py`
```python
get_db() -> pymongo.database.Database   # dùng Singleton, gọi ở mọi nơi cần DB
close_db() -> None
```

---

## 6. Quy tắc Git

- Branch đặt tên theo format: `feature/<tên-chức-năng>` (ví dụ: `feature/auth`, `feature/note-crud`, `feature/ui-main`)
- **Không push thẳng lên `main`**. Tạo Pull Request và báo người tích hợp review.
- Mỗi commit viết rõ nội dung: `feat: thêm login`, `fix: sửa lỗi validate password`
- File `.env` **không được commit** (đã có trong `.gitignore`). Chia sẻ `MONGODB_URI` qua kênh riêng.

---

## 7. Cài đặt môi trường

```bash
# 1. Clone repo
git clone <repo-url>
cd mynote

# 2. Cài thư viện
pip install -r requirements.txt

# 3. Tạo file .env (copy mẫu, điền URI thật)
cp .env.example .env   # hoặc tạo tay

# 4. Chạy app
python main.py
```

**Nội dung `.env`:**
```
MONGODB_URI=mongodb+srv://<username>:<password>@cluster.mongodb.net/
```

---

## 8. Checklist trước khi tạo Pull Request

- [ ] Code chạy được, không có lỗi runtime
- [ ] Không để `print()` debug trong code
- [ ] Không hardcode URI, password hay thông tin nhạy cảm
- [ ] Tên hàm, biến viết bằng tiếng Anh theo `snake_case`
- [ ] Đã test thủ công chức năng được phân công

