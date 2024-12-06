import os
import shutil
import sys


def create_or_copy(source_root, dest_root, sub_path):
    """Copy all data from 'source_root' to 'dest_root', keeping track
    of the current sub-path common to both of them (the third
    argument.)

    """
    source_path = f"{source_root}{sub_path}"
    dest_path = f"{dest_root}{sub_path}"

    # If the destination path exists, delete it completely.
    if os.path.exists(dest_path):
        shutil.rmtree(dest_path)

    # Note that we have to create 'public' even if it existed before,
    # because we therefore deleted it in the previous if-statement.
    os.mkdir(dest_path)

    paths = os.listdir(source_path)

    for entry in paths:
        full_source_path = f"{source_path}{entry}"

        if os.path.isdir(full_source_path):
            # 'source_path' must always end with a slash.
            create_or_copy(source_root, dest_root, f"{sub_path}{entry}/")
        else:
            full_dest_path = f"{dest_path}{entry}"
            shutil.copy(full_source_path, full_dest_path)


if __name__ == "__main__":
    source_root = sys.argv[1]
    dest_root = sys.argv[2]

    create_or_copy(source_root, dest_root, "/")
