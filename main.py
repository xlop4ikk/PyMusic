import tkinter as tk
import string
import random
from tkinter import END
from tkinter import filedialog
import requests
from bs4 import BeautifulSoup as BS

#-----------------------------------------------------------
# Создание формы
#-----------------------------------------------------------

lst = []
link_lst = []

root = tk.Tk()
root.title("PyMusic")
root.geometry("380x620")
root.resizable(False, False)
root.configure(bg="white")

label_1 = tk.Label(root, text="Введите имя исполнителя:", bg="white", fg="black", font="Consolas")
text_box_1 = tk.Entry(root, width=30)
editor = tk.Text(height=5)

label_2 = tk.Label(root, text="Каталог для скачивания:", bg="white", fg="black", font="Consolas")
text_box_2 = tk.Entry(root, width=30)

label_3 = tk.Label(root, text="Все треки:", bg="white", fg="black", font="Consolas")
list_box_3 = tk.Listbox(root, width= 30, height=18)

success = tk.Label(root, text="Success!")
error = tk.Label(root, text="Error!")

#-----------------------------------------------------------
# Парсинг названий песен
#-----------------------------------------------------------

def singer_name():
    singer_name = text_box_1.get()
    music_url = f'https://pesni.guru/search/{singer_name}'
    response = requests.get(music_url)
    soup = BS(response.content, 'html.parser') 
    for tableRow in soup.select('p'):
        lst.append(tableRow.text)
    for element in (lst):
        list_box_3.insert(0, element)
        
#-----------------------------------------------------------
# Диалоговое окно выбора каталога для сохранения файла
#-----------------------------------------------------------

def folder_choose():
    filepath = filedialog.askdirectory()
    if filepath == "":
        print('Вы ничего не выбрали!')
    else:
        text_box_2.insert(0, filepath)

#-----------------------------------------------------------
# Получение текста песни
#-----------------------------------------------------------

def music_open():
    singer_name = text_box_1.get()
    music_url = f'https://pesni.guru/search/{singer_name}'
    letters = string.ascii_lowercase
    file_name = ''.join(random.choice(letters) for i in range(10))
    music_url_2 = None
    response = requests.get(music_url)
    soup = BS(response.content, 'html.parser') 
    selection = list_box_3.curselection()[0]
    articles = soup.find_all('p')
    for a in articles:
        link_lst.append(a.find('a')['href'])
    link_lst.reverse()
    for i in range(0, len(link_lst)):
        if selection == i:
            music_url_2 = f'https://pesni.guru{link_lst[i]}'
    # Считывание самого текста
    response_2 = requests.get(music_url_2)
    soup_2 = BS(response_2.content, 'html.parser') 
    articles_div = soup_2.find('div', class_='songtext')
    folder = text_box_2.get()
    my_file = open(f"{folder}/{file_name}.html", "w+", encoding="utf-8")
    my_file.write(f'''<html>
                    <head>
                    <title>text</title>
                    </head> 
                    <body>
                    <h1>Ваш текст</h1>           
                    {articles_div}
                    </body>
                    </html>''')
    my_file.close()

#-----------------------------------------------------------
# Очистка textbox
#-----------------------------------------------------------

def clear():
    text_box_1.delete(0, END)
    text_box_2.delete(0, END)
    list_box_3.delete(0, END)

#-----------------------------------------------------------
# Реализация программы
#-----------------------------------------------------------

button_1 = tk.Button(root, text="Поиск!", command=singer_name)
button_2 = tk.Button(root, text="Выбор каталога!", command=folder_choose)
button_3 = tk.Button(root, text="Создать текстовый файл!", command=music_open)
button_4 = tk.Button(root, text="Очистить!", command=clear)
label_1.pack()
text_box_1.pack()
label_2.pack()
text_box_2.pack()
label_3.pack()
list_box_3.pack()
button_1.pack(ipadx=20, ipady=8, pady=5, side= "top")
button_2.pack(ipadx=20, ipady=8, pady=5, side= "top")
button_3.pack(ipadx=20, ipady=8, pady=5, side= "top")
button_4.pack(ipadx=20, ipady=8, pady=5, side= "top")

root.mainloop()