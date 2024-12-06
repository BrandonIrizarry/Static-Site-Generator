import os
import argparse
import re
from enum import IntEnum, auto
from collections import defaultdict
from typing import Callable


class BlockType(IntEnum):
    H1 = auto()
    H2 = auto()
    H3 = auto()
    H4 = auto()
    H5 = auto()
    H6 = auto()
    OL = auto()
    UL = auto()
    PRE_CODE = auto()
    BLOCKQUOTE = auto()
    P = auto()

    def is_group(self):
        return self in (self.OL,
                        self.UL,
                        self.BLOCKQUOTE)

    def is_header(self):
        return self in range(self.H1, self.H6)


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


def create_word_groups(line_group: list[str]) -> list[list[str]]:
    """Tokenize 'line_group' into separate words."""
    word_groups = list(map(lambda line: re.split(r"\s+", line), line_group))

    return word_groups


def identify_block_type(token: str):
    key = defaultdict(lambda: BlockType.P, {
        "*": BlockType.UL,
        "-": BlockType.UL,
        "#": BlockType.H1,
        "##": BlockType.H2,
        "###": BlockType.H3,
        "####": BlockType.H4,
        "#####": BlockType.H5,
        "######": BlockType.H6,
        "```": BlockType.PRE_CODE,
        ">": BlockType.BLOCKQUOTE
    })

    if re.match(r"\d+\.", token):
        return BlockType.OL
    else:
        return key[token]


def make_tuples(group: list[list[str]]):
    first_token = group[0][0]
    tag = identify_block_type(first_token)

    # Remove extraneous Markdown artifacts previously used for parsing
    if tag == BlockType.PRE_CODE:
        group = group[1:]
    elif tag.is_header():
        if len(group) != 1:
            raise RuntimeError(f"Illegal header block with {len(group)} lines")

        group = [group[0][1:]]

    return (tag, group)


def flatmap(lst, fn: Callable[[str], list[str]]):
    """A flatmap function for Python lists of strings.

    Apply 'fn' to the members of 'lst', then flatten and return the
    result.

    """
    return [y for x in lst for y in fn(x)]


def tokenize_inline_style_markers(words: list[str]) -> list[str]:
    def split_and_remove_blanks(word) -> list[str]:
        splitted: list[str] = re.split(r"(\*\*|\*|`)", word)

        if splitted[0] == "":
            del splitted[0]

        if len(splitted) > 0 and splitted[-1] == "":
            del splitted[-1]

        return splitted

    return flatmap(words, split_and_remove_blanks)


def preprocess_typed_block(typed_block: tuple[BlockType, list[list[str]]]):
    """Preprocess an already tagged Markdown block.

    1. Tokenize words further by inline style marker (*, **, etc)
    2. Consolidate multi-line list items into one list, such that each
    member of 'typed_block' now represents a single list item.

    """
    acc = []
    what: BlockType = typed_block[0]

    if (not what.is_group()):
        for words in typed_block[1]:
            acc.append(words)
            acc[-1] = tokenize_inline_style_markers(acc[-1])
    else:
        groups = typed_block[1]

        for words in groups:
            token = words[0]
            pseudo_type = identify_block_type(token)

            if pseudo_type == what:
                # Here we can finally remove the various itemization
                # tokens (*, -, 1./2./3. etc, and >)
                acc.append(words[1:])
            else:
                acc[-1].extend(["\n"] + words)

            acc[-1] = tokenize_inline_style_markers(acc[-1])

    return (what, acc)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a Markdown file.")
    parser.add_argument("nickname",
                        type=str,
                        help="The name of the Markdown file (no file suffix)")

    args = parser.parse_args()
    nickname = args.nickname

    text: str = get_markdown_file_content(nickname)
    blocks: list[str] = split_text_into_blocks(text)
    line_groups: list[list[str]] = list(map(split_block_into_lines, blocks))
    preprocessed: list[list[str]] = join_code_block_members(line_groups)

    word_tree: list[list[list[str]]] = list(map(create_word_groups,
                                                preprocessed))

    enum_tagged = list(map(make_tuples, word_tree))
    enum_tagged = list(map(preprocess_typed_block, enum_tagged))

    for e in enum_tagged:
        print()
        print(e)
