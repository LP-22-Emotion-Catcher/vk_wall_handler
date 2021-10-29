import logging

from service.worker import Worker

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    logger.debug('VK wall handler started')
    worker = Worker()
    worker.work()
