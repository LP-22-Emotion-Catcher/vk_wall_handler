import logging

from service.worker import Worker

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    worker = Worker()
    worker.work()
