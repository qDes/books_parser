# Парсер книг с сайта tululu.org

Проект скачивания книг жанра фантастика с обложками и составления файла с описанием скачанных книг.

### Как установить

Для работы необходим python версии 3.6+. <br>
Установка зависимостей:
```
pip3 install -r requirements.txt
```

### Использование
Запуск скрипта:
```
python3 parse_tululu_category.py --start_page %start_page% --end_page %end_page%
```
Для запуска необходимо указать первую и последнюю страницу с которой будут скачиваться книги(если не указывать аргумент end_page парсер пройдёт до последней страницы - 701).<br>
После работы скрипта в папку ```books/``` скачаются книги, в папку ```images/``` скачаются обложки книг, в файле ```description``` содержится описание скаченной библиотеки в формате json.<br>
Структура файла description:
```json
[
  {
      "title": "Название книги",
      "author": "Автор книги",
      "img_src": "images/обложка.жпг",
      "book_path": "books/книга.txt",
      "comments": ["комментарий1", "комментарий2"],
      "genres": ["жанр1", "жанр2"]
  }, 
  ...
]
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).