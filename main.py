"""CS -> Talants"""
import os
import json
import random
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
        try :
            for event in self.vk.longpoll.listen() :
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == self.id :
                    name = event.message
                    break
        except :
            return None
        vk.send_message(self.id, "Отправьте кол-во ед. предмета")
        try :
            for event in self.vk.longpoll.listen() :
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == self.id :
                    num = event.message
                    break
        except :
            return None
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
    
    def activate_cod(self, message: str) -> None :
        with open('temp_data.json', 'r') as file :
            data = json.load(file)
        if not message in data['cods'] :
            return None
        keys = list(data['stuff'].keys())
        values = list(data['stuff'].values())
        while 0 in values :
            i = values.index(0)
            keys.pop(i)
            values.pop(i)
        if len(keys) == 0 :
            self.vk.send_message(self.id, "Извините, но сейчас нету призов!")
            return None
        data['cods'].remove(message)
        with open('temp_data.json', 'w') as file :
            json.dump(data, file, indent=4)
        summ = sum(values)
        msg = "Здравствуйте! Вы активировали промокод на розыгрыш призов!\nПримерные шансы на выигрыш:\n"
        for i in range(0, len(keys)) :
            key = keys[i]
            chance = values[i]/(summ*5)
            msg += f"{key}: {chance*100}%\n"
        msg += "Нажмите кнопку \"Запуск\" для участия в розыгрыше."
        keyboard = (
            Keyboard(one_time=True, inline=False)
            .add(Text("Запуск"), color=KeyboardButtonColor.PRIMARY)
        ).get_json()
        self.vk.send_keyboard(self.id, msg, keyboard)
        try :
            for event in self.vk.longpoll.listen() :
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == self.id :
                    break
        except :
            return None
        keyboard = (
            Keyboard(one_time=True, inline=False)
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .row()
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
            .add(Text("📦"), color=KeyboardButtonColor.PRIMARY)
        ).get_json()
        self.vk.send_keyboard(self.id, "Выберите коробку", keyboard)
        try :
            for event in self.vk.longpoll.listen() :
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == self.id :
                    break
        except :
            return None
        chance = random.randint(1, 10)
        if chance <= 8 :
            self.vk.send_message(self.id, "Увы, но вам ничего не выпало!")
            return None
        stuff = []
        try :
            for i in range(0, len(keys)) :
                for j in range(0, values[i]) :
                    stuff.append(keys[i])
        except :
            return None
        item = stuff[random.randint(0, len(stuff))]
        with open('temp_data.json', 'r') as file :
            data = json.load(file)
        data['stuff'][item] -= 1
        with open('temp_data.json', 'w') as file :
            json.dump(data, file, indent=4)
        self.vk.send_message(self.id, f"Поздравляю! Вы выиграли {item}\nНапишите @luckybox111 для выдачи!")

vk = VK(TOKEN)
threads = []
users = []

def logic(id: int, message: str) -> None :
    com = Command(TOKEN, id)
    if message == PASSWORD :
        com.add_admin()
    elif message.lower() == "создать код" :
        com.mk_cod()
    elif message.lower() == "добавить приз":
        com.add_stuff()
    else :
        com.activate_cod(message)

def start_chat(id: int, message: str) -> None :
    logic(id, message)
    while True :
        try :
            for event in vk.longpoll.listen() :
                if event.type == VkEventType.MESSAGE_NEW and event.to_me and event.user_id == id :
                    logic(id, event.message)
        except :
            pass

while True :
    try :
        for event in vk.longpoll.listen() :
            if event.type == VkEventType.MESSAGE_NEW and event.to_me and not event.user_id in users :
                threads.append(threading.Thread(target=start_chat, args=(event.user_id, event.message)))
                threads[-1].start()
                threads[-1].join()
                users.append(event.user_id)
    except  :
        pass