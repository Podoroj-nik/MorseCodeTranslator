import sys
import time
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from pyfirmata import Arduino


#  Шифровка текста
def translation(text: str):
    text = text.upper()
    morse_code = {
        'А': '.- ', 'Б': '-... ', 'В': '.-- ', 'Г': '--. ', 'Д': '-.. ', 'Е': '. ', 'Ж': '...- ',
        'З': '--.. ', 'И': '.. ', 'Й': '.--- ', 'К': '-.- ', 'Л': '.-.. ', 'М': '-- ', 'Н': '-. ',
        'О': '--- ', 'П': '.--. ', 'Р': '.-. ', 'С': '... ', 'Т': '- ', 'У': '..- ', 'Ф': '..-. ',
        'Х': '.... ', 'Ц': '-.-. ', 'Ч': '---. ', 'Ш': '---- ', 'Щ': '--.- ', 'Ъ': '.--.-. ', 'Ы': '-.--',
        'Ь': '-..- ', 'Э': '..-.. ', 'Ю': '..-- ', 'Я': '.-.- ', 'A': '.-', 'B': '-...', 'C': '-.-.',
        'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..',
        'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-',
        'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---',
        '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 'Ё': '.'
    }

    out_text = ''
    for symb in text:
        if symb == ' ':
            zn = '/'
        elif symb in morse_code:
            zn = morse_code[symb]
        else:
            #  Неизвестный символ
            zn = '#'

        out_text += zn + ' '

    return out_text


#  Передача сигнала
def dlin():
    '''возвращает длинный сигнал на плату Arduino'''
    led_pin.write(1)
    led_pin_2.write(1)
    time.sleep(0.17)
    led_pin.write(0)
    led_pin_2.write(0)


def corot():
    '''возвращает короткий сигнал на плату Arduino'''
    led_pin.write(1)
    led_pin_2.write(1)
    time.sleep(0.03)
    led_pin.write(0)
    led_pin_2.write(0)


def rashif(arg: str):
    '''взависимости от символа выбирает какой сигнал подать на плату Arduino'''
    for i in arg:
        #  Короткий сигнал
        if i == '.':
            corot()
            time.sleep(0.2)

        #  Длинный сигнал
        if i == '-':
            dlin()
            time.sleep(0.2)

        #  Пауза между буквами
        if i == ' ':
            time.sleep(0.1)

        #  Пауза между словами
        if i == '/':
            time.sleep(1)


def save_text(text: str):
    f_name = f'data/MorseCode.txt'
    with open(f_name, "w") as file:
        file.write(text)
    return "Код Морзе сохранён"

def port_search():
    f_name = f'data/input.txt'
    with open(f_name, "r", encoding="utf8") as file:
        text = file.readlines()
    return text


class MorseCoder(QMainWindow):
    def __init__(self):
        self.pos = 0
        super(MorseCoder, self).__init__()
        uic.loadUi('data/Morse_Display.ui', self)

        self.play_Button.clicked.connect(self.play)
        self.save_Button.clicked.connect(self.save)

        self.setFixedSize(self.size())

    def play(self):
        M_code = translation(self.lineEdit.text())
        rashif(M_code)
        return True

    def save(self):
        M_code = translation(self.lineEdit.text())
        save_text(M_code)
        return True


if __name__ == '__main__':

    # инициализация порта
    try:
        port_data = port_search()
        port = port_data[0].strip()
        board = Arduino(port)
        led_pin = board.get_pin(port_data[1].strip())
        led_pin_2 = board.get_pin(port_data[2].strip())
    except Exception:
        print('Извините, порт не найден(((')

    app = QApplication(sys.argv)
    ex = MorseCoder()
    ex.show()
    sys.exit(app.exec())
