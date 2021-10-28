import logging

from service.worker import Worker

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logger.info('Started')
    worker = Worker()
    worker.work()
