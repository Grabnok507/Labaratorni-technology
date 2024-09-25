from collections import Counter
import math
import re

# Функция для подсчета энтропии
def calculate_entropy(freqs):
    total = sum(freqs.values())  # Общее количество символов
    entropy = 0
    for freq in freqs.values():
        p = freq / total
        entropy -= p * math.log2(p)
    return entropy

# Функция для подсчета количества информации
def calculate_information(entropy, length):
    return entropy * length

# Функция для фильтрации символов на основе языка
def filter_text_by_language(text, language):
    if language == 'ukrainian':
        # Украинские буквы
        pattern = r'[А-ЩЬЮЯЄІЇҐа-щьюяєіїґ]'
    elif language == 'german':
        # Немецкие буквы
        pattern = r'[A-Za-zÄÖÜäöüß]'
    elif language == 'english':
        # Английские буквы
        pattern = r'[A-Za-z]'
    else:
        return ''

    return ''.join(re.findall(pattern, text))

# Функция для анализа текста по языку
def analyze_language_text(text, language_name):
    print(f"\nАнализ для {language_name.capitalize()}:")
    if len(text) == 0:
        print(f"Нет символов для {language_name.capitalize()}.")
        return

    freqs = Counter(text)  # Подсчет частоты символов
    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1])  # Сортировка по частоте

    # Вывод символов и их частоты
    print("Символ | Частота")
    print("-----------------")
    for char, freq in sorted_freqs:
        print(f"{repr(char):^7} | {freq}")

    # Вычисление и вывод энтропии
    entropy = calculate_entropy(freqs)
    print(f"\nЭнтропия для {language_name.capitalize()}: {entropy:.4f} бит на символ")

    # Вычисление и вывод количества информации
    total_info = calculate_information(entropy, len(text))
    print(f"Количество информации в {language_name.capitalize()}: {total_info:.4f} бит\n")

# Основная функция для анализа текста на всех языках
def analyze_text(text):
    # Фильтрация текста для каждого языка
    ukrainian_text = filter_text_by_language(text, 'ukrainian')
    german_text = filter_text_by_language(text, 'german')
    english_text = filter_text_by_language(text, 'english')

    # Анализ текста на украинском
    analyze_language_text(ukrainian_text, 'украинском')

    # Анализ текста на немецком
    analyze_language_text(german_text, 'немецком')

    # Анализ текста на английском
    analyze_language_text(english_text, 'английском')

# Функция для анализа текста на выбранном языке
def analyze_single_language_text(text, language):
    filtered_text = filter_text_by_language(text, language)
    if language == 'ukrainian':
        analyze_language_text(filtered_text, 'украинском')
    elif language == 'german':
        analyze_language_text(filtered_text, 'немецком')
    elif language == 'english':
        analyze_language_text(filtered_text, 'английском')

# Функция для чтения текста из файла с обработкой ошибок кодировки
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Попробуем другую кодировку (например, cp1251)
        try:
            with open(file_path, 'r', encoding='cp1251') as file:
                return file.read()
        except UnicodeDecodeError:
            print(f"Ошибка: не удалось прочитать файл {file_path} ни в utf-8, ни в cp1251.")
            return None
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        return None

# Основная функция
def main():
    # Ввод выбора метода
    choice = input("Вы хотите ввести текст вручную (1) или загрузить из файла (2)? Введите 1 или 2: ")

    if choice == '1':
        # Ввод текста вручную
        text = input("Введите текст: ")
    elif choice == '2':
        # Ввод пути к файлу
        file_path = input("Введите путь к файлу с текстом: ")

        # Чтение текста из файла
        text = read_file(file_path)

        # Проверка, удалось ли загрузить текст
        if not text:
            return
    else:
        print("Неверный выбор. Пожалуйста, введите 1 или 2.")
        return

    # Выбор анализа: одного языка или всех
    language_choice = input("Выберите язык для анализа - украинский (1), немецкий (2), английский (3), или все языки сразу (4): ")

    if language_choice == '1':
        analyze_single_language_text(text, 'ukrainian')
    elif language_choice == '2':
        analyze_single_language_text(text, 'german')
    elif language_choice == '3':
        analyze_single_language_text(text, 'english')
    elif language_choice == '4':
        analyze_text(text)
    else:
        print("Неверный выбор языка.")

# Запуск программы
if __name__ == "__main__":
    main()
