import requests
from bs4 import BeautifulSoup
from collections import Counter
import math
import re

# Функція для підрахунку ентропії
def calculate_entropy(freqs):
    total = sum(freqs.values())  # Загальна кількість символів
    entropy = 0
    for freq in freqs.values():
        p = freq / total
        entropy -= p * math.log2(p)
    return entropy

# Функція для підрахунку кількості інформації
def calculate_information(entropy, length):
    return entropy * length

# Функція для очищення тексту від HTML тегів
def clean_html(raw_html):
    soup = BeautifulSoup(raw_html, 'html.parser')
    return soup.get_text()

# Функція для фільтрації тексту за мовами
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

# Функція для аналізу тексту
def analyze_text(text):
    freqs = Counter(text)  # Підрахунок частоти символів
    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)  # Сортування за частотою

    # Виведення символів і їх частоти
    print(f"{'Символ':^7} | {'Частота':^7}")
    print("-----------------")
    for char, freq in sorted_freqs:
        print(f"{repr(char):^7} | {freq:^7}")

    # Загальна кількість символів
    total_chars = len(text)
    print(f"\nЗагальна кількість символів у тексті: {total_chars}")

    # Обчислення і виведення ентропії
    entropy = calculate_entropy(freqs)
    print(f"\nЕнтропія тексту: {entropy:.4f} біт на символ")

    # Обчислення і виведення кількості інформації
    total_info = calculate_information(entropy, total_chars)
    print(f"Кількість інформації у тексті: {total_info:.4f} біт")

# Функція для аналізу сайту за вибраною мовою
def analyze_website_by_language(url, language=None):
    try:
        # Отримуємо контент із сайту
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на успішну відповідь

        # Очищаємо текст від HTML тегів
        text = clean_html(response.text)

        # Якщо вибрана мова, фільтруємо текст
        if language:
            filtered_text = filter_text_by_language(text, language)
            analyze_text(filtered_text)
        else:
            # Якщо мова не вибрана, аналізуємо текст для всіх мов
            print("\nАналіз тексту українською мовою:")
            analyze_text(filter_text_by_language(text, 'ukrainian'))

            print("\nАналіз тексту російською мовою:")
            analyze_text(filter_text_by_language(text, 'russian'))

            print("\nАналіз тексту англійською мовою:")
            analyze_text(filter_text_by_language(text, 'english'))

    except requests.exceptions.RequestException as e:
        print(f"Помилка при спробі доступу до сайту: {e}")

# Основна програма
def main():
    url = input("Введіть URL сайту для аналізу: ")

    # Введення вибору аналізу за мовою
    language_choice = input(
        "Виберіть мову для аналізу - українська (1), російська (2), англійська (3), або всі мови одразу (4): "
    )

    if language_choice == '1':
        analyze_website_by_language(url, 'ukrainian')
    elif language_choice == '2':
        analyze_website_by_language(url, 'russian')
    elif language_choice == '3':
        analyze_website_by_language(url, 'english')
    elif language_choice == '4':
        analyze_website_by_language(url)  # Без фільтрації, аналіз усіх мов
    else:
        print("Неправильний вибір. Будь ласка, виберіть 1, 2, 3 або 4.")

if __name__ == "__main__":
    main()

