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
    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1])  # Сортировка по частоте

    # Вывод символов и их частоты
    print("Символ | Частота")
    print("-----------------")
    for char, freq in sorted_freqs:
        print(f"{repr(char):^7} | {freq}")

    # Общее количество символов
    total_chars = len(text)
    print(f"\nОбщее количество символов в тексте: {total_chars}")

    # Вычисление и вывод энтропии
    entropy = calculate_entropy(freqs)
    print(f"\nЭнтропия текста: {entropy:.4f} бит на символ")

    # Вычисление и вывод количества информации
    total_info = calculate_information(entropy, total_chars)
    print(f"Количество информации в тексте: {total_info:.4f} бит")

# Основная функция для анализа сайта
def analyze_website(url):
    try:
        # Получаем контент с сайта
        response = requests.get(url)
        response.raise_for_status()  # Проверка на успешный ответ

        # Очищаем текст от HTML тегов
        text = clean_html(response.text)

        # Анализ текста
        analyze_text(text)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при попытке доступа к сайту: {e}")

# Основная программа
def main():
    url = input("Введите URL сайта для анализа: ")
    analyze_website(url)

if __name__ == "__main__":
    main()
