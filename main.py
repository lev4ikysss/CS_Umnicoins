"""CS -> Talants"""
import random
import os
import json
import secrets
import threading
from dotenv import load_dotenv
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType
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
        self.vk = VkApi(token=token)
        self.longpoll = VkLongPoll(self.vk)

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

vk = VK(TOKEN)

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

    def add_stuff(self) -> None :
        if not is_admin(self.id) :
            return None
        vk.send_message(self.id, "Отправьте название предмета")
        for event in vk.longpoll.listen() :
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == id :
                name = event.message
        vk.send_message(self.id, "Отправьте кол-во ед. предмета")
        for event in vk.longpoll.listen() :
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == id :
                num = event.message
        with open('temp_data.json', 'r') as file :
            data = json.load(file)
        try :
            data['stuff'][name] = int(num)
            with open('temp_data.json', 'w') as file :
                json.dump(data, file, indent=4)
        except :
            vk.send_message(self.id, "Вы ввели не число!")
            return None
        vk.send_message(self.id, "Успешно!")

threads = []
users = []

def logic(id: int, message: str) -> None :
    com = Command(TOKEN, id)
    if message == PASSWORD :
        com.add_admin()
    elif message.lower() == "создать код" :
        com.mk_cod()

def start_chat(id: int, message: str) -> None :
    logic(id, message)
    for event in vk.longpoll.listen() :
        if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == id :
            logic(id, message)

for event in vk.longpoll.listen() :
    if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.user_id in users :
        threads.append(threading.Thread(target=start_chat, args=(event.user_id, event.message)))
        threads[-1].start()
        threads[-1].join()
        users.append(event.user_id)