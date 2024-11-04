from dataclasses import dataclass


@dataclass
class ImageDTO:
    filename: str
    content: bytes
    content_type: str
