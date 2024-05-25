import datetime
import sys
import logging
from pathlib import Path
from logging.config import dictConfig
import importlib
import types
from abc import abstractmethod, ABC
from types import SimpleNamespace
""" cognosis commenting sub-routines for NLP cognition and re-cognition of the source code of the module and submodules and their SimpleNamespaces and any filesystem objects they create or link to  |
'|' == next line  |
'||' == next_subsection -- source code will appear before the next subsection  |
'|||' == end_section  -- proceed to source code as-normally, ignoring all comments and triple-pipes  |
'normal' comments have no pipes whatsoever (or they are escaped, if they are) |
'|||...<content>...' presumed section, keep reading until a '||' or '|||' is found for the next subsection  |
'||...<content>...' presumed source code, handle it as-normally, until a '|', '||' or '|||' is found for the next subsection  |
'|...' this is a sub-routine NLP cognition 'line'  |
'...' this is a sub-routine NLP cognition 'section', or it is source code. Keep reading until a '|','||' or '|||' is found for the next subsection, or the end of the file  |"""
# notate within 'triple-pipes' mandatory NLP 'cognitive notes' which accompany module and submodule source code and SimpleNamespaces  |
# the final 'triple-pipes' indicates to any-reader of the source code that NLP has concluded and normal python code can resume 'ignoring' the mandatory NLP and [[triple-pipes]] sub-routines  |
# associativity is achieved via cultivation of NAMESPACE, a symlink farm, runtime methods ([[BYOI]] and [[triple-pipes]] sub-routines), and continuous reading (of the source code, and of the sub-routines within the sub-routines architecture)  |
# [[double-bracket]]ed entities are NLP namespaces, which, if unavailable-for import, will be created in the runtime (and validated as source code at conclusion of runtime and the git commits itself).  |
# all runtime resources must be accessed via 'with' statements and all functions must try/exccept; finally, ensuring all runtime resources must be 'closed' at the end of the runtime. __enter__() and __exit__() must be defined for context managers. For example, global ENV variables should be defined as 'with' statements.  ||
class BYOI(ABC):
    """BYOI - bring your own intelligence.

    Abstraction of the source code of the module and submodules and their
    SimpleNamespaces and any filesystem objects they create or link to:
    must be 'presentable' to EXTERNAL NLP and generative intelligence; via a
    virtual shell (see src/shell/shell.py for details).
    """

    @abstractmethod
    def __init__(self) -> None:
        # Define the modality of the BYOI, is it an API, a local process,  |
        # a cloud-provider, etc?  ||
        pass

    @abstractmethod
    def __call__(self) -> None:
        # Init the BYOI shell_session (see src/shell/shell.py for details).  ||
        pass

    @abstractmethod
    def _post(self, msg: str) -> None:
        # Post a message to the BYOI shell_session queue handler.  ||
        pass

    def _chat(self, msg: str) -> None:
        # Post a message directly to chat interface.  ||
        pass

    def _debug(self) -> None:
        # Debug the BYOI shell_session queue handler (and __call__() status)  |
        # or a chat message to the BYOI chat session.  ||
        pass

# Global dictionary to track associations  ||
associative_links = {}

def import_module(mod: str) -> str:
    """Imports a module and tracks associations."""
    try:
        importlib.import_module(str(mod))
        if isinstance(sys.modules[mod], types.ModuleType):
            associative_links[mod] = {
                # You can add any metadata here:
                'type': 'ModuleType',
                'import_time': datetime.datetime.now()
            }
            return 'IMPORTED'
        else:
            return 'UNKNOWN_TYPE'
    except ModuleNotFoundError:
        return 'NOT_FOUND'

def Is_Associatve(mod: str) -> bool:
    """ Returns True if the module is associated with the associative_links dictionary and check Is_Named() """
    return mod in associative_links and Is_Named(mod)

def Is_Named(mod: str) -> bool:
    """Returns True if the module is associated with the associative_links dictionary and has a name."""
    if mod in associative_links:
        name = associative_links[mod].get('name')
        return name is not None
    else:
        return False
