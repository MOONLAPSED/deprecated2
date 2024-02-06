#! /usr/bin/env python3
# main.py
import os
import sys

try:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # is there adequate permission to expand the path?
except Exception as e:
    print(e)
finally:
    sys.path.extend([
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')),
        os.path.join(os.path.dirname(os.path.realpath(__file__)), '.'),
        os.path.abspath(os.path.dirname(__file__))
    ])


if __name__ == "__main__":
    try:
        import src.lager
        import xml.etree.ElementTree as ET
    except ImportError:
        print("Elementree not found.")
    finally:
        src.lager.main()
        src.lager.sub()
    