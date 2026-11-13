# views/main_view.py — Màn hình chính (quản lý ghi chú)

import customtkinter as ctk
from config import (
    ACCENT, ACCENT_HOVER,
    SIDEBAR, MAIN_BG, SURFACE, SURFACE_HOVER, SELECTED, BORDER,
    TEXT, MUTED,
    NEUTRAL_BUTTON, NEUTRAL_HOVER,
    DANGER_BUTTON, DANGER_HOVER, DANGER_TEXT,
    LABELS, FILTERS, FILTER_ICONS,
    FONT_TITLE, FONT_HEADING, FONT_LABEL,
    FONT_SMALL, FONT_TINY, FONT_CONTENT, FONT_NAV,
)

# Dữ liệu mẫu chỉ dùng để render giao diện (xóa khi tích hợp controller)
_DEMO_NOTES = [
    {
        "id": 1, "title": "Ôn tập thuật toán", "label": "Học tập",
        "content": (
            "Cần xem lại các thuật toán cơ bản như:\n"
            "- Tìm kiếm nhị phân\n"
            "- Sắp xếp (Quick Sort, Merge Sort)\n"
            "- Quy hoạch động"
        ),
        "starred": False, "deleted": False, "created": "2026-11-08 00:12",
    },
    {
        "id": 2, "title": "Kế hoạch tuần", "label": "Công việc",
        "content": "- Học KTPM\n- Làm đồ án\n- Nộp báo cáo thứ Sáu",
        "starred": False, "deleted": False, "created": "2026-11-07 20:30",
    },
    {
        "id": 3, "title": "Danh sách mua sắm", "label": "Khác",
        "content": "Sữa, trứng, mì gói, rau xanh",
        "starred": False, "deleted": False, "created": "2026-11-06 18:05",
    },
    {
        "id": 4, "title": "Ý tưởng dự án", "label": "Cá nhân",
        "content": "Xây dựng ứng dụng quản lý chi tiêu cá nhân.",
        "starred": True, "deleted": False, "created": "2026-11-05 09:40",
    },
]

_DEMO_USER = {"username": "nguoidung", "fullname": "Nguyễn Văn A"}


class MainView(ctk.CTkFrame):
    """Màn hình chính: sidebar + list panel + detail panel."""

    def __init__(self, master, user=None, on_logout=None):
        super().__init__(master, fg_color=MAIN_BG, corner_radius=0)
        self.user          = user or _DEMO_USER
        self.on_logout     = on_logout or (lambda: None)
        self.active_filter = "Tất cả ghi chú"
        self.nav_buttons   = {}
        self._build()

    # ── Layout gốc ──────────────────────────────────────────────────────────
    def _build(self):
        self.grid_columnconfigure(0, minsize=220)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self._build_sidebar()
        self._build_main()

    # ════════════════════════════════════════════════════════════════════════
    #  Sidebar
    # ════════════════════════════════════════════════════════════════════════
    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color=SIDEBAR)
        sb.grid(row=0, column=0, sticky="nsew")
        sb.grid_propagate(False)

        # Tên app
        ctk.CTkLabel(sb, text="Ghi chú", font=FONT_TITLE,
                     text_color=TEXT).pack(anchor="w", padx=20, pady=(28, 2))
        ctk.CTkLabel(sb, text="Gọn gàng, dễ tìm",
                     font=FONT_SMALL, text_color=MUTED).pack(anchor="w", padx=20, pady=(0, 20))

        # Thông tin user
        user_box = ctk.CTkFrame(sb, fg_color=SURFACE, corner_radius=8,
                                border_width=1, border_color=BORDER)
        user_box.pack(fill="x", padx=12, pady=(0, 20))
        ctk.CTkLabel(user_box, text="👤",
                     font=("Segoe UI", 20)).pack(side="left", padx=(10, 6), pady=8)
        info = ctk.CTkFrame(user_box, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, pady=8)
        ctk.CTkLabel(info, text=self.user["fullname"], anchor="w",
                     font=FONT_SMALL, text_color=TEXT).pack(anchor="w")
        ctk.CTkLabel(info, text=f'@{self.user["username"]}', anchor="w",
                     font=("Segoe UI", 10), text_color=MUTED).pack(anchor="w")

        # Menu filter
        ctk.CTkLabel(sb, text="THƯ VIỆN",
                     font=FONT_NAV, text_color=MUTED).pack(anchor="w", padx=20, pady=(0, 8))

        for name in FILTERS:
            active = (name == self.active_filter)
            b = ctk.CTkButton(
                sb,
                text=f"  {FILTER_ICONS[name]}   {name}",
                anchor="w", height=38, corner_radius=6,
                fg_color=SELECTED if active else "transparent",
                hover_color=SURFACE_HOVER,
                text_color=ACCENT if active else TEXT,
                font=("Segoe UI", 13, "bold" if active else "normal"),
            )
            b.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[name] = b

        # Bottom: divider → switch → logout
        ctk.CTkFrame(sb, height=1, fg_color=BORDER).pack(
            fill="x", padx=16, pady=(20, 12), side="bottom")

        ctk.CTkButton(
            sb, text="⏻  Đăng xuất", height=34, corner_radius=6,
            fg_color=DANGER_BUTTON, hover_color=DANGER_HOVER,
            text_color=DANGER_TEXT, font=FONT_SMALL, anchor="w",
            command=self.on_logout,
        ).pack(side="bottom", fill="x", padx=10, pady=(0, 8))

        ctk.CTkSwitch(
            sb, text="Chế độ tối", text_color=TEXT,
            progress_color=ACCENT, font=FONT_SMALL,
        ).pack(side="bottom", anchor="w", padx=18, pady=(0, 10))

    # ════════════════════════════════════════════════════════════════════════
    #  Khu vực chính (top bar + list panel + detail panel)
    # ════════════════════════════════════════════════════════════════════════
    def _build_main(self):
        main = ctk.CTkFrame(self, corner_radius=0, fg_color=MAIN_BG)
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_columnconfigure(0, weight=0, minsize=300)
        main.grid_columnconfigure(1, weight=1, minsize=320)
        main.grid_rowconfigure(1, weight=1)

        # ── Thanh tiêu đề ──
        top = ctk.CTkFrame(main, fg_color="transparent")
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=22, pady=(20, 18))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(top, text=self.active_filter, anchor="w",
                     text_color=TEXT, font=FONT_TITLE).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(top, text="Sắp xếp và quản lý ghi chú của bạn",
                     anchor="w", text_color=MUTED,
                     font=FONT_SMALL).grid(row=1, column=0, sticky="w", pady=(2, 0))

        actions = ctk.CTkFrame(top, fg_color="transparent")
        actions.grid(row=0, column=1, rowspan=2, sticky="e")
        ctk.CTkEntry(actions, width=210, height=38, corner_radius=6,
                     border_color=BORDER, fg_color=SURFACE, text_color=TEXT,
                     placeholder_text="⌕  Tìm kiếm ghi chú...",
                     placeholder_text_color=MUTED).pack(side="left", padx=(0, 10))
        ctk.CTkButton(actions, text="＋  Thêm ghi chú", height=38, width=142,
                      corner_radius=6, fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      text_color=("white", "#101820"),
                      font=FONT_SMALL).pack(side="left")

        # ── Danh sách ghi chú ──
        list_panel = ctk.CTkFrame(main, fg_color="transparent")
        list_panel.grid(row=1, column=0, sticky="nsew", padx=(20, 8), pady=(0, 18))
        list_panel.grid_columnconfigure(0, weight=1)
        list_panel.grid_rowconfigure(1, weight=1)

        list_hdr = ctk.CTkFrame(list_panel, fg_color="transparent")
        list_hdr.grid(row=0, column=0, sticky="ew", padx=4, pady=(0, 8))
        list_hdr.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(list_hdr, text="Ghi chú", text_color=TEXT,
                     font=FONT_HEADING).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(list_hdr, text=str(len(_DEMO_NOTES)),
                     text_color=MUTED, font=FONT_TINY).grid(row=0, column=1, sticky="e")

        list_frame = ctk.CTkScrollableFrame(
            list_panel, width=280, fg_color="transparent",
            corner_radius=0,
            scrollbar_button_color=BORDER,
            scrollbar_button_hover_color=MUTED)
        list_frame.grid(row=1, column=0, sticky="nsew")

        for idx, note in enumerate(_DEMO_NOTES):
            self._note_card(list_frame, note, selected=(idx == 0))

        # ── Chi tiết ghi chú ──
        self.detail = ctk.CTkFrame(main, corner_radius=8, fg_color=SURFACE,
                                   border_width=1, border_color=BORDER)
        self.detail.grid(row=1, column=1, sticky="nsew", padx=(8, 20), pady=(0, 18))
        self.detail.grid_columnconfigure(0, weight=1)
        self.detail.grid_rowconfigure(3, weight=1)
        self._show_detail(_DEMO_NOTES[0])

    # ── Card ghi chú ────────────────────────────────────────────────────────
    def _note_card(self, parent, note, selected=False):
        card = ctk.CTkFrame(
            parent, corner_radius=7, cursor="hand2",
            fg_color=SELECTED if selected else SURFACE,
            border_width=1,
            border_color=ACCENT if selected else BORDER)
        card.pack(fill="x", padx=2, pady=4)

        star = "★  " if note["starred"] else ""
        ctk.CTkLabel(card, text=star + note["title"], anchor="w",
                     text_color=TEXT,
                     font=FONT_LABEL).pack(fill="x", padx=12, pady=(11, 2))

        preview = note["content"].replace("\n", " ")
        preview = preview[:42] + ("..." if len(preview) > 42 else "")
        ctk.CTkLabel(card, text=preview, anchor="w",
                     text_color=MUTED,
                     font=FONT_TINY).pack(fill="x", padx=12)

        bottom = ctk.CTkFrame(card, fg_color="transparent")
        bottom.pack(fill="x", padx=12, pady=(7, 10))
        self._pill(bottom, note["label"]).pack(side="left")
        ctk.CTkLabel(bottom, text=note["created"][:10],
                     text_color=MUTED,
                     font=FONT_TINY).pack(side="right")

    # ── Chi tiết ────────────────────────────────────────────────────────────
    def _show_detail(self, note):
        head = ctk.CTkFrame(self.detail, fg_color="transparent")
        head.grid(row=0, column=0, sticky="ew", padx=22, pady=(20, 8))
        head.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(head, text=note["title"], anchor="w", text_color=TEXT,
                     font=FONT_TITLE, wraplength=500,
                     justify="left").grid(row=0, column=0, sticky="w")

        btns = ctk.CTkFrame(head, fg_color="transparent")
        btns.grid(row=1, column=0, sticky="w", pady=(12, 0))
        self._small_btn(btns, "✎  Sửa")
        self._small_btn(btns,
                        "★  Bỏ đánh dấu" if note["starred"] else "☆  Đánh dấu")
        self._small_btn(btns, "×  Xóa", danger=True)

        # Nhãn + ngày tạo
        meta = ctk.CTkFrame(self.detail, fg_color="transparent")
        meta.grid(row=1, column=0, sticky="w", padx=22, pady=(0, 12))
        self._pill(meta, note["label"], size=12).pack(side="left")
        ctk.CTkLabel(meta, text="   " + note["created"],
                     text_color=MUTED, font=FONT_TINY).pack(side="left")

        # Đường kẻ phân cách
        ctk.CTkFrame(self.detail, height=1, fg_color=BORDER).grid(
            row=2, column=0, sticky="ew", padx=22, pady=(0, 4))

        # Nội dung
        box = ctk.CTkTextbox(self.detail, fg_color="transparent",
                             text_color=TEXT, border_width=0,
                             font=FONT_CONTENT, wrap="word")
        box.grid(row=3, column=0, sticky="nsew", padx=14, pady=(4, 14))
        box.insert("1.0", note["content"])
        box.configure(state="disabled")

    # ── Tiện ích UI ─────────────────────────────────────────────────────────
    def _pill(self, parent, label, size=11):
        lb = LABELS.get(label, LABELS["Khác"])
        return ctk.CTkLabel(parent, text=label, corner_radius=5, height=22,
                            fg_color=(lb[0], lb[2]), text_color=(lb[1], lb[3]),
                            font=("Segoe UI", size, "bold"), padx=8)

    def _small_btn(self, parent, text, danger=False):
        width = max(76, len(text) * 8 + 20)
        ctk.CTkButton(
            parent, text=text, width=width, height=32, corner_radius=5,
            fg_color=DANGER_BUTTON  if danger else NEUTRAL_BUTTON,
            text_color=DANGER_TEXT  if danger else TEXT,
            hover_color=DANGER_HOVER if danger else NEUTRAL_HOVER,
            font=FONT_TINY,
        ).pack(side="left", padx=(0, 7))
