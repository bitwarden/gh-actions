from typing import List, Self


class FileFormat:
    name = "FileFormat"
    lines: List[str] = []

    def __init__(self, contents: str) -> None:
        self.lines = contents.split("\n")
