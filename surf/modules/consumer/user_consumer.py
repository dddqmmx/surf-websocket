import orjson as json

from surf.modules.consumer.services import UserService
from surf.modules.util import BaseConsumer


class UserConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.public_key = None
        self.user_service = UserService()
        self.func_dict = {
            'login': self.login,
            'get_user_data': self.get_user_data,
            'search_user': self.search_user,
            'get_friends': self.get_friends
        }

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        command = text_data['command']
        if command in self.func_dict.keys():
            await self.func_dict.get(command)(text_data)

    async def login(self, text_data):
        respond_json = self.user_service.login(text_data['session_id'])
        await self.send(respond_json)

    async def get_user_data(self, text_data):
        respond_json = self.user_service.get_user_data(text_data)
        await self.send(respond_json)

    async def search_user(self, text_data):
        respond_json = self.user_service.search_user(text_data)
        await self.send(respond_json)

    async def get_friends(self, text_data):
        respond_json = self.user_service.get_friends(text_data)
        await self.send(respond_json)
