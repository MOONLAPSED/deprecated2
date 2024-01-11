import os
import logging
import pathlib
from time import time

"""
{
  'FileTypeSelector': {
    'Class Definition': {
      'Attributes': [
        'directory',
        'file_extension',
        'logger'
      ],
      'Methods': [
        'init',
        'select_files',
        'generate_markdown_content'
      ]
    },
    'Description': "This class helps you select files of a specific type from a directory...",
    'Usage': "Instantiate FileTypeSelector, set parameters, and call select_files to obtain file information."
  },
  'create_obsidian_folders': {
    'Parameters': [
      'base_folder',
      'folders'
    ],
    'Description': "Creates Obsidian-like folders and subfolders based on the crawled data.",
    'Usage': "Call this function with the base folder and a list of folders to create Obsidian-like structures."
  },
  'main': {
    'Logic': "Instantiate FileTypeSelector, crawl through the knowledge base, create Obsidian-like folders...",
    'Usage': "Execute the main function to run the script and perform the specified actions."
  }
}
"""

class FileTypeSelector:
    """
    This class helps you select files of a specific type from a directory.
    """
    def __init__(self, directory, file_extension, logger=None):
        """
        Instantiate FileTypeSelector, set parameters, and call select_files to obtain file information.
        """
        self.directory = directory
        self.file_extension = file_extension
        self.logger = logger or logging.getLogger(__name__)

    def select_files(self):
        """
        Selects files of a specific type from a directory.
        """
        self.logger.info(f"Selecting files from {self.directory} with extension {self.file_extension}...")
        start = time()
        files = []
        for file in pathlib.Path(self.directory).rglob(f"*.{self.file_extension}"):
            files.append(file)
        end = time()
        self.logger.info(f"Selected {len(files)} files in {end-start} seconds.")
        return files
    
    def generate_markdown_content(self, file):
        """
        Generates the content for a markdown file.
        """
        self.logger.info(f"Generating content for {file}...")
        start = time()
        with open(file, "r") as f:
            content = f.read()
        end = time()
        self.logger.info(f"Generated content in {end-start} seconds.")
        return content
    
    def write_markdown_file(self, file, content):
        """
        Writes the content to a markdown file.
        """
        self.logger.info(f"Writing content to {file}...")
        start = time()
        with open(file, "w") as f:
            f.write(content)
        end = time()
        self.logger.info(f"Wrote content in {end-start} seconds.")

    def create_obsidian_folders(self, base_folder, folders):
        """
        Creates Obsidian-like folders and subfolders based on the crawled data.
        """
        self.logger.info(f"Creating Obsidian-like folders and subfolders based on the crawled data...")
        start = time()
        for folder in folders:
            folder_path = os.path.join(base_folder, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
        end = time()
        self.logger.info(f"Created Obsidian-like folders and subfolders in {end-start} seconds.")
    
    def main(self):
        """
        Logic: Instantiate FileTypeSelector, crawl through the knowledge base, create Obsidian-like folders...
        Usage: Execute the main function to run the script and perform the specified actions.
        """
        self.logger.info("Executing main function...")
        start = time()
        files = self.select_files()
        for file in files:
            content = self.generate_markdown_content(file)
            self.write_markdown_file(file, content)
        self.create_obsidian_folders(self.directory, ["Folder 1", "Folder 2"])
        end = time()
        self.logger.info(f"Executed main function in {end-start} seconds.")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Instantiate and run FileTypeSelector
    fs = FileTypeSelector(directory="path_to_your_files", file_extension="txt")
    fs.main()
