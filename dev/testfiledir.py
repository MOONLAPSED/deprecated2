import os
import src.lager

root_logger, sub_logger = src.lager.init_logging()
if __name__ != "__main__":
    def main2():
        print("Hello from testfiledir.py in /dev/testfiledir.py")
        print("The current working directory is: " + os.getcwd())
        root_logger.info("Log message from testfiledir.py")
        sub_logger.info("Another log message from testfiledir.py")