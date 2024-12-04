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


def split_line_group_into_words(line_group: list[str]) -> list[list[str]]:
    return list(map(lambda line: line.split(" "), line_group))


line_groups = list(map(split_block_into_lines, blocks))


for line_group in line_groups:
    print(split_line_group_into_words(line_group))
