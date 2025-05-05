"""CS -> Talants"""
import random
import os
import json
from dotenv import load_dotenv
import vk_api
from vkbottle import Keyboard, KeyboardButtonColor, Text

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
PASSWORD = str(os.getenv('PASSWORD'))

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

class Command :
    def __init__(self, token: str):
        self.vk = VK(token)
        
    def add_admin(self, id: int) -> None :
        with open('temp_data.json', 'r') as file :
            data = json.load(file)
        data['admin'].append(id)
        with open('temp_data.json', 'w') as file :
            json.dump(data, file, indent=4)