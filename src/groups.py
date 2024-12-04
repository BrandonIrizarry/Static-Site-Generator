import os
import argparse
from enum import Enum, auto


def get_markdown_file_content(nickname: str) -> str:
    """Return contents of 'nickname'.md.

    This file should be found in the 'content' directory, under the
    project root.

    """
    markdown_filename = os.path.expanduser(
        f"~/boot_dev/Static_Site_Generator/content/{nickname}.md"
    )

    with open(markdown_filename, "r", encoding="utf-8") as markdown_file:
        markdown_text = markdown_file.read()

        return markdown_text


def split_text_into_blocks(text: str) -> list[str]:
    """Isolate 'text' into blocks which are more readily identifiable
    as Markdown entities."""
    return text.split("\n\n")


def split_block_into_lines(block: str) -> list[str]:
    """Split the given block into its component lines.

    This should aid in supporting multi-line list items, for example.

    """
    return block.strip().split("\n")


def join_code_block_members(line_groups: list[list[str]]) -> list[list[str]]:
    """For each code block, join the associated blocks as if they were
    originally a single block.

    We need this because code blocks themselves are literal text, and
    can contain their own spacing; so double-newline isn't sufficient
    for isolating them properly.

    """

    acc: list[list[str]] = []
    inside_code_block = False

    for lg in line_groups:
        # If this line group begins in "```", then we enter code block
        # mode, and so we append an empty list to our running result,
        # which will hold the line groups associated with the newly
        # detected code block.
        if lg[0] == "```":
            inside_code_block = True
            acc.append([])

        if inside_code_block:
            acc[-1].extend(lg)
        else:
            acc.append(lg)

        # If this line group ends in "```", then we exit code block
        # mode.
        #
        # Also, we don't need the final "```" for HTML conversion, so
        # get rid of it.
        if lg[-1] == "```":
            acc[-1].pop()
            inside_code_block = False

    return acc


class BlockType(Enum):
    H1 = 1
    H2 = 2
    H3 = 3
    H4 = 4
    H5 = 5
    H6 = 6
    OL = auto()
    UL = auto()
    PRE_CODE = auto()
    BLOCKQUOTE = auto()


def convert_line_group_to_tuple(line_group: list[str]):
    first_line = line_group[0]

    if first_line.startswith("1. "):
        return (BlockType.OL, line_group)
    elif first_line.startswith("* ") or first_line.startswith("- "):
        return (BlockType.UL, line_group)
    elif first_line.startswith("# "):
        return (BlockType.H1, line_group)
    elif first_line.startswith("## "):
        return (BlockType.H2, line_group)
    elif first_line.startswith("### "):
        return (BlockType.H3, line_group)
    elif first_line.startswith("#### "):
        return (BlockType.H4, line_group)
    elif first_line.startswith("##### "):
        return (BlockType.H5, line_group)
    elif first_line.startswith("###### "):
        return (BlockType.H6, line_group)
    elif first_line.startswith("```"):
        # The "```" doesn't add any more information at this point, so
        # get rid of it.
        return (BlockType.PRE_CODE, line_group[1:])
    elif first_line.startswith("> "):
        return (BlockType.BLOCKQUOTE, line_group)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a Markdown file.")
    parser.add_argument("nickname",
                        type=str,
                        help="The name of the Markdown file (no file suffix)")

    args = parser.parse_args()
    nickname = args.nickname

    text = get_markdown_file_content(nickname)
    blocks = split_text_into_blocks(text)
    line_groups: list[list[str]] = list(map(split_block_into_lines, blocks))
    preprocessed = join_code_block_members(line_groups)

    enum_tagged = list(map(convert_line_group_to_tuple, preprocessed))

    for e in enum_tagged:
        print()
        print(e)
