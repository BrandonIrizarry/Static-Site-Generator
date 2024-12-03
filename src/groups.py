import os


markdown_filename = os.path.expanduser(
    "~/boot_dev/Static_Site_Generator/content/tolkien.md"
)


with open(markdown_filename, "r", encoding="utf-8") as markdown_file:
    markdown_text = markdown_file.read()

    print(markdown_text)
