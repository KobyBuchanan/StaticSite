import os, shutil
from block_markdown import markdown_to_html_node
from pathlib import Path


dir_path_static = "./static"
dir_path_public = "./public"


def content_copy(source_path, destination_path):
    if not os.path.exists(destination_path):
        os.mkdir(destination_path)

    for filename in os.listdir(source_path):
        from_path = os.path.join(source_path, filename)
        dest_path = os.path.join(destination_path,filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path,dest_path)
        else:
            content_copy(from_path,dest_path)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def generate_page(source_path, template_path, dest_path):
    print(f"Generating page from {source_path} to {dest_path} using {template_path}")

    with open(source_path, "r") as f:
        markdown = f.read()

    with open(template_path, "r") as f:
        template = f.read()

    html_node = markdown_to_html_node(markdown)
    html = html_node.to_html()
    title = extract_title(markdown)

    with open(dest_path, "w") as f:
        f.write(template.replace("{{ Title }}",title).replace("{{ Content }}", html))


def generate_pages_recursive(source_path, template_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_path):
        from_path = os.path.join(source_path, filename)
        if os.path.isfile(from_path):
            if Path(from_path).suffix == ".md":
                dest_path = os.path.join(dest_dir_path, f"{Path(from_path).stem}.html")
                generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, os.path.join(dest_dir_path, filename))



def main():
    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")    
    content_copy(dir_path_static,dir_path_public)

    generate_pages_recursive("./content", "./template.html",dir_path_public)

main()
