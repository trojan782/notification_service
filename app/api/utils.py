import os
import boto3

# Helper functions were are supposed to be here...

sns = boto3.client('sns')

topic_arn = os.getenv('TOPIC_ARN')

def get_subcription_by_topic(topic_arn):
    response = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
    endpoints = [subscription['Endpoint'] for subscription in response['Subscriptions']]
    return endpoints

