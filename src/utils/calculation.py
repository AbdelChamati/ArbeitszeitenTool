def calculate(start, end):
    from datetime import datetime

    fmt = "%H:%M"

    start_time = datetime.strptime(start, fmt)
    end_time = datetime.strptime(end, fmt)

    diff = (end_time - start_time).seconds / 3600

    overtime = max(0, diff - 5)
    income = overtime * 17

    return round(diff, 2), round(overtime, 2), round(income, 2)
