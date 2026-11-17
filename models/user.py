
from dataclasses import dataclass


@dataclass
class User:
    id: str
    username: str
    fullname: str

    @staticmethod
    def from_dict(doc: dict) -> "User":
        return User(
            id=str(doc.get("_id", doc.get("id", ""))),
            username=doc.get("username", ""),
            fullname=doc.get("fullname", "")
        )


