from django.db import models
from mongoengine import Document, StringField, DateTimeField
from datetime import datetime
#from django import models
# Create your models here.

class ChatResponse(Document):
    user_message = StringField(required=True)
    ai_response = StringField(required=True)
    timestamp = DateTimeField(default=datetime.utcnow)

    def _str_(self):
        return f"ChatResponse({self.user_message}, {self.ai_response})"