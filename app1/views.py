from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChatResponseSerializer
from django.conf import settings
from .models import ChatResponse
from ai71 import AI71
from rest_framework.decorators import api_view


class ExampleView(APIView):
    def get(self, request):
        data = {"message": "Hello, world!"}
        return Response(data, status=status.HTTP_200_OK)
    

#-------------------------------------------------------------------------   
AI71_API_KEY = "api71-api-bbf93539-d8b8-4e01-9fff-ca49ac77e090"
client = AI71(AI71_API_KEY)

@api_view(['POST'])
def get_ai_response(request):
    print(request.data["message"])
    serializer = ChatResponseSerializer(data=request.data)
    if serializer.is_valid():
        user_message = serializer.validated_data['message']
        user_message =request.data['message']
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        messages.append({"role": "user", "content": user_message})
        content = ""
        chat_response = ChatResponse(user_message=user_message, ai_response=content)
        chat_response.save()
        for chunk in client.chat.completions.create(
            messages=messages,
            model="tiiuae/falcon-180B-chat",
            stream=True,
        ):
            delta_content = chunk.choices[0].delta.content
            if delta_content:
                content += delta_content

        messages.append({"role": "assistant", "content": content})

        # # Save to MongoDB
        chat_response = ChatResponse(user_message=user_message, ai_response=content)
        chat_response.save()
        print("saved to dataBase")

        return Response({"response": content}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
