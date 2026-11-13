# config.py — Cấu hình toàn cục

import os
from dotenv import load_dotenv  # type: ignore

load_dotenv()

# ─── MongoDB ──────────────────────────────────────────────────────────────────
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
DB_NAME     = "mynote_db"
COL_USERS   = "users"
COL_NOTES   = "notes"

# ─── Cửa sổ ───────────────────────────────────────────────────────────────────
WIN_TITLE   = "Ứng dụng Ghi chú Cá nhân"
WIN_SIZE    = "1180x720"
WIN_MINSIZE = (980, 600)

# ─── Font ─────────────────────────────────────────────────────────────────────
FONT_FAMILY   = "Segoe UI"
FONT_TITLE    = ("Segoe UI", 22, "bold")
FONT_HEADING  = ("Segoe UI", 14, "bold")
FONT_LABEL    = ("Segoe UI", 13, "bold")
FONT_BODY     = ("Segoe UI", 13)
FONT_SMALL    = ("Segoe UI", 12)
FONT_TINY     = ("Segoe UI", 11)
FONT_CONTENT  = ("Segoe UI", 14)
FONT_NAV      = ("Segoe UI", 10, "bold")

# ─── Màu sắc (light, dark) ───────────────────────────────────────────────────
ACCENT          = ("#496C8B", "#89A9C6")
ACCENT_HOVER    = ("#3D5E7C", "#7394B1")

SIDEBAR         = ("#F0F3F5", "#191E24")
MAIN_BG         = ("#F7F8FA", "#12171D")
SURFACE         = ("#FFFFFF", "#1B222A")
SURFACE_HOVER   = ("#F0F3F6", "#242D37")
SELECTED        = ("#E3EBF2", "#2B3A49")
BORDER          = ("#DCE2E8", "#303A45")

TEXT            = ("#28333E", "#E3E8ED")
MUTED           = ("#73808D", "#9AA6B2")

NEUTRAL_BUTTON  = ("#E9EDF1", "#28323D")
NEUTRAL_HOVER   = ("#DDE3E9", "#35414D")

DANGER_BUTTON   = ("#F5E9E8", "#422C2D")
DANGER_HOVER    = ("#EED9D7", "#563536")
DANGER_TEXT     = ("#9D4E49", "#E4AAA5")

ERROR_COLOR     = "#D92D20"

# ─── Nhãn ghi chú: (bg_light, text_light, bg_dark, text_dark) ────────────────
LABELS = {
    "Công việc": ("#E7EFE9", "#496852", "#293B30", "#B6D1BD"),
    "Học tập":   ("#E7EDF4", "#49627D", "#293746", "#B7C9DD"),
    "Cá nhân":   ("#EEE9F1", "#6B5A76", "#392F40", "#CDBED5"),
    "Khác":      ("#F1ECE4", "#76664D", "#40382C", "#D3C3A6"),
}

# ─── Bộ lọc sidebar ───────────────────────────────────────────────────────────
FILTERS = [
    "Tất cả ghi chú",
    "Công việc",
    "Học tập",
    "Cá nhân",
    "Khác",
    "Đánh dấu",
    "Thùng rác",
]

FILTER_ICONS = {
    "Tất cả ghi chú": "▤",
    "Công việc":      "□",
    "Học tập":        "▧",
    "Cá nhân":        "○",
    "Khác":           "◇",
    "Đánh dấu":       "☆",
    "Thùng rác":      "▥",
}
