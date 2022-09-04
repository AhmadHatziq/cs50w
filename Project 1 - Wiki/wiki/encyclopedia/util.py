import re
import markdown 

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

def delete_entry(title): 
    """
    Delete the local .md file for a given title. 
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)

def get_entry(title):
    """
    Retrieves an encyclopedia entry (in HTML form) by its title. If no such
    entry exists, the function returns None.
    """
    filename = f"entries/{title}.md"
    with open(filename, 'r', encoding='utf8') as f:
        text = f.read()
        return markdown.markdown(text)

    try:
        f = default_storage.open(f"entries/{title}.md")
        markdown_raw = f.read().decode("utf-8")
        html_converted = markdown.markdown(markdown_raw)
        return html_converted
    except FileNotFoundError:
        return None

def get_entry_markdown(title): 
    """
    Retrieves an encyclopedia entry (in markdown form) by its title. If no such
    entry exists, the function returns None.
    """
    filename = f"entries/{title}.md"
    with open(filename, 'r', encoding='utf8') as f:
        text = f.read()
        
        return text
    try:
        f = default_storage.open(f"entries/{title}.md")
        markdown_raw = f.read().decode("utf-8")
        return markdown_raw
    except FileNotFoundError:
        return None