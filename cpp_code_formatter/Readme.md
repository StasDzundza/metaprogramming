# Форматувальник C++ коду
# Автор
 Дзундза Станіслав Васильови
 # Як використовувати
 Для використання форматувальника потрібно перейти в головну директорію проєкту, де знаходиться файл main.py та запустити в цій папці командний рядок.
Для запуску форматувальника потрібно в командному рядку ввести `python main.py` та параметри. Список доступних параметрів:

- `python main.py -h` або `python main.py --help` - виводить в консоль допомогу для запуску форматувальника.
- `python main.py -v` або `python main.py --verify` - записує в файл `log.log` наявні помилки форматування в файлі не змінюючи його.
- `python main.py [--format path_to_config_file] (-f|-d|-p) path_to_cpp_file_or_dir` - запускає роботу форматувальника. Параметри у [] необов'язкові, вони встановлюють конфіг(файл у форматі json), за допомогою яких буде відбуватись форматування. Якщо його не встановити - буде використовуватись конфіг за замовчуванням. З () потрібно вибрати один параметр, де -f - форматування файлу, -d - форматування файлів у директорії, -p - форматування файлів у цілому проекті.
- Приклад файлу конфігурацій знаходиться в кореневій директорії, саме він використовується за замовчуванням(`config.py`) 
- Тестовий приклад використання `python main.py -f Test/test_code.cpp`.
- Результат буде збережений у файл із приставкою `_formatted`. Помилки про стиль початкового файлу  будуть виведені у файл `log.log`