#! bin/python3
# defines the UFS data structure which wraps the shutil module's relevant classes and functions and methods for this project,
"""to-wrap:
FUNCTIONS
    chown(path, user=None, group=None)
        Change owner user and group of the given path.
        
        user and group can be the uid/gid or the user/group names, and in that case,
        they are converted to their respective uid/gid.
    
    copy(src, dst, *, follow_symlinks=True)
        Copy data and mode bits ("cp src dst"). Return the file's destination.
        
        The destination may be a directory.
        
        If follow_symlinks is false, symlinks won't be followed. This
        resembles GNU's "cp -P src dst".
        
        If source and destination are the same file, a SameFileError will be
        raised.
    
    copy2(src, dst, *, follow_symlinks=True)
        Copy data and metadata. Return the file's destination.
        
        Metadata is copied with copystat(). Please see the copystat function
        for more information.
        
        The destination may be a directory.
        
        If follow_symlinks is false, symlinks won't be followed. This
        resembles GNU's "cp -P src dst".
    
    copyfile(src, dst, *, follow_symlinks=True)
        Copy data from src to dst in the most efficient way possible.
        
        If follow_symlinks is not set and src is a symbolic link, a new
        symlink will be created instead of copying the file it points to.
    
    copyfileobj(fsrc, fdst, length=0)
        copy data from file-like object fsrc to file-like object fdst
    
    copymode(src, dst, *, follow_symlinks=True)
        Copy mode bits from src to dst.
        
        If follow_symlinks is not set, symlinks aren't followed if and only
        if both `src` and `dst` are symlinks.  If `lchmod` isn't available
        (e.g. Linux) this method does nothing.
    
    copystat(src, dst, *, follow_symlinks=True)
        Copy file metadata
        
        Copy the permission bits, last access time, last modification time, and
        flags from `src` to `dst`. On Linux, copystat() also copies the "extended
        attributes" where possible. The file contents, owner, and group are
        unaffected. `src` and `dst` are path-like objects or path names given as
        strings.
        
        If the optional flag `follow_symlinks` is not set, symlinks aren't
        followed if and only if both `src` and `dst` are symlinks.
    
    copytree(src, dst, symlinks=False, ignore=None, copy_function=<function copy2 at 0x7f608638b640>, ignore_dangling_symlinks=False, dirs_exist_ok=False)
        Recursively copy a directory tree and return the destination directory.
        
        If exception(s) occur, an Error is raised with a list of reasons.
        
    ...(see help(shutil) for more))
"""

# Imports
from shutil import *
from pathlib import Path
from os import *
from sys import *
from typing import *
from datetime import *
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, validator

# Classes
@dataclass(frozen=True)
class UFSObject(ABC):
    """
    UFSObject class - a base class for UFSFile and UFSDir.
    """
    path: str
    path_obj: Path
    path_obj_exists: bool
    path_obj_is_dir: bool
    path_obj_is_file: bool
    path_obj_is_symlink: bool

    @validator('path_obj_exists', always=True)
    def path_obj_exists_validator(cls, v, values, **kwargs):
        return v or values['path_obj'].exists()

    def __str__(self) -> str:
        """
        String representation of the UFSObject class.
        """
        return f"UFSObject(path={self.path}, path_obj={self.path_obj}, path_obj_exists={self.path_obj_exists}, path_obj_is_dir={self.path_obj_is_dir}, path_obj_is_file={self.path_obj_is_file}, path_obj_is_symlink={self.path_obj_is_symlink}"
    
    def __repr__(self) -> str:
        """
        String representation of the UFSObject class.
        """
        return f"UFSObject(path={self.path}, path_obj={self.path_obj}, path_obj_exists={self.path_obj_exists}, path_obj_is_dir={self.path_obj_is_dir}, path_obj_is_file={self.path_obj_is_file}, path_obj_is_symlink={self.path_obj_is_symlink}"

    def __eq__(self, other: object) -> bool:
        """
        Equality operator for the UFSObject class.
        """
        if isinstance(other, UFSObject):
            return self.path == other.path
        return False
    
    def __hash__(self) -> int:
        """
        Hash operator for the UFSObject class.
        """
        return hash(self.path)
    
    def __ne__(self, other: object) -> bool:
        """
        Inequality operator for the UFSObject class.
        """
        if isinstance(other, UFSObject):
            return self.path!= other.path
        return True
    
    def __lt__(self, other: object) -> bool:
        """
        Less than operator for the UFSObject class.
        """
        if isinstance(other, UFSObject):
            return self.path < other.path
        return False
    
    def __le__(self, other: object) -> bool:
        """
        Less than or equal to operator for the UFSObject class.
        """
        if isinstance(other, UFSObject):
            return self.path <= other.path
        return False
    
    def __gt__(self, other: object) -> bool:
        """
        Greater than operator for the UFSObject class.
        """
        if isinstance(other, UFSObject):
            return self.path > other.path
        return False
    
    def __ge__(self, other: object) -> bool:
        """
        Greater than or equal to operator for the UFSObject class.
        """
        if isinstance(other, UFSObject):
            return self.path >= other.path
        return False
    
    def __init__(self, path: str):
        """
        Constructor for the UFSObject class.
        """
        self.path = path
        self.path_obj = Path(path)
        self.path_obj_exists = self.path_obj.exists()
        self.path_obj_is_dir = self.path_obj.is_dir()
        self.path_obj_is_file = self.path_obj.is_file()
        self.path_obj_is_symlink = self.path_obj.is_symlink()
        self.path_obj_is_block_device = self.path_obj.is_block_device()
        self.path_obj_is_char_device = self.path_obj.is_char_device()
        self.path_obj_is_fifo = self.path_obj.is_fifo()
        self.path_obj_is_socket = self.path_obj.is_socket()
        self.path_obj_is_mount = self.path_obj.is_mount()
        self.path_obj_is_reserved = self.path_obj.is_reserved()
        
    
    def __copy__(self) -> object:
        """
        Copy operator for the UFSObject class.
        """
        return UFSObject(self.path)
    


class UFS:
    """
    UFS class - wraps the shutil module's relevant classes and functions and methods for this project.
    """
    def __init__(self, path: str):
        """
        Constructor for the UFS class.
        """
        self.path = path
        self.path_obj = Path(path)
        self.path_obj.mkdir(parents=True, exist_ok=True)
        self.path_obj.chmod(0o777)
        self.path_obj.chown(0, 0)
        self.path_obj.touch()
        self.path_obj.write_text("UFS")
        self.path_obj.chmod(0o777)
        self.path_obj.chown(0, 0)
        self.path_obj.touch()
        self.path_obj.write_text("UFS")
        self.path_obj.chmod(0o777)
        self.path_obj.chown(0, 0)
        self.path_obj.touch()
        self.path_obj.write_text("UFS")
        self.path_obj.chmod(0o777)

    def __str__(self) -> str:
            """
            Returns the path of the UFS object.
            """
            return self.path
    
    def __repr__(self) -> str:
            """
            Returns the path of the UFS object.
            """
            return self.path
    
    def __enter__(self) -> None:
            """
            Returns the path of the UFS object.
            """
            return self.path
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
            """
            Deletes the UFS object.
            """
            self.path_obj.unlink()
            self.path_obj.rmdir()


