# Дни недели с большим и маленьким количеством рабочих дней в году
workdays = {
    'Monday': 0, 
    'Tuesday': 0, 
    'Wednesday': 0, 
    'Thursday': 0, 
    'Friday': 0, 
    'Saturday': 0, 
    'Sunday': 0 
}

# Список дней недели
days_of_week = list(workdays.keys())

def get_day_of_year(is356: bool, day_of_month: int, month: str) -> int:
    '''
    Возвращает номер дня в году
    '''
    days = {
        'January': 0,
        'February': 31,
        'March': 59,
        'April': 90,
        'May': 120,
        'June': 151,
        'July': 181,
        'August': 212,
        'September': 243,
        'October': 273,
        'November': 304,
        'December': 334
    }
    return days[month] + day_of_month + (1 if is356 and days[month] > 58 else 0)

n = int(input().strip())
year = int(input().strip())
holidays = []
for i in range(n):
    day = input().split()
    holidays.append((int(day[0]), day[1]))
first_day = input().strip()

DAYS_NUMBER = 366 if year % 400 == 0 or (year % 4 == 0 and year % 25 != 0) else 365

index_first_day = days_of_week.index(first_day)

workdays[first_day] += 1
if DAYS_NUMBER == 366:
    workdays[days_of_week[(index_first_day + 1) % 7]] += 1

for day in holidays:
    day_of_year = get_day_of_year(DAYS_NUMBER == 366, day[0], day[1])
    day_of_week_index = (day_of_year + index_first_day - 1) % 7
    day_of_week = days_of_week[day_of_week_index]
    workdays[day_of_week] -= 1

great_day, bad_day = max(workdays, key=workdays.get), min(workdays, key=workdays.get)

print(great_day, bad_day)
