from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.tg.client import TgClient
from todolist.settings import TG_BOT_TOKEN


class VerificationView(GenericAPIView):
    model = TgUser
    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = TgUser.objects.filter(verification_code=request.data.get('verification_code')).first()

        instance.user = self.request.user
        instance.save(update_fields='user')

        tg_client = TgClient(token=TG_BOT_TOKEN)
        tg_client.send_message(chat_id=instance.tg_chat_id, text='Verification completed successfully')
