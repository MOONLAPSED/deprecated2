#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations
#------------------------------------------------------------------------------
# Standard Library Imports - 3.13 std libs **ONLY**
#------------------------------------------------------------------------------
import re
import os
import io
import dis
import sys
import ast
import time
import site
import mmap
import json
import uuid
import shlex
import socket
import struct
import shutil
import pickle
import ctypes
import logging
import tomllib
import pathlib
import asyncio
import inspect
import hashlib
import tempfile
import platform
import traceback
import functools
import linecache
import importlib
import threading
import subprocess
import tracemalloc
import http.server
import collections
from array import array
from pathlib import Path
from enum import Enum, auto
from collections.abc import Iterable, Mapping
from datetime import datetime
from queue import Queue, Empty
from abc import ABC, abstractmethod
from functools import reduce, lru_cache, partial, wraps
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager, asynccontextmanager
from importlib.util import spec_from_file_location, module_from_spec
from types import SimpleNamespace, ModuleType,  MethodType, FunctionType, CodeType, TracebackType, FrameType
from typing import (
    Any, Dict, List, Optional, Union, Callable, TypeVar, Tuple, Generic, Set,
    Coroutine, Type, NamedTuple, ClassVar, Protocol, runtime_checkable, AsyncIterator
)
import cProfile
import pstats
from threading import Thread
import argparse
from io import StringIO
import signal
import errno
import signal
try:
    from . import __all__
    if not __all__:
        __all__ = []
    else:
        __all__ += __file__
except ImportError:
    __all__ = []
    __all__ += __file__
IS_WINDOWS = os.name == 'nt'
IS_POSIX = os.name == 'posix'
profiler = cProfile.Profile()
profiler.enable
class SystemProfiler:
    """Handles system profiling and performance measurements"""
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls) -> 'SystemProfiler':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._initialize()
            return cls._instance
    
    def _initialize(self) -> None:
        self.profiler = cProfile.Profile()
        self.start_time = time.monotonic()
        
    def start(self) -> None:
        self.profiler.enable()
        
    def stop(self) -> str:
        self.profiler.disable()
        s = StringIO()
        ps = pstats.Stats(self.profiler, stream=s).sort_stats('cumulative')
        ps.print_stats()
        return s.getvalue()

class ProcessExecutor:
    """Platform-independent process execution"""
    @staticmethod
    def _windows_run_command(command, timeout, env):
        from ctypes import windll, wintypes
        
        # Optimize process priority - using Windows ABOVE_NORMAL_PRIORITY_CLASS
        def set_process_priority():
            windll.kernel32.SetPriorityClass(
                wintypes.HANDLE(-1), 
                0x00008000  # ABOVE_NORMAL_PRIORITY_CLASS
            )

        def wrun_command(command, timeout=None, env=None):
            # Increase buffer sizes for better performance
            BUFFER_SIZE = 65536  # 64KB buffer
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
                shell=True,
                env=env,
                bufsize=BUFFER_SIZE  # Set larger buffer
            )
            
            # Set higher priority for the subprocess
            set_process_priority()
            
            # Use memoryview for zero-copy buffering
            def read_stream(stream):
                buffer = []
                while True:
                    chunk = stream.read1(BUFFER_SIZE)
                    if not chunk:
                        break
                    buffer.append(chunk)
                return b''.join(buffer).decode()
                
            stdout = read_stream(process.stdout)
            stderr = read_stream(process.stderr)
            
            return_code = process.wait(timeout=timeout)
            return stdout, stderr, return_code

        try:
            stdout, stderr, status = wrun_command(command, timeout=timeout, env=env)
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            print("STATUS:", status, '\n', '_' * 80)
            return stdout, stderr, status
        except TimeoutError as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise
    @staticmethod
    def _posix_run_command(command, timeout, env):
        import resource
        
        # Set process priority using nice value (-20 to 19, lower is higher priority)
        def set_process_priority():
            try:
                os.nice(-10)  # Higher priority but not maximum
            except PermissionError:
                pass
                
        def run_command(command, timeout=None, env=None):
            BUFFER_SIZE = 65536  # 64KB buffer
            
            # Set resource limits for better performance
            resource.setrlimit(resource.RLIMIT_NOFILE, (4096, 4096))
            
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,
                shell=True,
                env=env,
                bufsize=BUFFER_SIZE,
                preexec_fn=set_process_priority
            )
            
            # Use memoryview for efficient reading
            stdout, stderr = process.communicate(timeout=timeout)
            return stdout.decode(), stderr.decode(), process.returncode
        try:
            stdout, stderr, status = run_command(command, timeout=timeout, env=env)
            print("STDOUT:", stdout)
            print("STDERR:", stderr)
            print("STATUS:", status, '\n', '_' * 80)
            return stdout, stderr, status  # Add return statement
        except TimeoutError as e:
            print(e)
            raise
        except Exception as e:
            print(e)
            raise
    @staticmethod
    def run_command(command: List[str], timeout: Optional[float] = None, 
                   env: Optional[Dict[str, str]] = None) -> Tuple[str, str, int]:
        """Platform-independent command execution"""
        if IS_WINDOWS:
            return ProcessExecutor._windows_run_command(command, timeout, env)
        return ProcessExecutor._posix_run_command(command, timeout, env)
class Benchmark:
    """Command benchmarking utility"""
    def __init__(self, command: List[str], iterations: int = 10):
        self.command = command
        self.iterations = iterations
        self.results: List[float] = []
        self.profiler = SystemProfiler()
    def run(self) -> float:
        self.profiler.start()
        best = sys.maxsize
        for _ in range(self.iterations):
            t0 = time.monotonic()
            ProcessExecutor.run_command(self.command)
            t1 = time.monotonic()
            duration = t1 - t0
            self.results.append(duration)
            best = min(best, duration)
            print(f'{duration:.3f}s')
        profile_data = self.profiler.stop()
        print('_' * 80)
        print(f'Best of {self.iterations}: {best:.3f}s')
        print('Profile data:')
        print(profile_data)
        return best

def main() -> int:
    parser = argparse.ArgumentParser(description='Benchmark command execution')
    parser.add_argument('-n', '--num', type=int, default=10,
                       help="Number of iterations")
    parser.add_argument('cmd', nargs=argparse.REMAINDER, help="Command to execute")
    args = parser.parse_args()
    if not args.cmd:
        parser.error("Command is required")
    # Remove the '--' separator if it exists
    if args.cmd[0] == '--':
        command = args.cmd[1:]
    else:
        command = args.cmd
    benchmark = Benchmark(command, args.num)
    benchmark.run()
    return 0

if __name__ == "__main__":
# python handle.py -- python -c "print('hello')"
    sys.exit(main())