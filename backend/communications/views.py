from django.shortcuts import render

class ConversationMessagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, room_name):
        conversation = Conversation.objects.get(id=room_name)
        messages = conversation.messages.all().order_by('timestamp')
        return Response([{
            "sender": m.sender.username,
            "message": m.text,
            "timestamp": m.timestamp
        } for m in messages])




