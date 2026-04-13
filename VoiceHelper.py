import json
import os
import time as t
import sys
import speech_recognition as sr
import multiprocessing

# Определяем путь к конфигу рядом с .exe или .py файлом
if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILE_NAME = os.path.join(BASE_DIR, "config.json")


def listen_me():
    #Функция для работы с микрофоном
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration=0.5)
            print("\n Слушаю вас...")
            audio = r.listen(source, timeout=10, phrase_time_limit=5)
            return r.recognize_google(audio, language="ru-RU").lower()
    except Exception:
        return ""



def main():
    # 1. Загрузка или создание конфигурации
    data = None
    if os.path.exists(FILE_NAME):
        try:
            with open(FILE_NAME, "r", encoding="utf-8") as f:
                data = json.load(f)
        except:
            os.remove(FILE_NAME)
            data = None

    if not data:
        print("                     --- НАСТРОЙКА ПУТЕЙ И КОМАНД ---")
        print("--- ПОСЛЕДНИЕ ТРИ ПУТЯ БУДУТ ИСПОЛЬЗЫВАТЬСЯ ДЛЯ ОДИНАРНОГО И КОМБО, ШЕСТОЕ СЛОВО ДЛЯ НЕГО ---")
        p1 = input('Путь к 1 .exe: ')
        p2 = input('Путь к 2 .exe: ')
        p3 = input('Путь к 3 .exe: ')
        p4 = input('Путь к 4 .exe: ')
        p5 = input('Путь к 5 .exe: ')

        w1 = input('Слово для файла 1: ').lower()
        w2 = input('Слово для файла 2: ').lower()
        w3 = input('Слово для файла 3: ').lower()
        w4 = input('Слово для файла 4: ').lower()
        w5 = input('Слово для файла 5: ').lower()
        w6 = input('Слово для комбо 6: ').lower()

        data = {
            "wor1": w1, "wor2": w2, "wor3": w3, "wor4": w4, "wor5": w5, "wor6": w6,
            "pat1": p1, "pat2": p2, "pat3": p3, "pat4": p4, "pat5": p5
        }

        with open(FILE_NAME, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print("Настройки сохранены!\n")

    # 2. Основной цикл работы
    text = listen_me()
    print(f"Вы сказали: {text}")

    if text:
        if data["wor1"] in text:
            os.startfile(data["pat1"])
        elif data["wor2"] in text:
            os.startfile(data["pat2"])
        elif data["wor3"] in text:
            os.startfile(data["pat3"])
        elif data["wor4"] in text:
            os.startfile(data["pat4"])
        elif data["wor5"] in text:
            os.startfile(data["pat5"])
        elif data["wor6"] in text:
            os.startfile(data["pat3"]);
            t.sleep(0.5)
            os.startfile(data["pat4"]);
            t.sleep(0.5)
            os.startfile(data["pat5"])
        else:
            print("Команда не найдена")

    print("\nЗавершение через 4 секунды...")
    t.sleep(2)


if __name__ == '__main__':
    # КРИТИЧЕСКИ ВАЖНО: предотвращает открытие лишних окон в .exe
    multiprocessing.freeze_support()

    try:
        main()
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter для выхода...")
