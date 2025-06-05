from blocks import markdown_to_html_node
import os


def extract_title(markdown:str):
    # This only checks for h1 Headers
    if not markdown.startswith("#"):
        raise Exception("Not a proper header")
    return markdown.split("#")[1].split("\n")[0].strip()
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path) as f:
        src_file = f.read()
        
    with open(template_path) as f:
        templte_file = f.read()
        
    markdown = markdown_to_html_node(src_file).to_html()
    title = extract_title(src_file)
    
    with open(dest_path, "w") as f:
        f. write(templte_file.replace("{{ Title }}", title).replace("{{ Content }}", markdown))


def generate_pages_recursive(src_dir, template_path, dest_dir):
    for root, dirs, files in os.walk(src_dir):
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, src_dir)
                relative_path = os.path.splitext(rel_path)[0] + ".html"
                new_path = os.path.join(dest_dir, relative_path)
                os.makedirs(os.path.dirname(new_path), exist_ok=True)
                generate_page(full_path, template_path, new_path)


       