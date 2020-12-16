from discord.ext.commands import BadArgument, Converter
from datetime import timedelta


#-----------------------------+
# Типы ошибок конвертирования |
#-----------------------------+
# Польза этих кастомных ошибок форматирования в следующем
# Если при обработке команды какой-то аргумент не удалось конверитровать в другой тип
# То такая ошибка активирует ивент on_command_error(...)
# Внутри этого ивента можно "распаковывать" эти ошибки и сообщать пользователям что именно произошло

class BadInt(BadArgument):
    def __init__(self, argument):
        """
        Вызывается, когда не удаётся конвертировать строку в целое число.
        Несёт в себе аргумент, который спровоцировал ошибку.
        """
        self.argument = argument


class BadTimedelta(BadArgument):
    def __init__(self, argument):
        """
        Вызывается, когда не удаётся конвертировать строку в промежуток времени <datetime.timedelta>
        Несёт в себе аргумент, который спровоцировал ошибку.
        """
        self.argument = argument


class BadBool(BadArgument):
    def __init__(self, argument):
        """
        Вызывается, когда не удаётся конвертировать строку в логическую переменную
        Несёт в себе аргумент, который спровоцировал ошибку.
        """
        self.argument = argument


#-----------------------------+
#         Конвертеры          |
#-----------------------------+
# В библиотеке discord.py заранее предусмотрены очень многие конвертеры
# Но всё-таки не все, и вот некоторые довольно полезные дополнительные конвертеры

class IntConverter(Converter):
    async def convert(self, ctx, argument):
        """
        Конвертер строки в целое число
        -> Возвращает целое число или вызывает ошибку форматирования
        """
        try:
            return int(argument)
        except:
            raise BadInt(argument)


class TimedeltaConverter(Converter):
    async def convert(self, ctx, argument):
        """
        Предполагается, что аргумент отформатирован как в этом примере: "1d5h30m10s"
        (1 день 5 часов 30 минут 10 секунд)
        -> Возвращает соответствующий объект класса <datetime.timedelta>
        """
        # Игнор регистра
        rest = argument.lower()
        # Если аргумент это просто целое число, то по умолчанию это минуты
        if rest.isdigit():
            td = timedelta(minutes=int(rest))
        else:
            tkeys = ["d", "h", "m", "s"]
            # Здесь мы создаём словарик, где всех единиц времени по нулю
            raw_delta = {tk: 0 for tk in tkeys}
            # Перебираем все единицы времени
            for tk in tkeys:
                # Отследим первый виток цикла
                # Представим строку "1d5h30m10s" для примера
                # Первый разделитель - "d"
                pair = rest.split(tk, maxsplit=1)
                # Слева в паре находится "1", а справа "5h30m10s"
                if len(pair) < 2:
                    # Если разделителя "d" не было, то считается, что дни не указаны
                    raw_delta[tk] = 0
                else:
                    # Проверяем, является ли левый элемент пары числом
                    value, rest = pair
                    if not value.isdigit():
                        # Если левый элемент пары не число, то вызываем ошибку форматирования
                        raise BadTimedelta(argument)
                    raw_delta[tk] = int(value)
                    # Если мы дошли сюда, то:
                    # 1) Аргумент дней успешно считался
                    # 2) Осталось конвертировать "5h30m10s"
                    # В следующих 3 шагах цикла мы конвертируем 5h, 30m и 10s
            # Вбиваем полученные данные в timedelta
            td = timedelta(days=raw_delta["d"], hours=raw_delta["h"], minutes=raw_delta["m"], seconds=raw_delta["s"])
        # 0 секунд это отстой, так что лучше рассмотреть этот случай
        if td.total_seconds() > 0:
            return td
        raise BadTimedelta(argument)


class BoolConverter(Converter):
    async def convert(self, ctx, argument):
        """
        Принимает какую-то строку
        -> Возвращает True/False или вызывает ошибку форматирования
        """
        arg = argument.lower()
        if arg in ["on", "yes", "y", "1", "true", "да", "д"]:
            return True
        if arg in ["off", "no", "n", "0", "false", "нет", "н", "не"]:
            return False
        raise BadBool(argument)
