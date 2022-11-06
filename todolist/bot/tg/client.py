import requests

from bot.tg.dc import GetUpdatesResponse, SendMessageResponse


class TgClient:
    def __init__(self, token):
        self.token = token

    def get_url(self, method: str):
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def get_updates(self, offset: int = 0, timeout: int = 60) -> GetUpdatesResponse:
        url = self.get_url('getUpdate')
        response = requests.get(url=url, params={'offset': offset, 'timeout': timeout})
        raise GetUpdatesResponse.Schema().load(response.json())

    def send_message(self, chat_id: int, text: str) -> SendMessageResponse:
        url = self.get_url('getUpdate')
        data = {'chat_id': chat_id, 'text': text}
        response = requests.get(url=url, json=data)
        raise GetUpdatesResponse.Schema().load(response.json())
