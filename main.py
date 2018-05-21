from os import listdir, getcwd
import queue
import threading
from time import sleep


from googletrans import Translator
from termcolor import colored

from pyperclip import paste

translator = Translator()


def get_paste():
    old = ""
    while work:
        sleep(0.5)
        word = paste()
        if word != old:
            qetQueue.put(word)
            old = word


def get_input():
    while work:
        word = input("")
        qetQueue.put(word.strip().lower())


def functPrint():
    while work:
        sleep(0.5)
        if not printQueue.empty():
            text = printQueue.get()
            print("{} {}".format(symbol, text))


def make_dict(name="dictionary.txt"):
    if name in listdir(getcwd()):
        pass
    else:
        with open(name, "w") as f:
            pass


def read_dict(name="dictionary.txt"):
    dictionary = {}
    with open(name, "r") as f:
        for text in f:
            if text:
                listText = text.split("=")
                if len(listText) == 2:
                    dictionary[listText[0].strip()] = listText[1].strip()
    return dictionary


def add_word(eng, pl, name="dictionary.txt"):
    with open(name, "a") as f:
        f.write("{} = {}\n".format(eng, pl))


def translate(word):
    dictionary = read_dict(name)
    if word in dictionary:
        text = dictionary[word]
    else:
        out = translator.translate(text=word, dest="pl")
        text = out.text
        text = text.lower()
        if text != word:
            dictionary[word] = text
            add_word(word, text, name)
    text = colored(text, "white")
    return text


def play(name="dictionary.txt"):
    while work:
        if not qetQueue.empty():
            word = qetQueue.get()
            printQueue.put(word)
            text = translate(word)
            printQueue.put(text)


def main():
    make_dict(name)
    play()


if __name__ == '__main__':
    work = True
    name = "dictionary.txt"
    symbol = colored(">>>", "green")

    qetQueue = queue.Queue()
    printQueue = queue.Queue()

    thread_get_paste = threading.Thread(target=get_paste)
    thread_get_input = threading.Thread(target=get_input)
    thread_functPrint = threading.Thread(target=functPrint)

    thread_get_paste.start()
    thread_get_input.start()
    thread_functPrint.start()
    main()
