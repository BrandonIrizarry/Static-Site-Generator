import os


root_dir = os.path.expanduser("~/boot_dev/Static_Site_Generator")
public_dir = f"{root_dir}/public"
static_dir = f"{root_dir}/static"
content_source = f"{root_dir}/content/index.md"
template_source = f"{root_dir}/template.html"

print(f"""
root_dir: {root_dir}
public_dir: {public_dir}
static_dir: {static_dir}
content_source: {content_source}
template_source: {template_source}
""")
