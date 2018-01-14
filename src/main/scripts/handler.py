import logging
import os
from datetime import datetime

import boto3

from cosmoanalytics.iterator_stream import IteratorStream
from cosmoanalytics.sqs_reader import SqsReader

LOGGER = logging.getLogger()


def upload_progress_handler(number_of_bytes):
    LOGGER.info("uploaded bytes: %s", number_of_bytes)


def handle(event, context):
    if event and 'test' in event and event['test']:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    queue = os.environ['QUEUE']
    bucket = os.environ['CSV_DATA_BUCKET']
    LOGGER.info("queue: %s", queue)
    LOGGER.info("bucket: %s", bucket)

    reader = SqsReader(queue)
    stream = IteratorStream(reader.read_messages())

    file_name = "{}.csv".format(datetime.utcnow().strftime("%Y%m%d%H%M"))
    boto3.client('s3').upload_fileobj(stream, bucket, file_name, Callback=upload_progress_handler)

    return {
        "processed_messages": reader.processed_messages,
        "queue": queue,
        "bucket": bucket,
        "filename": file_name,
        "event": event
    }


if __name__ == '__main__':
    print(handle({'test': False}, None))