# Casino-bot
Это пет-проект Telegram-бот, в котором игра реализована с помощью так называемых *dice-emojis* (🏀, 🎰 и другие).

В 2020 году в Telegram появилась [прорывная фича](https://telegram.org/blog/folders#and-one-more-thing) - dice-emoji
кубика 🎲. Позже появились 🏀, ⚽️, 🎯, 🎳 и 🎰. Их особенность в том, что бот не может управлять значением, которое выпадет
пользователю (а значит, это первое честное казино в истории!).

## Содержание
- [Технологии](#технологии)
- [Запуск](#Запуск)
- [To do](#to-do)

## Технологии
- [Telegram](https://t.me)
- [Aiogram](https://aiogram.dev/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

## Запуск
Проект запускается в двух контейнерах Docker - приложение и контейнер с БД Postgres.
То есть для запуска вам нужен Docker.

Сделайте git-clone проекта
```bash
git clone https://github.com/Vester1/TG-Bot-casino.git
cd casinobot
```

Скопируйте файл _.env.example_ в _.env_ и откройте его
```bash
cp .env.example .env
nano .env
```
Добавьте свой токен и задайте пароль БД.\
Теперь соберите контейнер командой:
```bash
docker compose up --build
```

## To do
- [ ] Добавить inline режим для работы в группах
- [ ] Добавить монетизацию (если это законно) 
- [ ] Добавить английский
