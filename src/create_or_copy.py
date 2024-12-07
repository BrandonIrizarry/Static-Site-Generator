import os
import shutil
import re
import argparse

from main import run


def get_extension(filename):
    b = os.path.basename(filename)
    parts = b.split(".")
    return parts[-1]


def create_or_copy(source_root,
                   dest_root,
                   sub_path,
                   template_path=None,
                   bootstrap_flag=False):
    """Copy all data from 'source_root' to 'dest_root', keeping track
    of the current sub-path common to both of them (the third
    argument.)

    The presence of a template implies we're to convert Markdown files
    we see first into HTML, using the template.

    """
    source_path = f"{source_root}{sub_path}"
    dest_path = f"{dest_root}{sub_path}"

    # If the destination path exists, delete it completely.
    if os.path.exists(dest_path) and bootstrap_flag:
        shutil.rmtree(dest_path)

    # Make 'os.mkdir' a bit more like the shell's 'mkdir'.
    if not os.path.exists(dest_path):
        os.mkdir(dest_path)

    paths = os.listdir(source_path)

    for entry in paths:
        full_source_path = f"{source_path}{entry}"

        if os.path.isdir(full_source_path):
            # 'source_path' must always end with a slash.
            create_or_copy(source_root,
                           dest_root,
                           f"{sub_path}{entry}/",
                           template_path)
        else:
            full_dest_path = f"{dest_path}{entry}"
            extension = get_extension(full_source_path)

            # A True 'conversion_flag' value means we're trying to
            # copy Markdown from the 'content' directory, but we
            # subvert this (whenever it happens) by first converting
            # the Markdown to HTML, and copying that instead.
            if template_path and extension == "md":
                # We generate the HTML into the same 'content'
                # directory, so that it gets copied over in the same
                # path-respecting manner as the rest of the stuff.
                html_source_path = re.sub(r"\.md$", ".html", full_source_path)
                html_dest_path = re.sub(r"\.md$", ".html", full_dest_path)

                run(full_source_path, html_source_path, template_path)
                shutil.copy(html_source_path, html_dest_path)
            else:
                shutil.copy(full_source_path, full_dest_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Copy static and built artifacts into a public directory."
    )

    parser.add_argument("source_root",
                        type=str)

    parser.add_argument("dest_root",
                        type=str)

    parser.add_argument("--template",
                        type=str)

    parser.add_argument("--bootstrap",
                        help="Obliterate the existing 'public' directory",
                        action="store_true")

    args = parser.parse_args()

    create_or_copy(
        args.source_root,
        args.dest_root,
        "/",
        args.template,
        args.bootstrap
    )
