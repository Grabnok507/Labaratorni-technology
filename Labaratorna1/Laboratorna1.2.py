import requests
from bs4 import BeautifulSoup
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

# Функция для очистки текста от HTML тегов
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()

# Функция для фильтрации текста по языкам
def filter_text_by_language(text, language):
    if language == 'ukrainian':
        pattern = r'[А-ЩЬЮЯЄІЇҐа-щьюяєіїґ]'
    elif language == 'russian':
        pattern = r'[А-ЯЁа-яё]'
    elif language == 'english':
        pattern = r'[A-Za-z]'
    else:
        return ''
    return ''.join(re.findall(pattern, text))

# Функция для анализа текста
def analyze_text(text):
    freqs = Counter(text)  # Подсчет частоты символов
    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)  # Сортировка по частоте

    # Вывод символов и их частоты
    print(f"{'Символ':^7} | {'Частота':^7}")
    print("-----------------")
    for char, freq in sorted_freqs:
        print(f"{repr(char):^7} | {freq:^7}")

    # Общее количество символов
    total_chars = len(text)
    print(f"\nОбщее количество символов в тексте: {total_chars}")

    # Вычисление и вывод энтропии
    entropy = calculate_entropy(freqs)
    print(f"\nЭнтропия текста: {entropy:.4f} бит на символ")

    # Вычисление и вывод количества информации
    total_info = calculate_information(entropy, total_chars)
    print(f"Количество информации в тексте: {total_info:.4f} бит")

# Функция для анализа сайта по выбранному языку
def analyze_website_by_language(url, language=None):
    try:
        # Получаем контент с сайта
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный ответ

        # Очищаем текст от HTML тегов
        text = clean_html(response.text)

        # Если язык выбран, фильтруем текст
        if language:
            filtered_text = filter_text_by_language(text, language)
            analyze_text(filtered_text)
        else:
            # Если язык не выбран, анализируем текст для всех языков
            print("\nАнализ текста на украинском языке:")
            analyze_text(filter_text_by_language(text, 'ukrainian'))

            print("\nАнализ текста на русском языке:")
            analyze_text(filter_text_by_language(text, 'russian'))

            print("\nАнализ текста на английском языке:")
            analyze_text(filter_text_by_language(text, 'english'))

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при попытке доступа к сайту: {e}")

# Основная программа
def main():
    url = input("Введите URL сайта для анализа: ")

    # Ввод выбора анализа по языку
    language_choice = input(
        "Выберите язык для анализа - украинский (1), русский (2), английский (3), или все языки сразу (4): "
    )

    if language_choice == '1':
        analyze_website_by_language(url, 'ukrainian')
    elif language_choice == '2':
        analyze_website_by_language(url, 'russian')
    elif language_choice == '3':
        analyze_website_by_language(url, 'english')
    elif language_choice == '4':
        analyze_website_by_language(url)  # Без фильтрации, анализ всех языков
    else:
        print("Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")

if __name__ == "__main__":
    main()

