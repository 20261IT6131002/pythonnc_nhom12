# views/register_view.py — Màn hình đăng ký

import customtkinter as ctk
from config import (
    ACCENT, ACCENT_HOVER, MAIN_BG, SURFACE, SURFACE_HOVER, BORDER,
    TEXT, MUTED, ERROR_COLOR,
    FONT_TITLE, FONT_LABEL, FONT_SMALL, FONT_TINY,
)


class RegisterView(ctk.CTkFrame):
    """Màn hình đăng ký tài khoản."""

    def __init__(self, master, on_register=None, on_back=None):
        super().__init__(master, fg_color=MAIN_BG, corner_radius=0)
        self.on_register = on_register or (lambda: None)
        self.on_back     = on_back     or (lambda: None)
        self._build()

    def _build(self):
        card = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14,
                            border_width=1, border_color=BORDER,
                            width=400, height=560)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.grid_propagate(False)

        ctk.CTkLabel(card, text="📝", font=("Segoe UI", 40)).pack(pady=(36, 4))
        ctk.CTkLabel(card, text="Tạo tài khoản", font=FONT_TITLE,
                     text_color=TEXT).pack()
        ctk.CTkLabel(card, text="Điền thông tin để bắt đầu",
                     font=FONT_SMALL, text_color=MUTED).pack(pady=(2, 24))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=36)

        fields = [
            ("Họ và tên",          "Nhập họ và tên...",        False),
            ("Tên đăng nhập",      "Nhập tên đăng nhập...",    False),
            ("Mật khẩu",           "Tạo mật khẩu...",          True),
            ("Nhập lại mật khẩu",  "Nhập lại mật khẩu...",     True),
        ]
        for lbl, ph, hidden in fields:
            ctk.CTkLabel(inner, text=lbl, anchor="w",
                         font=FONT_LABEL, text_color=TEXT).pack(fill="x")
            kw = {"show": "●"} if hidden else {}
            ctk.CTkEntry(inner, height=36, corner_radius=6,
                         border_color=BORDER, fg_color=SURFACE, text_color=TEXT,
                         placeholder_text=ph, placeholder_text_color=MUTED,
                         **kw).pack(fill="x", pady=(4, 10))

        ctk.CTkLabel(inner, text="", text_color=ERROR_COLOR,
                     font=FONT_TINY).pack(fill="x", pady=(0, 6))

        ctk.CTkButton(inner, text="Đăng ký", height=40, corner_radius=6,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      text_color=("white", "#101820"),
                      font=FONT_LABEL,
                      command=self.on_register).pack(fill="x")

        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(pady=(14, 0))
        ctk.CTkLabel(row, text="Đã có tài khoản?",
                     font=FONT_SMALL, text_color=MUTED).pack(side="left")
        ctk.CTkButton(row, text="Đăng nhập", width=80, height=28,
                      fg_color="transparent", hover_color=SURFACE_HOVER,
                      text_color=ACCENT, font=("Segoe UI", 12, "bold"),
                      border_width=0,
                      command=self.on_back).pack(side="left", padx=(4, 0))
