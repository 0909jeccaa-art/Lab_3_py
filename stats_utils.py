import statistics

def get_average(values):
    """Повертає середнє значення списку."""
    return round(statistics.mean(values), 2) if values else None

def get_min(values):
    """Повертає мінімальне значення."""
    return min(values) if values else None

def get_max(values):
    """Повертає максимальне значення."""
    return max(values) if values else None

def get_median(values):
    """Повертає медіану."""
    return round(statistics.median(values), 2) if values else None

def detect_jumps(values, timestamps, threshold):
    """
    Виявляє різкі перепади між сусідніми значеннями.
    Повертає список часових міток, де відбувся перепад.
    """
    jumps = []
    for i in range(1, len(values)):
        if abs(values[i] - values[i - 1]) > threshold:
            jumps.append(timestamps[i])
    return jumps

def print_table(parameter_name, data_dict):
    """Виводить таблицю з показниками певного параметра."""
    print(f"\nПоказники для параметра: {parameter_name}")
    print("+----------------------+-------------+")
    print(f"| {'Timestamp':<20} | {parameter_name:<11} |")
    print("+----------------------+-------------+")
    for timestamp, value in data_dict.items():
        print(f"| {timestamp:<20} | {value:<11} |")
    print("+----------------------+-------------+")