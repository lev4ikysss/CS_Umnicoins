"""CS -> Talants"""
import random
import os
import json
import secrets
from dotenv import load_dotenv
import vk_api
from vkbottle import Keyboard, KeyboardButtonColor, Text

load_dotenv()
TOKEN = str(os.getenv('TOKEN'))
PASSWORD = str(os.getenv('PASSWORD'))

def is_admin(u_id: int) -> bool :
    with open('temp_data.json', 'r') as file :
        data = json.load(file)
    if u_id in data['admin'] : return True
    return False

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
    def __init__(self, token: str, u_id: int):
        self.vk = VK(token)
        self.id = u_id
        
    def add_admin(self) -> None :
        with open('temp_data.json', 'r') as file :
            data = json.load(file)
        data['admin'].append(self.id)
        with open('temp_data.json', 'w') as file :
            json.dump(data, file, indent=4)
        self.vk.send_message(self.id, "Вы получили статус администратора!")

    def mk_cod(self) -> None :
        if not is_admin(self.id) :
            return None
        cod = secrets.token_urlsafe(16)
        with open('temp_data.json', 'r') as file :
            data = json.load(file)
        data['cods'].append(cod)
        with open('temp_data.json', 'w') as file :
            json.dump(data, file, indent=4)
        self.vk.send_message(self.id, cod)