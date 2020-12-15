# Что это?
Данный репозиторий содержит небольшие, но полезные при разработке Discord-ботов коды на Python3+ с разъяснениями.

# О кастомных конвертерах
В чём их смысл?<br>
Рассмотрим вот такой способ применения:
```python
@client.command()
async def greet(ctx, *, member: discord.Member):
    await ctx.send(f"Hello, {member.mention}!")
```
Самое волшебное здесь то, что `member: discord.Member` это и есть конвертер. Он срабатывает при вызове команды, получая на входе строку, а на выходе - объект `discord.Member`.<br>
Но что произойдёт, если конвертер не справится?<br>
Библиотека `discord.py` вызовет ивент `on_command_error`.<br>
Надо бы сообщить пользователю, что он ввёл участника неправильно, так что давайте обработаем ошибку, вызвавшую этот ивент.
```python
@client.event
async def on_command_error(ctx, error): # Здесь error это и есть ошибка, которая вызвала ивент
    if isinstance(error, commands.BadArgument): # Проверяем, является ли ошибка результатом конвертирования аргументов
        if isinstance(error, commands.MemberNotFound): # Проверяем, был ли это конвертер именно строки в участника
            await ctx.send(f"Участник {error.argument} не был найден")
        else:
            await ctx.send("Что-то было введено неправильно")
```
Так что если конвертер не спарвится, то вызовется ошибка `commands.BadArguemnt`, которая, в свою очередь, тоже имеет разновидности.<br>
В файле [custom_converters.py](https://github.com/EQUENOS/Discord.py-Code-Samples/blob/main/custom_converters.py) я написал несколько дополнительных конвертеров. Как теперь ими пользоваться?
```python
from custom_converters import BoolConverter, BadBool


@client.command()
async def test(ctx, value: BoolConverter):
    await ctx.send(value)


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument): # Это всё с прошлого раза
        if isinstance(error, commands.MemberNotFound):
            await ctx.send(f"Участник {error.argument} не был найден")
        elif isinstance(error, BadBool): # Вот эта проверка сработает, если наш BoolConverter споткнётся
            await ctx.send(f"Аргумент {error.argument} не похож на логическую переменную...")
        else:
            await ctx.send("Что-то было введено неправильно")
```
