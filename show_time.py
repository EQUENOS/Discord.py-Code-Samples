def pickform(num: int, wordforms: list):
    """
    NOTE: Аргумент wordforms должен выглядеть так: ['(1) ключ', '(2) ключа', '(5) ключей']
    -> Возвращает нужную форму слова для данного числа, например "1 велосипед" или "2 велосипеда"
    """
    # Числа-исключения от 11 до 14
    if 10 < num < 15: return wordforms[2]
    num = num % 10 # Далее важна только последняя цифра
    if num == 1: return wordforms[0]
    if 1 < num < 5: return wordforms[1]
    return wordforms[2]


def visdelta(delta):
    """
    NOTE: Аргумент delta может быть как секундами, так и объектом <datetime.timedelta>
    -> Возвращает читаемый промежуток времени на русском языке, например "3 минуты 30 секунд"
    """
    # Если delta это просто число, то оно считывается как секунды
    if not isinstance(delta, int): delta = int(delta.total_seconds())
    # Вычисляем и записываем каждую единицу времени
    nt = {}
    nt['s'] = delta % 60; delta //= 60 # Секунды
    nt['m'] = delta % 60; delta //= 60 # Минуты
    nt['h'] = delta % 24; delta //= 24 # Часы
    nt['d'] = delta % 7; delta //= 7 # Дни
    nt['w'] = delta # Недели
    # Далее идут все возможные формы слов в связке с числом (1 банан, 2 банана, 5 бананов)
    wforms = {
        's': ['секунда', 'секунды', 'секунд'],
        'm': ['минута', 'минуты', 'минут'],
        'h': ['час', 'часа', 'часов'],
        'd': ['день', 'дня', 'дней'],
        'w': ['неделя', 'недели', 'недель']
    }
    # Формируем читаемые сочетания для каждой единицы времени
    l = [f'{n} {pickform(n, wforms[k])}' for k, n in nt.items() if n > 0]
    l.reverse() # Чтобы время писалось начиная с недель и заканчивая секундами
    # Склеиваем словосочетания
    return '0.1 секунды' if len(l) == 0 else ' '.join(l)


def visdate(date):
    """
    NOTE: Аргумент date должен быть объектом <datetime.date> или <datetime.datetime>
    -> Возвращает читаемую дату, например "31 декабря 1971"
    """
    # Укажем месяцы в родительном падеже
    months = [
        "декабря", "января", "февраля",
        "марта", "апреля", "мая",
        "июня", "июля", "августа",
        "сентября", "октября", "ноября"
    ] # Позиция месяца в списке соответствует остатку от деления его номера на 12
    return f"{date.day} {months[date.month % 12]} {date.year}"


def vistime(time):
    """
    NOTE: Аргумент time должен быть объектом <datetime.time> или <datetime.datetime>
    -> Возвращает читаемое время в привычном формате - 18:30
    """
    return f"{time.hour}:{time.minute}" if time.minute > 9 else f"{time.hour}:0{time.minute}"


def visdatetime(datetime):
    """
    NOTE: Аргумент date должен быть объектом <datetime.datetime>
    -> Возвращает дату и время в читаемом формате, например "9:00 1 сентября 1999"
    """
    return f"{vistime(datetime)} {visdate(datetime)}"


