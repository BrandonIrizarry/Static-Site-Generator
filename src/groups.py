import os
import re


def get_markdown_file_content(nickname: str) -> str:
    markdown_filename = os.path.expanduser(
        f"~/boot_dev/Static_Site_Generator/content/{nickname}.md"
    )

    with open(markdown_filename, "r", encoding="utf-8") as markdown_file:
        markdown_text = markdown_file.read()

        return markdown_text


text = """
* list item 1
continuation of 1
* list item 2
continuation of 2
"""

blocks = text.split("\n\n")
splits = [block.strip().split("\n") for block in blocks]

print(splits)
