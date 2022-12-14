## Парсер Massimo Dutti
Работу скрипта можно посмотреть тут:
- [Massimo Dutti](https://t.me/massimoduttikz)

Скрипт скрейпит (парсит) сайты Massimo Dutti и добавляет в БД информацию о товаре. При следующем запуске проверяет продукт, и в случае изменения цены добавляет новую цену в БД. Если цена снизилась на 15% и меньше, то отправляет на соответствующие Telegram-каналы.

### Установка и настройка
Клонируем репозитории
```
https://github.com/daradan/parser_massimodutti.git
```
Устанавливаем библиотеки
```
pip install -r requirements.txt
```
Создаем файл ___.env___ и заполняем свои данные
```
TG_TOKEN=...
TG_CHANNEL=@...
TG_CHANNEL_ERROR=...
```

____
## Massimo Dutti Parser
You can see how the script works here:
- [Massimo Dutti](https://t.me/massimoduttikz)

The script scrapes (parses) the Massimo Dutti sites and adds the product information to the database. The next time it runs, it checks the product, and if the price has changed, it adds the new price to the database. If the price has dropped by 15% or less, it sends to the appropriate Telegram feeds.

### Installation and setup
Clone repositories
```
https://github.com/daradan/parser_massimodutti.git
```
Installing libraries
```
pip install -r requirements.txt
```
Create file ___.env___ and fill in your data
```
TG_TOKEN=...
TG_CHANNEL=@...
TG_CHANNEL_ERROR=...
```