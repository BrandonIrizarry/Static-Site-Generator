import os


def get_markdown_file_content(nickname: str) -> str:
    markdown_filename = os.path.expanduser(
        f"~/boot_dev/Static_Site_Generator/content/{nickname}.md"
    )

    with open(markdown_filename, "r", encoding="utf-8") as markdown_file:
        markdown_text = markdown_file.read()

        return markdown_text


text = get_markdown_file_content("original_example")


def split_text_into_blocks(text: str) -> list[str]:
    return text.split("\n\n")


blocks = split_text_into_blocks(text)


def split_block_into_lines(block: str) -> list[str]:
    return block.strip().split("\n")


line_groups: list[list[str]] = list(map(split_block_into_lines, blocks))

acc: list[list[str]] = []
inside_code_block = False

for lg in line_groups:
    if lg[0] == "```":
        inside_code_block = True
        acc.append([])

    if inside_code_block:
        acc[-1].extend(lg)
    else:
        acc.append(lg)

    if lg[-1] == "```":
        inside_code_block = False

for lg in acc:
    print()
    print(lg)
