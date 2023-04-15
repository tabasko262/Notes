from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QHBoxLayout, QVBoxLayout, QLineEdit, QTextEdit, QInputDialog

import json


app = QApplication([])#створення додатки

# '''Замітки в json'''
# notes = {
#     "Ласкаво просимо!": {
#         "текст": "Це найкращий додаток для заміток у світі!",
#         "теги": ["добро", "інструкція"]
#     }
# } 

# with open("notes_data.json", "w") as file:#записуємо замітки в json
#     json.dump(notes, file)


window = QWidget()#створення вікна додатки
window.resize(900, 600)#розміри вікна
window.setWindowTitle('Notes')#назва вікна

"""ІНТЕРФЕЙС ПРОГРАМИ"""
text_field = QTextEdit()#Велике поле для вводу


list_notes = QListWidget()#список заміток
list_notes_label = QLabel('Список заміток')

#кнопки для дії з замітками
btn_create_note = QPushButton('Створити замітку')
btn_del_note = QPushButton('Видалити замітку')
btn_save_note = QPushButton('Зберегти замітку')


list_tags = QListWidget()#список тегів
list_tags_label = QLabel('Список тегів')

#кнопки для дій з тегами
btn_add_tag = QPushButton('Додати до замітки')
btn_del_tag = QPushButton('Відкріпити від замітки')
btn_search_note = QPushButton('Шукати замітки по тегу')


input_tag = QLineEdit()#поле для вводу тегу
input_tag.setPlaceholderText('Введіть тег...')#надпис пропаде коли ми натиснемо


col1 = QVBoxLayout()
col1.addWidget(text_field)


col2 = QVBoxLayout()
col2.addWidget(list_notes_label)
col2.addWidget(list_notes)


row1 = QHBoxLayout()
row1.addWidget(btn_create_note)
row1.addWidget(btn_del_note)


row2 = QHBoxLayout()
row2.addWidget(btn_save_note)


col2.addLayout(row1)
col2.addLayout(row2)
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(input_tag)


row3 = QHBoxLayout()
row3.addWidget(btn_add_tag)
row3.addWidget(btn_del_tag)


row4 = QHBoxLayout()
row4.addWidget(btn_search_note)


col2.addLayout(row3)
col2.addLayout(row4)


layot_notes = QHBoxLayout()
layot_notes.addLayout(col1, stretch=2)
layot_notes.addLayout(col2, stretch=1)


window.setLayout(layot_notes)

'''ФУНКЦІОНАЛ ПРОГРАМИ'''

'''Робота з текстом замітки'''
def show_note():#функція показу замітки
    key = list_notes.selectedItems()[0].text()
    text_field.clear()
    text_field.setText(notes[key]['текст'])
    list_tags.clear()
    list_tags.addItems(notes[key]['теги'])


def add_note():#функція додавання заміток
    note_name, ok = QInputDialog.getText(window, 'Додати замітку', 'Назва замітки:')
    if note_name and ok != '':
        notes[note_name] = {'текст': '', 'теги': []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]['теги'])
    

def del_note():#функція видалення заміток 
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        text_field.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)


def save_note():#функція збереження заміток
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]['текст'] = text_field.toPlainText()
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)
        

def add_tag():#функція додавання тегів
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        if input_tag.text():
            tag = input_tag.text()
            if not tag in notes[key]['теги']:
                notes[key]['теги'].append(tag)
                list_tags.addItem(tag)
                input_tag.clear()
                with open('notes_data.json', 'w') as file:
                    json.dump(notes, file, sort_keys=True)


def del_tag():#функція видалення тегів
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]['теги'])
        with open('notes_data.json', 'w') as file:
            json.dump(notes, file, sort_keys=True)


def search_note():#функція пошуку заміток по тегу
    if input_tag.text() and btn_search_note.text() == 'Шукати замітки по тегу':
        tag = input_tag.text()
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note] = notes[note]
        btn_search_note.setText("Скинути пошук")
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
    elif input_tag.text() and btn_search_note.text() == "Скинути пошук":
        input_tag.clear()
        list_tags.clear()
        list_notes.text()
        list_notes.addItems(notes)
        btn_search_note.setText('Шукати замітки по тегу')


#Запуск функцій після натиснення кнопки
btn_del_note.clicked.connect(del_note)
btn_save_note.clicked.connect(save_note)
btn_create_note.clicked.connect(add_note)
btn_add_tag.clicked.connect(add_tag)
btn_del_tag.clicked.connect(del_tag)
btn_search_note.clicked.connect(search_note)

list_notes.itemClicked.connect(show_note)


with open('notes_data.json', 'r') as file:
    notes = json.load(file)
list_notes.addItems(notes)



window.show()


app.exec_()

















