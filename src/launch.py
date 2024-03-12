import logging

if 'ml' not in logging.Logger.manager.loggerDict:
    logging.basicConfig(level=logging.INFO)
ml = logging.getLogger('ml')

def main() -> None:
    ml.info('Hello World!')