"""CS -> Talants"""
import random
import os
import json
import dotenv
import vk_api
from vkbottle import Keyboard, KeyboardButtonColor, Text, OpenLink

class VK :
    def __init__(self, token: str):
        self.vk = vk_api.VkApi(token=token)

    def send_message(self, id: int, message: str) -> None :
        self.vk.method('messages.send', {
                'user_id': id,
                'message': message,
                'random_id': random.randint(1, 1000000000000)
                })

    def send_keyboard(self, id: int, message: str, keyboard) -> None :
        self.vk.method('messages.send', {
                'user_id': id,
                'message': message,
                'keyboard': keyboard,
                'random_id': random.randint(1, 1000000000000)
                })
        