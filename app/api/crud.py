import boto3
import re
from models import User, Notification
from fastapi import HTTPException
from utils import get_subcription_by_topic

TOPIC_ARN = 'arn:aws:sns:eu-west-1:935097633081:all'

sqs = boto3.client('sqs')
sns = boto3.client('sns')
queue = sqs.get_queue_url(QueueName='app_queue')

dynamodb = boto3.resource('dynamodb')

user_table = dynamodb.Table('user_table')
notification_table = dynamodb.Table('notification_usertable')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


def create_user(user: User):
    try:
        user_data = user.dict()
        if not re.fullmatch(regex, user_data['email']):
            raise HTTPException(status_code=400, detail="Please enter a valid email address.")
        existing_users = get_all_users()
        emails = [user['email'] for user in existing_users['users']]
        if user_data['email'] in emails:
            return {"message": "user already exists"}
        else:
            user_table.put_item(Item=user_data)
        return {"message": "User created successfully", "user": user_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_user_events(email: str):
    try:
        response = user_table.get_item(Key={'email': email})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="User not found")
        return {"users_events": response['Item']['events']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_all_users():
    try:
        response = user_table.scan()
        return {"users": response['Items']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def create_notification(notification: Notification):
    try:
        notification_data = notification.dict()
        # notification_table.put_item(Item=notification_data)
        sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=notification_data['message'])
        return {"message": "Notification created successfully", "notification": notification_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

def create_event():
    pass

def subcribe_to_event(endpoint: str):
    try:
        if not re.fullmatch(regex, endpoint):
            raise HTTPException(status_code=400, detail="Please enter a valid email address.")
        # if endpoint not in get_all_users():
        #     return {"error": "user is not signed up"}
        if endpoint in get_subcription_by_topic(TOPIC_ARN):
            raise HTTPException(status_code=400, detail="endpoint already subscribed to this event.")
        else:
            sns.subscribe(TopicArn=TOPIC_ARN, Protocol='email', Endpoint=endpoint)
            return {"message": "endpoint subscribed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        