import os
import pathlib
import hashlib
import json
from datetime import datetime, timezone
import shutil

BASE_DIR = pathlib.Path('./vmss')   # Base directory for the VMSS
META_DIR = pathlib.Path('./meta_commits')  # Directory to store meta-commits


def hash_content(content: bytes) -> str:
    """Create a SHA-256 hash of the given content."""
    return hashlib.sha256(content).hexdigest()

def rgb_from_hash(hash_hex: str) -> tuple:
    """Convert the first 6 characters of the hash into RGB color values."""
    # Ensure we have a valid hash string
    if not hash_hex or len(hash_hex) < 6:
        return (0, 0, 0)  # Return black for invalid or empty hash
    return (
        int(hash_hex[:2], 16),  # Red component
        int(hash_hex[2:4], 16), # Green component
        int(hash_hex[4:6], 16)  # Blue component
    )

def hash_directory(dir_path):
    """Create a hash combining the contents of .py files and other specified files within a directory."""
    hasher = hashlib.sha256()
    for path in pathlib.Path(dir_path).rglob('*'):
        if path.is_file() and path.suffix in {'.py', ',*'} and path.name != '__init__.py':
            with path.open('rb') as f:
                hasher.update(f.read())
    return hasher.hexdigest() if hasher.digest() else None

def get_spectral_name(index: int) -> str:
    """Generate a spectral name based on index."""
    spectral_names = ['infrared', 'red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet', 'ultraviolet']
    return spectral_names[index % len(spectral_names)]

class MetaCommitManager:
    def __init__(self):
        self.commits = []  # Stores meta-commits
        self.load_meta_commits()

    def load_meta_commits(self):
        """Load meta-commits from storage if available."""
        META_DIR.mkdir(parents=True, exist_ok=True)
        meta_file_path = META_DIR / "commits.json"
        if meta_file_path.exists():
            with meta_file_path.open('r') as f:
                self.commits = json.load(f)

    def save_meta_commits(self):
        """Persist the current commit list."""
        meta_file_path = META_DIR / "commits.json"
        with meta_file_path.open('w') as f:
            json.dump(self.commits, f, indent=4)

    def create_meta_commit(self):
        """Create a new meta-commit."""
        state_hash = self.generate_merkle_root()
        if state_hash is None:
            print("No valid files found for hashing; cannot create commit.")
            return None  # Or handle differently if desired

        spectral_name = get_spectral_name(len(self.commits))
        timestamp = datetime.now(timezone.utc).isoformat()
        rgb_value = rgb_from_hash(state_hash)

        meta_commit = {
            "spectral_name": spectral_name,
            "hash": state_hash,
            "timestamp": timestamp,
            "rgb": rgb_value
        }

        self.commits.append(meta_commit)
        self.save_meta_commits()
        return meta_commit

    def generate_merkle_root(self):
        """Generate a Merkle root from VMSS files."""
        file_hashes = []
        for root, _, files in os.walk(BASE_DIR):
            for file in files:
                file_path = pathlib.Path(root) / file
                if file_path.suffix in {'.py', ',*'} and file_path.name != '__init__.py':
                    with file_path.open('rb') as f:
                        file_hashes.append(hash_content(f.read()))

        if not file_hashes:
            print("Warning: No files found for hashing.")
            return None

        return self._merkle_root(file_hashes)

    def _merkle_root(self, hashes):
        """Compute the Merkle root from a list of hashes."""
        if not hashes:
            return None  # Return a standard empty hash or None for an empty list
        
        if len(hashes) == 1:
            return hashes[0]

        # Ensure the list has an even number of elements
        if len(hashes) % 2 == 1:
            # Duplicate last hash to make pair
            hashes.append(hashes[-1])

        # Create a new level of hashes
        new_level = []
        for i in range(0, len(hashes), 2):
            combined_hash = hash_content((hashes[i] + hashes[i+1]).encode())
            new_level.append(combined_hash)

        return self._merkle_root(new_level)

def initialize_vmss_structure():
    """Setup the VMSS with directories for each byte of a 16-bit word."""
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    # Create directories for each possible high byte (00-FF)
    for high_byte in range(0x100):
        dir_path = BASE_DIR / f"{high_byte:02x}"
        dir_path.mkdir(parents=True, exist_ok=True)

        # Create subdirectories for each possible low byte (00-FF)
        for low_byte in range(0x100):
            sub_dir_path = dir_path / f"{low_byte:02x}"
            sub_dir_path.mkdir(parents=True, exist_ok=True)

            # Optionally initialize a __init__.py in each subdirectory
            init_file_path = sub_dir_path / "__init__.py"
            if not init_file_path.exists():
                init_file_path.write_text("# Initialization logic might go here.\n")

def collapse_vmss():
    """Collapse directory structure by removing inactive directories."""
    inactive_dirs = []
    for subdir in BASE_DIR.iterdir():
        if subdir.is_dir():
            non_empty = False
            # Check for presence of .py or ,* files
            for path in subdir.rglob('*'):
                if path.is_file() and path.suffix in {'.py', ',*'} and path.name != '__init__.py':
                    non_empty = True
                    break
            
            if not non_empty:
                print(f"Collapsing inactive directory: {subdir}")
                shutil.rmtree(subdir)  # Remove inactive directory
                inactive_dirs.append(subdir)
    return inactive_dirs

def main():
    BASE_DIR.mkdir(parents=True, exist_ok=True)

    meta_commit_mgr = MetaCommitManager()
    initialize_vmss_structure()
    print(f"VMSS structure initialized under {BASE_DIR}.")

    # Perform the collapse to remove inactive directories
    collapsed_dirs = collapse_vmss()
    print("Collapsed directories:", collapsed_dirs)

    # Create a new meta-commit to document current VMSS state
    new_commit = meta_commit_mgr.create_meta_commit()
    if new_commit is not None:
        print(f"Created new meta commit: {new_commit['spectral_name']} (RGB: {new_commit['rgb']})")


if __name__ == "__main__":
    main()