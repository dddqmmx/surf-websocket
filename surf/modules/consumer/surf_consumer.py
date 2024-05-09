# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius(fuzequan)
Created Time    : 2024/5/8 15:14
File Name       : surf_consumer.py
Last Edit Time  : 
"""
import json
from typing import Callable, Dict

from surf.appsGlobal import logger, errorResult
from surf.modules.util import BaseConsumer, UserPool, session_check
from surf.modules.consumer.services import ChatService, ServerService, UserService

from cryptography.hazmat.primitives import serialization
from surf.modules.encryption.encryption_ras import generate_key_pair


class SurfConsumer(BaseConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.userPool = UserPool()
        self.service_dict = {
            "chat": ChatService(),
            "server": ServerService(),
            "user": UserService()
        }
        self.func_dict: Dict[str, Dict[str, Callable[[str], any]]] = {
            "key": {
                "key_exchange": self.key_exchange
            },
            "chat": {
                "get_message": self.get_message,
                "send_message": self.send_message
            },
            "user": {
                'login': self.login,
                'get_user_data': self.get_user_data,
                'search_user': self.search_user,
                'get_friends': self.get_friends
            },
            "server": {
                "create_server": self.create_server,
                "create_channel_group": self.create_channel_group,
                "create_channel": self.create_channel,
                "get_server_details": self.get_server_details,
                "add_server_member": self.add_server_member
            },
            'test': {
                'test1': self.test
            }
        }

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    @session_check
    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        command = text_data['command']
        # path = self.scope['url_route']['kwargs']['path']
        path = text_data['path']
        if path in self.func_dict.keys() and command in self.func_dict[path].keys():
            await self.func_dict[path].get(command)(text_data)

    async def key_exchange(self, text_data):
        private_key, public_key = generate_key_pair()  # 将private_key保存为self.private_key
        serialized_public_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        init_json = {
            'command': 'key_exchange',
            'public_key': serialized_public_key.decode('utf-8'),
        }
        await self.send(text_data=json.dumps(init_json))

    """-------------------------------user----------------------------"""

    async def login(self, text_data):
        respond_json, session = self.service_dict['user'].login(text_data['public_key'])
        if session:
            if not self.userPool.access_new_user(session, self):
                logger.error('user login failed, see more at connections.log')
                await self.send(errorResult('login', '登录失败', 'user'))
        await self.send(respond_json)

    async def get_user_data(self, text_data):
        respond_json = self.service_dict['user'].get_user_data(text_data)
        await self.send(respond_json)

    async def search_user(self, text_data):
        respond_json = self.service_dict['user'].search_user(text_data)
        await self.send(respond_json)

    async def get_friends(self, text_data):
        respond_json = self.service_dict['user'].get_friends(text_data)
        await self.send(respond_json)

    """-------------------------------server----------------------------"""

    async def create_server(self, text_data):
        respond_json = self.service_dict['server'].create_server(text_data)
        await self.send(respond_json)

    async def create_channel_group(self, text_data):
        respond_json = self.service_dict['server'].create_channel_group(text_data)
        await self.send(respond_json)

    async def create_channel(self, text_data):
        respond_json = self.service_dict['server'].create_channel(text_data)
        await self.send(respond_json)

    async def get_server_details(self, text_data):
        respond_json = self.service_dict['server'].get_server_details(text_data)
        await self.send(respond_json)

    async def add_server_member(self, text_data):
        respond_json = self.service_dict['server'].add_server_member(text_data)
        await self.send(respond_json)

    """-------------------------------chat----------------------------"""

    async def get_message(self, text_data):
        respond_json = self.service_dict['chat'].get_message(text_data)
        await self.send(respond_json)

    async def send_message(self, text_data):
        respond_json = self.service_dict['chat'].send_message(text_data)
        if respond_json['message'] is not False:
            self.userPool.broadcast_to_all_user_in_channel(text_data)
        else:
            await self.send(respond_json)

    async def test(self, text_data):
        await self.send('114514')