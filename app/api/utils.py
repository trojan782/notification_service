import boto3

# from crud import get_all_users
sns = boto3.client('sns')

topic_arn = 'arn:aws:sns:eu-west-1:935097633081:all'

def get_subcription_by_topic(topic_arn):
    response = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
    endpoints = [subscription['Endpoint'] for subscription in response['Subscriptions']]
    return endpoints


# def extract_user_emails():
#     return get_all_users()

# # docker run --rm -v ~/.aws:/root/.aws consumer

# extract_user_emails()
