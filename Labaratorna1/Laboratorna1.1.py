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

# Функція для фільтрації символів на основі мови
def filter_text_by_language(text, language):
    if language == 'ukrainian':
        # Українські букви
        pattern = r'[А-ЩЬЮЯЄІЇҐа-щьюяєіїґ]'
    elif language == 'german':
        # Німецькі букви
        pattern = r'[A-Za-zÄÖÜäöüß]'
    elif language == 'english':
        # Англійські букви
        pattern = r'[A-Za-z]'
    else:
        return ''

    return ''.join(re.findall(pattern, text))

# Функція для аналізу тексту за мовою
def analyze_language_text(text, language_name):
    print(f"\nАналіз для {language_name.capitalize()}:")
    if len(text) == 0:
        print(f"Немає символів для {language_name.capitalize()}.")
        return

    freqs = Counter(text)  # Підрахунок частоти символів
    sorted_freqs = sorted(freqs.items(), key=lambda x: x[1])  # Сортування за частотою

    # Виведення символів і їх частоти
    print("Символ | Частота")
    print("-----------------")
    for char, freq in sorted_freqs:
        print(f"{repr(char):^7} | {freq}")

    # Обчислення і виведення ентропії
    entropy = calculate_entropy(freqs)
    print(f"\nЕнтропія для {language_name.capitalize()}: {entropy:.4f} біт на символ")

    # Обчислення і виведення кількості інформації
    total_info = calculate_information(entropy, len(text))
    print(f"Кількість інформації в {language_name.capitalize()}: {total_info:.4f} біт\n")

# Основна функція для аналізу тексту на всіх мовах
def analyze_text(text):
    # Фільтрація тексту для кожної мови
    ukrainian_text = filter_text_by_language(text, 'ukrainian')
    german_text = filter_text_by_language(text, 'german')
    english_text = filter_text_by_language(text, 'english')

    # Аналіз тексту українською
    analyze_language_text(ukrainian_text, 'українською')

    # Аналіз тексту німецькою
    analyze_language_text(german_text, 'німецькою')

    # Аналіз тексту англійською
    analyze_language_text(english_text, 'англійською')

# Функція для аналізу тексту на обраній мові
def analyze_single_language_text(text, language):
    filtered_text = filter_text_by_language(text, language)
    if language == 'ukrainian':
        analyze_language_text(filtered_text, 'українською')
    elif language == 'german':
        analyze_language_text(filtered_text, 'німецькою')
    elif language == 'english':
        analyze_language_text(filtered_text, 'англійською')

# Функція для читання тексту з файлу з обробкою помилок кодування
def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except UnicodeDecodeError:
        # Спробуємо інше кодування (наприклад, cp1251)
        try:
            with open(file_path, 'r', encoding='cp1251') as file:
                return file.read()
        except UnicodeDecodeError:
            print(f"Помилка: не вдалося прочитати файл {file_path} ні в utf-8, ні в cp1251.")
            return None
    except FileNotFoundError:
        print(f"Помилка: файл {file_path} не знайдено.")
        return None

# Основна функція
def main():
    # Введення вибору методу
    choice = input("Ви хочете ввести текст вручну (1) чи завантажити з файлу (2)? Введіть 1 або 2: ")

    if choice == '1':
        # Введення тексту вручну
        text = input("Введіть текст: ")
    elif choice == '2':
        # Введення шляху до файлу
        file_path = input("Введіть шлях до файлу з текстом: ")

        # Читання тексту з файлу
        text = read_file(file_path)

        # Перевірка, чи вдалося завантажити текст
        if not text:
            return
    else:
        print("Неправильний вибір. Будь ласка, введіть 1 або 2.")
        return

    # Вибір аналізу: однієї мови чи всіх
    language_choice = input("Оберіть мову для аналізу - українська (1), німецька (2), англійська (3), або всі мови одразу (4): ")

    if language_choice == '1':
        analyze_single_language_text(text, 'ukrainian')
    elif language_choice == '2':
        analyze_single_language_text(text, 'german')
    elif language_choice == '3':
        analyze_single_language_text(text, 'english')
    elif language_choice == '4':
        analyze_text(text)
    else:
        print("Неправильний вибір мови.")

# Запуск програми
if __name__ == "__main__":
    main()

