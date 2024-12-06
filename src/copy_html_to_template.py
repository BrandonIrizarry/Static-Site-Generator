import sys
import re


def extract_header_element(source_html_filename):
    """Extract contents of h1 element found in 'source_html_filename' to
    use in final output's title element.

    Return a tuple of the title, paired with the contents of the
    source html file.

    """
    with open(source_html_filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
        title = None

        for line in lines:
            if (m := re.match("<h1>(.+?)</h1>", line)):
                title = m.group(1)
                break

        if title is None:
            raise RuntimeError("Missing title")

        return (title, "".join(lines))


def get_modified_html_template(template_filename, source_html_filename):
    """Copy contents of 'source_html_filename' into
    'template_filename', generating a complete HTML file.

    """
    title, html_content = extract_header_element(source_html_filename)

    with open(template_filename, "r", encoding="utf-8") as f:
        template_content = f.read()

        template_content = re.sub(r"{{\s+Title\s+}}", title, template_content)

        template_content = re.sub(r"{{\s+Content\s+}}",
                                  html_content,
                                  template_content)

        return template_content


if __name__ == "__main__":
    template_filename = sys.argv[1]
    source_html_filename = sys.argv[2]
    destination_html_filefname = sys.argv[3]

    modified_template = get_modified_html_template(template_filename,
                                                   source_html_filename)

    with open(destination_html_filefname, "w", encoding="utf-8") as f:
        f.write(modified_template)
