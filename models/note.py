
from dataclasses import dataclass


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
    def from_dict(doc: dict) -> "Note":
        return Note(
            id=str(doc.get("_id", doc.get("id", ""))),
            user_id=str(doc.get("user_id", "")),
            title=doc.get("title", ""),
            label=doc.get("label", "Khác"),
            content=doc.get("content", ""),
            starred=doc.get("starred", False),
            deleted=doc.get("deleted", False),
            created=doc.get("created", "")
        )
