import json
import logging

import boto3

LOGGER = logging.getLogger()


class SqsReader:

    def __init__(self, queue_url):
        self.queue_url = queue_url
        self.processed_messages = 0
        self.sqs = boto3.client('sqs')

    def read_messages(self):
        yield b"Time,SpO2,Pulse\n"
        response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=10)

        while 'Messages' in response:
            for message in response['Messages']:
                self.processed_messages += 1
                LOGGER.debug("processed %s", message)

                yield self.transform_to_csv(json.loads(message['Body'])).encode()

            self.delete_messages(response['Messages'])
            response = self.sqs.receive_message(QueueUrl=self.queue_url, MaxNumberOfMessages=10)

    def transform_to_csv(self, payload):
        if 'time' not in payload:
            LOGGER.error("unreadable payload: %s", payload)
            pass

        sp_o2 = payload['spO2'] if 'spO2' in payload else ''
        pulse = payload['pulse'] if 'pulse' in payload else ''
        return "{},{},{}\n".format(payload['time'], sp_o2, pulse)

    def delete_messages(self, messages):
        request = []
        for message in messages:
            request.append({
                'Id': message['MessageId'],
                'ReceiptHandle': message['ReceiptHandle']
            })

        LOGGER.debug("deleting messages: %s", request)
        self.sqs.delete_message_batch(QueueUrl=self.queue_url, Entries=request)
