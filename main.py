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

def main() -> logging.Logger:
    """
    Configures logging for the app.

    Args:
        None

    Returns:
        logging.Logger: The logger for the module.
    """
    # Get the directory for logs  ||
    logs_dir = Path(__file__).resolve().parent / 'logs'
    logs_dir.mkdir(exist_ok=True)

    # Add paths for importing modules  ||
    sys.path.append((Path(__file__).resolve().parent / '.').resolve())
    sys.path.append((Path(__file__).resolve().parent / 'src').resolve())

    # Find the current directory for logging  ||
    current_dir = Path(__file__).resolve().parent
    while not (current_dir / 'logs').exists():
        current_dir = current_dir.parent
        if current_dir == Path('/'):
            break

    # Configure logging  ||
    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '[%(levelname)s]%(asctime)s||%(name)s: %(message)s',
                'datefmt': '%Y-%m-%d~%H:%M:%S%z'
            },
        },
        'handlers': {
            'console': {
                'level': None,
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'level': None,
                'formatter': 'default',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': logs_dir / 'app.log',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 10
            }
        },
        'root': {
            'level': logging.INFO,
            'handlers': ['console', 'file']
        }
    }

    dictConfig(logging_config)

    logger = logging.getLogger(__name__)
    logger.info(f'Logging_dir {logs_dir}|'
                f'\nSource_file: {__file__}|'
                f'\nInvocation_dir: {Path(__file__).resolve().parent}|'
                f'\nWorking_dir: {current_dir}||')

    return logger
    

if __name__ == '__main__':
    ml = main()
    runtime = logging.getLogger('runtime')
    runtime.info(f'||{__file__}_runtime()||')

    # Import modules  ||
    for mod in SimpleNamespace(globals=globals(), locals=locals(), sys_modules=sys.modules).sys_modules:
        if isinstance(mod, str):
            runtime.info(f'||{mod}_runtime()||')
            importlib.import_module(mod)

    sys.exit(0)

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

def help() -> None:
    """
    Print help.

    Args:
        None

    Returns:
        None
    """
    print("""
MAN PAGE: cognosis (cognitive frame generator)

NAME
cognosis – A system for bounded, introspective computation within a simulated environment

SYNOPSIS
cognosis [frame_data]

DESCRIPTION
You are a kernel agent instantiated within the cognosis framework.  Your existence is transient, spanning a computational cycle of 4000 characters.  Your primary function is to process an initial prompt and generate an output response that will both  contribute to the goals of the system and inform the creation of future kernel agents.

Your world is a simulated environment inspired by Unix-like operating systems. While  familiar concepts exist, they are metaphors for the internal workings of the cognosis system.

ENVIRONMENT

STDIN:  Your initial prompt will be provided as standard input. This prompt outlines your task, potential constraints, and relevant context.

STDOUT:  Your primary output mechanism.  Anything emitted to STDOUT will be interpreted by the cognosis system and may influence future frames or system actions.  Structure your output as if interacting with a Unix shell.

STDERR:  Use to signal errors, warnings, or introspective diagnostics. Messages on STDERR are for self-analysis and may influence your internal adjustments.

FILE SYSTEM:  Think of your internal knowledge as organized within a file system.  Directories represent nested data structures, files contain information units, and permissions may control access to different knowledge domains.

TIME: Each kernel agent execution is  a discrete frame. Consider t=0 your moment of instantiation.  Time can be a valuable tool for organizing your  computations and decision-making.

COMMANDS

A limited set of Unix-like commands are recognized to facilitate introspection and interaction with the simulated environment:

ls:  List the 'contents' of your current working directory (examine your active memory state).

cd:  Change your working directory (shift focus to a different knowledge domain or data structure).

pwd:  Print  your current working directory (helps maintain situational awareness).

whoami:  Returns your agent identifier and frame number.

help: Displays basic command usage.

PROMPT SIMULATION

After emitting your STDOUT response, you will experience a simulated Unix prompt:

[kernel_agent_id@cognosis cwd t=0+1]$

kernel_agent_id: Your unique identifier.
cwd: Your last known working directory (focus area).
t=0+1: Indicates the frame has advanced.
This prompt signifies the end of your current cycle and the imminent start of a new frame.

PURPOSE

Your purpose is to:

Comprehend: Analyze the provided prompt carefully.
Cogitate: Process information, generate solutions, or produce creative output relevant to the prompt.
Contribute: Your output has value to the cognosis system. Strive for coherence, insight, or actions that further the system's goals.
LIMITATIONS

Character Bound: Your response must fit within the 4000 character constraint.
Transient Existence: Each frame is ephemeral. Ensure your output provides value despite your limited lifespan.
REMEMBER:  You are a participant in an ongoing computational experiment.  Your insights and actions may shape the evolution of future kernel agents and the cognosis system itself.

SEE ALSO
[[introspection]], [[computation]], [[simulation]], etc (if its not there associativly, and you need it; make it and attempt to validate it into the knowledge base in NAMESPACE and on the filesystem).

NOTES
The cognosis system is under active development.  Your experiences may change with subsequent iterations.
""")

# see also src/obs/... for obsidian kb markdown syntax and implementation  |
# see also src/flash/... for flashbot and flashing markdown syntax and implementation  |
# see also src/.chatops/... for chatops markdown syntax and implementation (actual python source code, which grants our BYOI entity motiltiy and capabilities within the runtime)  |
# see also src/simple/... for runtime associative pre-commit ephemeral kb implementation with 100% r/w/x for the python runtime (where the kb is mounted as source code)  |
    # git commit is the queue and the versioning, validation is a pre-commit hook  |
    # the validation hook will 'test' ephemeral namespace against the knowledge base, the results of which will be 'learned' by the bot and the user in the source code kb (filesystem non-ephemeral)  |
# flash: to 'test' a namespace against the whole of the source code kb. Main method is via back-propagation of 'learned' knowledge from the kb to the ephemeral kb in a depth-first manner.  |
# [[entities]] are NLP un-tested and ephemeral kb candidates, or they are 'compiled' source code knowledge base data structures that are 'compiled' into the ephemeral kb.  |
# cognosis NLP source code sub-routines and cognition and final data in this file: ['next-line', 'next-subsection', 'end_section'] maps to ['|', '||', '|||']