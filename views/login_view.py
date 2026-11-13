# views/login_view.py — Màn hình đăng nhập

import customtkinter as ctk
from config import (
    ACCENT, ACCENT_HOVER, MAIN_BG, SURFACE, SURFACE_HOVER, BORDER,
    TEXT, MUTED, ERROR_COLOR,
    FONT_TITLE, FONT_LABEL, FONT_SMALL, FONT_TINY,
)


class LoginView(ctk.CTkFrame):
    """Màn hình đăng nhập."""

    def __init__(self, master, on_login=None, on_register=None):
        super().__init__(master, fg_color=MAIN_BG, corner_radius=0)
        self.on_login    = on_login    or (lambda: None)
        self.on_register = on_register or (lambda: None)
        self._build()

    def _build(self):
        card = ctk.CTkFrame(self, fg_color=SURFACE, corner_radius=14,
                            border_width=1, border_color=BORDER,
                            width=400, height=460)
        card.place(relx=0.5, rely=0.5, anchor="center")
        card.grid_propagate(False)

        # Logo
        ctk.CTkLabel(card, text="📝", font=("Segoe UI", 44)).pack(pady=(40, 4))
        ctk.CTkLabel(card, text="Ghi chú", font=FONT_TITLE,
                     text_color=TEXT).pack()
        ctk.CTkLabel(card, text="Đăng nhập để tiếp tục",
                     font=FONT_SMALL, text_color=MUTED).pack(pady=(2, 28))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=36)

        # Username
        ctk.CTkLabel(inner, text="Tên đăng nhập", anchor="w",
                     font=FONT_LABEL, text_color=TEXT).pack(fill="x")
        ctk.CTkEntry(inner, height=38, corner_radius=6,
                     border_color=BORDER, fg_color=SURFACE, text_color=TEXT,
                     placeholder_text="Nhập tên đăng nhập...",
                     placeholder_text_color=MUTED).pack(fill="x", pady=(4, 14))

        # Password
        ctk.CTkLabel(inner, text="Mật khẩu", anchor="w",
                     font=FONT_LABEL, text_color=TEXT).pack(fill="x")
        ctk.CTkEntry(inner, height=38, corner_radius=6,
                     border_color=BORDER, fg_color=SURFACE, text_color=TEXT,
                     show="●",
                     placeholder_text="Nhập mật khẩu...",
                     placeholder_text_color=MUTED).pack(fill="x", pady=(4, 6))

        # Thông báo lỗi (placeholder)
        ctk.CTkLabel(inner, text="", text_color=ERROR_COLOR,
                     font=FONT_TINY).pack(fill="x", pady=(0, 10))

        # Nút đăng nhập → tạm thời vào thẳng MainView
        ctk.CTkButton(inner, text="Đăng nhập", height=40, corner_radius=6,
                      fg_color=ACCENT, hover_color=ACCENT_HOVER,
                      text_color=("white", "#101820"),
                      font=FONT_LABEL,
                      command=self.on_login).pack(fill="x")

        # Link → Đăng ký
        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(pady=(16, 0))
        ctk.CTkLabel(row, text="Chưa có tài khoản?",
                     font=FONT_SMALL, text_color=MUTED).pack(side="left")
        ctk.CTkButton(row, text="Đăng ký", width=66, height=28,
                      fg_color="transparent", hover_color=SURFACE_HOVER,
                      text_color=ACCENT, font=("Segoe UI", 12, "bold"),
                      border_width=0,
                      command=self.on_register).pack(side="left", padx=(4, 0))
