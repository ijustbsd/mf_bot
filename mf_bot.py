# -*- coding: utf-8 -*-
import datetime
import sys

import vk_api
from vk_api.longpoll import VkEventType, VkLongPoll

from answers import *


class VkBot():
    def __init__(self, login, password):
        self.vk_session = vk_api.VkApi(login, password)
        try:
            self.vk_session.auth()
            self.listener()
        except vk_api.AuthError as error_msg:
            print(error_msg)

    def sender(self, user_id, message):
        vk = self.vk_session.get_api()
        vk.messages.send(user_id=user_id, message=message)

    def answerer(self, text):
        numbers = [str(i) for i in range(1, 8)]
        # Расписание на завтра
        if text in ('rz', 'рз'):
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            wd = tomorrow.weekday()
            chisl = tomorrow.isocalendar()[1] % 2
            return rasp_chisl[wd] if chisl else rasp_znam[wd]
        # Расписание на день недели
        elif text in numbers:
            i = int(text) - 1
            if rasp_chisl[i] == rasp_znam[i]:
                return rasp_today[i] + rasp_chisl[i]
            else:
                return '%sЧислитель:\n%s\nЗнаменатель:\n%s' % (\
                    rasp_today[i],
                    rasp_chisl[i],
                    rasp_znam[i])
        # Расписание звонков
        elif text in ('звонки', 'з', 'z'):
            return rasp_zvon
        # Расписание на сегодня
        else:
            today = datetime.date.today()
            wd = today.weekday()
            chisl = today.isocalendar()[1] % 2
            return rasp_chisl[wd] if chisl else rasp_znam[wd]

    def listener(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                if event.to_me:
                    answer = self.answerer(event.text)
                    self.sender(event.user_id, answer)

if __name__ == '__main__':
    bot = VkBot(sys.argv[1], sys.argv[2])
