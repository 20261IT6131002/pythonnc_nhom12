"""Model ghi chú của ứng dụng MyNote."""

from dataclasses import dataclass
from typing import Any


@dataclass
class Note:
    id: str
    user_id: str
    title: str
    label: str
    content: str
    starred: bool
    deleted: bool
    created: str

    @staticmethod
    def from_dict(doc: dict[str, Any]) -> "Note":
        return Note(
            id=str(doc.get("_id", doc.get("id", ""))),
            user_id=str(doc.get("user_id", "")),
            title=str(doc.get("title", "")),
            label=str(doc.get("label", "Khác")),
            content=str(doc.get("content", "")),
            starred=bool(doc.get("starred", False)),
            deleted=bool(doc.get("deleted", False)),
            created=str(doc.get("created", "")),
        )

