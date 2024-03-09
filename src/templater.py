import pathlib

templater = '''\
import pathlib

def VaultLoader(vault_path):
    prompt = """\
    <%
    app.vault.getAllLoadedFiles()
    .filter(x => x instanceof tp.obsidian.TFolder)
    .map(x => x.name)
    \%>\n
    """


def VLOpath(VaultLoader):  # VaultLoader Object Path
    print(f"<% tp.obsidian.normalizePath(VaultLoader) \%>")
    return pathlib.Path(VaultLoader).absolute()

def headmatter():
    print(f'%)

def main():
    headmatter = 
'''
'''
import os
import shutil
from pathlib import Path

def migrate_media(vault_path, media_dir=".media"):
    """
    Migrates linked media files in an Obsidian vault to a dedicated media directory.

    Args:
        vault_path (str): Path to your Obsidian vault.
        media_dir (str): Name of the media directory (relative to the vault).
    """

    media_path = Path(vault_path) / media_dir
    media_path.mkdir(exist_ok=True)  # Create the media directory if needed

    # Iterate over Markdown files in the vault
    for md_file in vault_path.rglob("*.md"):
        with md_file.open("r+") as f:  # Open in read/write mode
            content = f.read()

            # Find linked media files (adjust the pattern if needed)
            for match in re.finditer(r"!\[\[(.*?)\]\]", content):
                original_path = Path(vault_path) / match.group(1)
                if original_path.exists():
                    # Calculate new filename (add hashing, metadata if desired)
                    new_filename = original_path.name 
                    new_path = media_path / new_filename

                    # Move the file
                    shutil.move(original_path, new_path)

                    # Update the link in the Markdown file
                    new_link = f"![[{media_dir}/{new_filename}]]"
                    content = content.replace(match.group(0), new_link)

            f.seek(0)  # Reset file pointer
            f.write(content)
            f.truncate() 

if __name__ == "__main__":
    vault_path = input("Enter your Obsidian vault path: ")
    migrate_media(vault_path)
'''