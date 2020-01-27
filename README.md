# Парсер книг с сайта tululu.org

Парсер скачивает и сохраняет книги в жанре фантастика.

### Как установить

Для работы необходим python версии 3.6+. <br>
Установка зависимостей:
```
pip3 install -r requirements.txt
```

### Использование
Запуск скрипта:
```
python3 parse_tululu_category.py --start_page %start_page% --end_page %end_page% --file %description.json%
```
При запуске скрипта указывается первая и последняя страница библиотеки сайта(если не указывать аргумент end_page парсер пройдёт до последней страницы - 701), аргумент file указывает на файл описания библиотеки.<br>
После работы программы папка ```books/``` содержит книги, папка ```images/``` - обложки книг, файл ```description.json``` - описание скачанной библиотеки. 
Структура файла с описание библиотеки:
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

]
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
