import os
import argparse
import re
from enum import IntEnum, auto
from collections import defaultdict
from typing import Callable, TypeAlias


class Tag(IntEnum):
    """An enum used to classify Markdown blocks in terms of HTML block
    elements.

    """
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


Block: TypeAlias = tuple[Tag, list[list[str]]]


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
    """Identify a Markdown block according to Markdown syntax."""
    key = defaultdict(lambda: Tag.P, {
        "*": Tag.UL,
        "-": Tag.UL,
        "#": Tag.H1,
        "##": Tag.H2,
        "###": Tag.H3,
        "####": Tag.H4,
        "#####": Tag.H5,
        "######": Tag.H6,
        "```": Tag.PRE_CODE,
        ">": Tag.BLOCKQUOTE
    })

    if re.match(r"\d+\.", token):
        return Tag.OL
    else:
        return key[token]


def make_tuples(group: list[list[str]]):
    """Type-tag a Markdown block according to what type of HTML block
    element it should represent.
    """
    first_token = group[0][0]
    tag = identify_block_type(first_token)

    # Remove extraneous Markdown artifacts previously used for parsing
    if tag == Tag.PRE_CODE:
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
    """Detach inline style markers from words in 'words'."""
    def split_and_remove_blanks(word) -> list[str]:
        splitted: list[str] = re.split(r"(\*\*|\*|`)", word)

        if splitted[0] == "":
            del splitted[0]

        if len(splitted) > 0 and splitted[-1] == "":
            del splitted[-1]

        return splitted

    return flatmap(words, split_and_remove_blanks)


def preprocess_typed_block(typed_block: Block):
    """Preprocess an already tagged Markdown block.

    1. Tokenize words further by inline style marker (*, **, etc)
    2. Consolidate multi-line list items into one list, such that each
    member of 'typed_block' now represents a single list item.

    """
    acc = []
    what: Tag = typed_block[0]

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


def generate_structure(text: str) -> list[Block]:
    blocks: list[str] = split_text_into_blocks(text)
    line_groups: list[list[str]] = list(map(split_block_into_lines, blocks))
    preprocessed: list[list[str]] = join_code_block_members(line_groups)

    word_tree: list[list[list[str]]] = list(map(create_word_groups,
                                                preprocessed))

    # Try to emulate a Lisp-style "let*" block.
    structure = (enum_tagged := map(make_tuples, word_tree),
                 list(map(preprocess_typed_block, enum_tagged)))[-1]

    return structure


def process_word_group(group: list[str]):
    acc = []
    inside_bold = False
    inside_italic = False
    inside_code = False

    for word in group:
        if word == "**":
            if inside_bold:
                acc.append("</b>")
            else:
                acc.append("<b>")

                inside_bold = not inside_bold
        elif word == "*":
            if inside_italic:
                acc.append("</i>")
            else:
                acc.append("<i>")

                inside_italic = not inside_italic
        elif word == "`":
            if inside_code:
                acc.append("</code>")
            else:
                acc.append("<code>")

                inside_code = not inside_code
        else:
            acc.append(word)

    # This form of the result surrounds even the HTML tags with
    # whitespace; we remove this in the next line, whose value we then
    # return.
    spaced_version = " ".join(acc)
    html_regex = r"<(?P<tagname>.+)>\s+(?P<content>.+)\s+</(?P=tagname)>"
    fixed_tags = re.sub(html_regex, r"<\g<tagname>>\g<content></\g<tagname>>", spaced_version)

    return fixed_tags


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse a Markdown file.")
    parser.add_argument("nickname",
                        type=str,
                        help="The name of the Markdown file (no file suffix)")

    args = parser.parse_args()
    nickname = args.nickname
    text: str = get_markdown_file_content(nickname)

    for i in generate_structure(text):
        print()
        print(i)
