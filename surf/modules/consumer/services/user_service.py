# -*- coding: utf-8 -*-
"""
Created By      : ZedFeorius
Created Time    : 2024/4/13 19:39
File Name       : user_service
Project Name    : surf-extreme
Last Edit Time  : 
"""
import traceback

from surf.modules.util import Session
from surf.modules.consumer.models import UserModel


class UserService(object):
    def __init__(self):
        self.__userModel = UserModel()
        pass

    def login(self, session_id):
        try:
            session = Session.get_session_by_id(session_id)
            if session:
                public_key = session.get('client_public_key')
                res = self.__userModel.get_userid_by_public_key(public_key)
                if len(res) > 0:
                    print(1)
                    user_id = res[0]['id']
                else:
                    print(2)
                    filters = {
                        "c_public_key": public_key
                    }
                    user_id = self.__userModel.save_user(filters)
                print(user_id)
                if user_id is not False:
                    session.set('user_id', user_id)
                    respond_json = {
                        'command': 'to_url',
                        'url': 'main'
                    }
                    return respond_json
                else:
                    return False
        except Exception as e:
            print(f"""{e}\n{traceback.format_exc()}""")
            return False

    def get_user_data(self, session_id):
        try:
            session = Session.get_session_by_id(session_id)
            user_id = session.get("user_id")
            if session:
                res = self.__userModel.get_userdata_by_userid(user_id)
                if len(res) > 0:
                    user_dict = {
                        "user_nickname": res[0]["nickname"],
                        "user_info": res[0]["info"]
                    }
                    respond_json = {
                        'command': "user_data",
                        'message': [
                            {
                                "user": user_dict,
                                "servers": []
                            }
                        ]
                    }
                    return respond_json
                else:
                    return False
        except Exception as e:
            print(f"""{e}\n{traceback.format_exc()}""")
            return False
