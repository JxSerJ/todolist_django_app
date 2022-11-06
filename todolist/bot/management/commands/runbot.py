from django.conf import settings
from django.core.management import BaseCommand

from bot.models import TgUser
from bot.tg.client import TgClient
from goals.models import Goal
from todolist.settings import TG_BOT_TOKEN


class Command(BaseCommand):
    help = 'Run TG bot'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # mandatory
        self.tg_client = TgClient(TG_BOT_TOKEN)

    def handle(self, *args, **kwargs):
        offset = 0

        while True:
            response = self.tg_client.get_updates(offset=offset)
            for item in response.result:
                offset = item.update_id + 1
                self.handle_message(item.message)

    def handle_message(self, message):
        tg_user, created = TgUser.objects.get_or_create(
            tg_user_id=message.from_.id,
            defaults={"tg_chat_id": message.chat.id,
                      'username': message.from_.username}
        )
        if created:
            self.tg_client.send_message(chat_id=message.chat.id, text="Greetings!")

        if tg_user.user:
            self.handle_verified_user(message, tg_user)
        else:
            self.handle_unverified_user(message, tg_user)

    def handle_verified_user(self, message, tg_user):
        if not message.text:
            self.tg_client.send_message(chat_id=message.chat.id, text="Doesn't look like anything to me")

        if '/goals' in message.text:
            self.show_goals(message, tg_user)
        elif '/create' in message.text:
            self.create_goal(message, tg_user)
        else:
            self.tg_client.send_message(chat_id=message.chat.id, text='Unknown command')

    def handle_unverified_user(self, message, tg_user):
        tg_user.generate_verification_code()
        tg_user.save(update_fields=['verification_code'])

        self.tg_client.send_message(
            chat_id=message.chat.id,
            text=f"You're not verified.\n"
                 f'Your verification code:   {tg_user.verification_code}\n'
                 f'Enter this code into corresponding field on the http://sprotsenko.ga/'
        )

    def show_goals(self, message, tg_user):
        goals = Goal.objects.filter(user=tg_user.user)
        if goals.count() == 0:
            self.tg_client.send_message(chat_id=message.chat.id, text='You have no goals here')
        else:
            title_str = 'Your goals:\n'
            response = '\n'.join([f'#{goal.id} {goal.title}' for goal in goals])
            self.tg_client.send_message(chat_id=message.chat.id, text=title_str + str(response))

    def create_goal(self, message, tg_user):
        pass  # todo
