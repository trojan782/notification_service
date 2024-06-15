import re
import os
import boto3
from dotenv import load_dotenv
from models import User, Notification
from fastapi import HTTPException
from utils import get_subcription_by_topic
from posthog import Posthog
import uuid

# load environment variables
load_dotenv()

TOPIC_ARN = os.getenv('TOPIC_ARN')
queue_name = os.getenv('QUEUE_NAME')
posthog_api_key = os.getenv('POSTHOG_APIKEY')
posthog_host = os.getenv('POSTHOG_HOST')

# posthog initalization
posthog = Posthog(project_api_key=posthog_api_key, host=posthog_host)

sqs = boto3.client('sqs')
sns = boto3.client('sns')
queue = sqs.get_queue_url(QueueName=queue_name)
dynamodb = boto3.resource('dynamodb')


user_table = dynamodb.Table('user_table')
notification_table = dynamodb.Table('notification_table')

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

"""
Creating a new user which will be stored in the users table.
POST - /user

{
    "name" : "John Doe"
    "email": "johndoe@email.com"
}
"""
def create_user(user: User):
    try:
        user_id = str(uuid.uuid4())
        user_data = user.dict()
        if not re.fullmatch(regex, user_data['email']):
            raise HTTPException(status_code=400, detail="Please enter a valid email address.")
        existing_users = get_all_users()
        emails = [user['email'] for user in existing_users['users']]
        if user_data['email'] in emails:
            return {"message": "user already exists"}
        else:
            user_table.put_item(Item=user_data)
            posthog.capture(user_id, "tried to create a user")
        return {"message": "User created successfully", "user": user_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
"""
To get all events(sns topics) a users/endpoint is subcribed to using the email.
GET - /user/events/{email}
"""
def get_user_events(email: str):
    try:
        response = user_table.get_item(Key={'email': email})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="User not found")
        return {"users_events": response['Item']['events']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# get a list of all users from the db
def get_all_users():
    user_id = str(uuid.uuid4())
    try:
        response = user_table.scan()
        posthog.capture(user_id, "tried to list all users")
        return {"users": response['Items']}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

'''
Creating a new notification/event to be sent out to subcribed users/endpoints.
POST - /notify
{
  "message": "creating a new notification! ⚡️"
}
'''
def create_notification(notification: Notification):
    try:
        notification_data = notification.dict()
        notification_table.put_item(Item=notification_data)
        sqs.send_message(QueueUrl=queue['QueueUrl'], MessageBody=notification_data['message'])
        return {"message": "Notification created successfully", "notification": notification_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
"""
Function to subcribe an endpoint(email/phone) to an event but I have implemented subcription just for emails.
Here I am just using a default event. although I am supposed to be able to subcribe to different events.
e.g /subcribe/{endpoint}
"""
def subcribe_to_event(endpoint: str):
    try:
        if not re.fullmatch(regex, endpoint):
            raise HTTPException(status_code=400, detail="Please enter a valid email address.")
        if endpoint in get_subcription_by_topic(TOPIC_ARN):
            raise HTTPException(status_code=400, detail="endpoint already subscribed to this event.")
        else:
            sns.subscribe(TopicArn=TOPIC_ARN, Protocol='email', Endpoint=endpoint)
            return {"message": "endpoint subscribed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
        