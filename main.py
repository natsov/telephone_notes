import os
import sys
import csv
import re

PAGES = 5


def load_notes():
    """Загрузка контактов из файла"""
    telephone_notes = []
    with open('telephone_notes.csv', 'r', newline='') as f:
        file_reader = csv.reader(f)
        for row in file_reader:
            telephone_notes.append(row)
    return telephone_notes


def save_notes(telephone_notes):
    """Сохранение записи в файл"""
    with open('telephone_notes.csv', 'w', newline='') as f:
        file_writer = csv.writer(f)
        file_writer.writerows(telephone_notes)


def print_notes_by_rows(note):
    """Вывод записей"""
    numder_row, last_name, name, surname, organization, work_phone, private_phone = note
    print(f"{numder_row} {last_name:<15}\t\t{name:<15}\t\t{surname:<15}\t\t{organization:<25}\t\t{work_phone:<20}\t\t{private_phone}")


def display_notes(telephone_notes):
    """Вывод страниц телефонного справочника"""
    total_pages = (len(telephone_notes) + PAGES - 1) // PAGES
    current_page = 1
    while True:
        if telephone_notes:
            start_index = (current_page - 1) * PAGES
            page_contacts = telephone_notes[start_index:start_index + PAGES]
            print("\n~~~Контакты~~~")
            print(f"№{'':<2}Фамилия{'':<15}Имя{'':<17}Отчество{'':<12}Название организации{'':<12}Рабочий телефон{'':<13}Личный телефон")
            for contact in page_contacts:
                print_notes_by_rows(contact)
            print(f"\nСтраница {current_page}/{total_pages}\n")
        else:
            print('\nЗаписи отсутствуют!\n')
            break
        if total_pages == 1:
            break
        command = input("Введите 'n' для следующей страницы, 'p' для предыдущей страницы или 'q' для выхода: ")
        if command == "n" and current_page < total_pages:
            current_page += 1
        elif command == "p" and current_page > 1:
            current_page -= 1
        elif command == "q":
            break
    return True


def get_valid_input(prompt):
    """Запрашивает и возвращает сообщение о корректности ввод от пользователя"""
    while True:
        user_input = input(prompt)
        if isinstance(user_input, str) and not re.search(r'\d', user_input):
            return user_input
        else:
            print("Ошибка: некорректный тип данных. Попробуйте снова.")


def get_valid_phone(prompt):
    """Запрашивает и возвращает валидный номер телефона"""
    while True:
        phone = input(prompt)
        if re.match(r"^[\d+]+$", phone) and len(phone) > 4:
            return phone
        else:
            print("Ошибка: некорректный тип данных. Попробуйте снова.")


def add_note(telephone_notes):
    """Добавление новой записи в файл"""
    print('\n~~~Добавление новой записи~~~')
    second_name = get_valid_input('Фамилия: ')
    name = get_valid_input('Имя: ')
    surname = get_valid_input('Отчество: ')
    organization = input('Название организации: ')
    work_phone = get_valid_phone('Рабочий телефон: ')
    private_phone = get_valid_phone('Личный телефон: ')
    try:
        telephone_notes.append([str(len(telephone_notes) + 1), second_name, name, surname, organization, work_phone, private_phone])
        save_notes(telephone_notes)
        print('Запись успешно добавлена!\n')
    except Exception as e:
        print(f'Ошибка при добавлении записи:', e)
        add_note(telephone_notes)


def edit_note(telephone_notes):
    """Редактирование записи"""
    while True:
        display_notes(telephone_notes)
        number_row_edit = int(input('Введите номер записи из справочника, которую требуется изменить: '))
        if 0 < number_row_edit <= len(telephone_notes):
            print('1.Фамилия\n2.Имя\n3.Отчество\n4.Название организации\n5.Рабочий телефон\n6.Личный телефон\n')
            number_param_edit = int(input('Выберите, какой параметр вы хотите изменить: '))
            new_param_note = input('Введите новое значение: ')
            telephone_notes[number_row_edit - 1][number_param_edit] = new_param_note
            save_notes(telephone_notes)
            print('Запись успешно изменена!\n')
            break
        else:
            print('Некорректный ввод номера записи')


def search_note(telephone_notes):
    """Поиск записей"""
    while True:
        search_phrase = input('Введите фразу для поиска: ')
        result = []
        for row in telephone_notes:
            if search_phrase.lower() in [field.lower() for field in row]:
                result.append(row)
        if result:
            print(f'Результат поиска: ({len(result)})')
            for contact in result:
                print_notes_by_rows(contact)
            print('\n')
            break
        else:
            print('Записей не найдено')


def main():
    telephone_notes = load_notes()

    while True:
        print("~~~Телефонный справочник~~~")
        print("1. Вывод записей")
        print("2. Добавить новую запись")
        print("3. Редактировать запись")
        print("4. Поиск записей")
        print("5. Выход")
        command_number = input("Введите номер команды: ")

        if command_number == "1":
            display_notes(telephone_notes)
        elif command_number == "2":
            add_note(telephone_notes)
        elif command_number == "3":
            edit_note(telephone_notes)
        elif command_number == "4":
            search_note(telephone_notes)
        elif command_number == "5":
            break
        else:
            print("Ошибка при вводе.")


if __name__ == "__main__":
    main()