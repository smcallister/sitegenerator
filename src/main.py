import os
import shutil

from conversions import markdown_to_html_node
from nodefunctions import extract_title

def copy_directory(source, dest):
    # Create the destination if it doesn't exist already.
    if not os.path.exists(dest):
        print(f"Creating directory {dest}")
        os.mkdir(dest)
    
    # Enumerate all files in the source directory.
    files = os.listdir(source)
    for file in files:
        # Build the full path to the source and destination file.
        source_file = os.path.join(source, file)
        dest_file = os.path.join(dest, file)

        # If this item is a file, copy it.
        if os.path.isfile(source_file):
            print(f"Copying file from {source_file} to {dest_file}")
            shutil.copy(source_file, dest_file)
        
        # Otherwise, copy the directory.
        else:
            copy_directory(source_file, dest_file)

def generate_page(source_path, template_path, dest_path):
    # Read the source markdown and template.
    print(f"Generating page from {source_path} to {dest_path} using {template_path}")
    with open(source_path) as source_file:
        source_contents = source_file.read()

    with open(template_path) as template_file:
        template_contents = template_file.read()
    
    # Convert the markdown into HTML and write it into the template.
    html_node = markdown_to_html_node(source_contents)
    title = extract_title(source_contents)
    content = template_contents.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html())

    # Write the template to a file.
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as dest_file:
        dest_file.write(content)

def generate_pages(source_path, template_path, dest_path):
    # Enumerate all files in the source directory.
    files = os.listdir(source_path)
    for file in files:
        # Build the full path to the source and destination file.
        source_file = os.path.join(source_path, file)
        dest_file = os.path.join(dest_path, file.replace(".md", ".html"))

        # If this item is a file, generate HTML from it
        if os.path.isfile(source_file):
            generate_page(source_file, template_path, dest_file)
        
        # Otherwise, generate pages in the subdirectory.
        else:
            generate_pages(source_file, template_path, dest_file)

def main():
    # Set up the public directory.
    shutil.rmtree("public")
    copy_directory("static", "public")

    # Generate pages.
    generate_pages("content", "template.html", "public")

if __name__ == "__main__":
    main()