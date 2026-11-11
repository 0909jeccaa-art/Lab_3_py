import csv
import json
import configparser
import stats_utils as su

# Пороги різких перепадів
THRESHOLDS = {
    "temperature": 7.0,
    "humidity": 20.0,
    "pressure": 5000.0
}

def read_csv(filename):
    """Зчитує дані з CSV і повертає словник з показниками."""
    data = {"temperature": {}, "humidity": {}, "pressure": {}}
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                ts = row['timestamp'].strip()
                data["temperature"][ts] = float(row['temperature'])
                data["humidity"][ts] = float(row['humidity'])
                data["pressure"][ts] = float(row['pressure'])
    except FileNotFoundError:
        print(f"Помилка: Файл {filename} не знайдено.")
    except Exception as e:
        print(f"Помилка при читанні CSV: {e}")
    return data

def read_config(filename):
    """Зчитує файл конфігурації INI."""
    config_dict = {}
    config = configparser.ConfigParser()
    try:
        config.read(filename, encoding='utf-8')
        for section in config.sections():
            if 'stats' in config[section]:
                # Розбиваємо рядок на список, видаляючи зайві пробіли
                stats_list = [s.strip() for s in config[section]['stats'].split(',')]
                config_dict[section] = stats_list
    except Exception as e:
        print(f"Помилка при читанні конфігурації: {e}")
    return config_dict

def main():
    # 1. Зчитування даних
    data = read_csv('data.csv')
    if not data or not data["temperature"]:
        return

    # 2. Зчитування налаштувань
    config = read_config('config.ini')
    if not config:
        return

    results = {}

    # 3. Обробка кожного параметра
    for param_name, param_data in data.items():
        if param_name not in config:
            continue
            
        # Виводимо таблицю значень
        su.print_table(param_name, param_data)
        
        # Підготовка даних для розрахунків
        timestamps = list(param_data.keys())
        values = list(param_data.values())
        stats_to_calc = config[param_name]
        
        results[param_name] = {}
        
        # Обчислення необхідних характеристик
        if 'average' in stats_to_calc:
            results[param_name]['average'] = su.get_average(values)
        if 'min' in stats_to_calc:
            results[param_name]['min'] = su.get_min(values)
        if 'max' in stats_to_calc:
            results[param_name]['max'] = su.get_max(values)
        if 'median' in stats_to_calc:
            results[param_name]['median'] = su.get_median(values)
        if 'jumps' in stats_to_calc:
            threshold = THRESHOLDS.get(param_name, 0)
            results[param_name]['jumps'] = su.detect_jumps(values, timestamps, threshold)

    # 4. Збереження результатів у JSON
    try:
        with open('results.json', 'w', encoding='utf-8') as json_file:
            json.dump(results, json_file, indent=4, ensure_ascii=False)
        print("\nРезультати успішно збережено у файлі results.json")
    except Exception as e:
        print(f"\nПомилка при збереженні JSON: {e}")

if __name__ == "__main__":
    main()