"""
Create new file respecting file structure.
arg:
	content: current file name with content
    fileName: new file name.
Rename content to fileName.
"""

import os
import sys
import shutil

def create_or_replace_file(source: str, destination: str) -> None:
    """Create new file or replace existing file with new content."""
    try:
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(source, destination)
    except Exception:
        raise

if __name__ == "__main__":
    content_file = sys.argv[1]
    new_file = sys.argv[2]
    create_or_replace_file(content_file, new_file)
    sys.exit(0)
