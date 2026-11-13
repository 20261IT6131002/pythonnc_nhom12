# main.py — Entry point: khởi tạo cửa sổ và điều hướng màn hình

import customtkinter as ctk
from config import WIN_TITLE, WIN_SIZE, WIN_MINSIZE
from views.login_view    import LoginView
from views.register_view import RegisterView
from views.main_view     import MainView


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        self.title(WIN_TITLE)
        self.geometry(WIN_SIZE)
        self.minsize(*WIN_MINSIZE)
        self._current_view = None
        self.show_login()

    # ── Điều hướng ──────────────────────────────────────────────────────────
    def _clear(self):
        if self._current_view:
            self._current_view.destroy()
            self._current_view = None

    def show_login(self):
        self._clear()
        view = LoginView(
            self,
            on_login=lambda: self.show_main(),   # tạm: vào thẳng MainView
            on_register=self.show_register,
        )
        view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._current_view = view

    def show_register(self):
        self._clear()
        view = RegisterView(
            self,
            on_register=self.show_login,         # tạm: sau đăng ký → về Login
            on_back=self.show_login,
        )
        view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._current_view = view

    def show_main(self, user=None):
        self._clear()
        view = MainView(
            self,
            user=user,
            on_logout=self.show_login,
        )
        view.place(relx=0, rely=0, relwidth=1, relheight=1)
        self._current_view = view


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = App()
    # Bỏ comment dòng dưới để xem thẳng MainView khi thiết kế:
    # app.show_main()
    app.mainloop()
