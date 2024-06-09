import os
import logging
import boto3
import signal

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

sqs = boto3.resource('sqs')
sns_client = boto3.client('sns')
sqs_client = boto3.client("sqs")
queue = sqs.get_queue_by_name(QueueName='app_queue')

# contants
QUEUE_URL = queue.url
TOPIC=sns_client.list_topics()
ARN=TOPIC['Topics'][0]['TopicArn']


if __name__ == '__main__':
    try:
        while True:
            msgs = queue.receive_messages(
                MaxNumberOfMessages=5,
                WaitTimeSeconds=20
            )

            if not msgs:
                logging.warning("No messages to process 💤...")
            else:
                for msg in msgs:
                    logging.info(f"Recieved message {msg.message_id} ⚡️")
                    sns_client.publish(TopicArn=ARN, Message=msg.body)
                    sqs_client.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=msg.receipt_handle)
                    logging.info(f"Notification sent out 🚀")
                    logging.info("message deleted from queue 🗑️")
    except KeyboardInterrupt:
        logging.info("exiting gracefully...")
        os.kill(os.getpid(), signal.SIGTERM)
    except Exception as e:
        logging.error(e)
        raise e