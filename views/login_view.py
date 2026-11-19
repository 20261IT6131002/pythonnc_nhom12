import customtkinter as ctk

from config import (
    ACCENT,
    ACCENT_HOVER,
    BORDER,
    ERROR_COLOR,
    FONT_FAMILY,
    FONT_SMALL,
    FONT_TINY,
    FONT_TITLE,
    MAIN_BG,
    MUTED,
    SURFACE,
    SURFACE_HOVER,
    TEXT,
)
from controllers.auth_controller import AuthController
from models.user import User


class LoginView(ctk.CTkFrame):
    def __init__(self, master, on_login, on_switch_register, on_toggle_mode=None, error: str = ""):
        super().__init__(master, fg_color="transparent")
        self.on_login = on_login
        self.on_switch_register = on_switch_register
        self.on_toggle_mode = on_toggle_mode

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        card = ctk.CTkFrame(
            self,
            width=440,
            corner_radius=10,
            fg_color=SURFACE,
            border_width=1,
            border_color=BORDER,
        )
        card.grid(row=0, column=0, padx=24, pady=24)
        card.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            card,
            text="Ghi chú",
            text_color=ACCENT,
            font=(FONT_FAMILY, 13, "bold"),
        ).pack(pady=(28, 4))

        ctk.CTkLabel(
            card,
            text="Chào mừng trở lại",
            text_color=TEXT,
            font=FONT_TITLE,
        ).pack(pady=(0, 4))

        ctk.CTkLabel(
            card,
            text="Đăng nhập để xem các ghi chú của bạn trên thiết bị này.",
            text_color=MUTED,
            font=FONT_SMALL,
            wraplength=360,
        ).pack(padx=30, pady=(0, 22))

        ctk.CTkLabel(
            card,
            text="Tên đăng nhập",
            anchor="w",
            text_color=TEXT,
            font=(FONT_FAMILY, 12, "bold"),
        ).pack(fill="x", padx=32, pady=(0, 5))

        self.username_entry = ctk.CTkEntry(
            card,
            height=40,
            corner_radius=5,
            border_color=BORDER,
            fg_color=MAIN_BG,
            text_color=TEXT,
            placeholder_text="ten_dang_nhap",
        )
        self.username_entry.pack(fill="x", padx=32, pady=(0, 14))

        ctk.CTkLabel(
            card,
            text="Mật khẩu",
            anchor="w",
            text_color=TEXT,
            font=(FONT_FAMILY, 12, "bold"),
        ).pack(fill="x", padx=32, pady=(0, 5))

        self.password_entry = ctk.CTkEntry(
            card,
            height=40,
            corner_radius=5,
            border_color=BORDER,
            fg_color=MAIN_BG,
            text_color=TEXT,
            show="•",
            placeholder_text="Nhập mật khẩu",
        )
        self.password_entry.pack(fill="x", padx=32, pady=(0, 12))

        self.show_password = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(
            card,
            text="Hiện mật khẩu",
            variable=self.show_password,
            text_color=MUTED,
            fg_color=ACCENT,
            hover_color=ACCENT,
            font=FONT_TINY,
            command=self._toggle_password_visibility,
        ).pack(anchor="w", padx=32, pady=(0, 10))

        self.error_label = ctk.CTkLabel(
            card,
            text=error,
            text_color=ERROR_COLOR,
            font=FONT_TINY,
            wraplength=360,
        )
        self.error_label.pack(fill="x", padx=32, pady=(0, 8))

        ctk.CTkButton(
            card,
            text="Đăng nhập",
            height=42,
            corner_radius=5,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color=("white", "#101820"),
            font=(FONT_FAMILY, 13, "bold"),
            command=self._submit,
        ).pack(fill="x", padx=32, pady=(0, 14))

        ctk.CTkButton(
            card,
            text="Chưa có tài khoản?  Đăng ký",
            height=32,
            corner_radius=5,
            fg_color="transparent",
            hover_color=SURFACE_HOVER,
            text_color=ACCENT,
            font=FONT_TINY,
            command=self.on_switch_register,
        ).pack(fill="x", padx=32, pady=(0, 18))

        self.mode_switch = ctk.CTkSwitch(
            card,
            text="Chế độ tối",
            text_color=MUTED,
            command=self._toggle_mode,
            progress_color=ACCENT,
            font=FONT_TINY,
        )
        if ctk.get_appearance_mode().lower() == "dark":
            self.mode_switch.select()
        self.mode_switch.pack(anchor="center", pady=(0, 22))

    def _toggle_password_visibility(self):
        self.password_entry.configure(show="" if self.show_password.get() else "•")

    def _toggle_mode(self):
        if callable(self.on_toggle_mode):
            self.on_toggle_mode()
        else:
            ctk.set_appearance_mode("dark" if self.mode_switch.get() else "light")

    def _submit(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        user, err = AuthController.login(username, password)
        if isinstance(user, User):
            self.error_label.configure(text="")
            self.on_login(user)
        else:
            self.error_label.configure(text=err or "Tên đăng nhập hoặc mật khẩu không chính xác.")