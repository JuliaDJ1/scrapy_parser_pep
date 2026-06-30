# Автор

Вадим Гусейнов

# Асинхронный парсер PEP на Scrapy

Парсер документов PEP (Python Enhancement Proposals) с сайта peps.python.org, реализованный на фреймворке Scrapy.

## Возможности

Паук `pep` обходит таблицу всех PEP на главной странице, переходит на страницу каждого документа и собирает:

- номер PEP,
- название,
- статус (Active, Final, Draft, Withdrawn, Rejected, Superseded, Accepted, Deferred и т.д.).

По результатам парсинга формируются два CSV-файла в директории `results/`:

- **pep_<дата>.csv** — полный список PEP с тремя колонками: номер, название, статус. Сохраняется через встроенный механизм Feed Exports.
- **status_summary_<дата>.csv** — сводная таблица по статусам: сколько документов в каждом статусе и общее количество (строка `Total`). Формируется через `PepParsePipeline`.

## Технологии

- Python 3.12
- Scrapy 2.9
- Twisted 22.10
- lxml, parsel, itemadapter

## Установка

```bash
git clone https://github.com/JuliaDJ1/scrapy_parser_pep.git
cd scrapy_parser_pep
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
scrapy crawl pep
```

После завершения работы в папке `results/` появятся оба CSV-файла. Полный обход всех PEP занимает около 15 минут (есть вежливая задержка между запросами `DOWNLOAD_DELAY = 1`).

## Тесты

```bash
pytest
```

## Структура проекта
scrapy_parser_pep/
├── pep_parse/
│   ├── spiders/
│   │   ├── init.py
│   │   └── pep.py          # Паук: parse() собирает ссылки, parse_pep() парсит карточку PEP
│   ├── init.py
│   ├── items.py             # PepParseItem: number, name, status
│   ├── middlewares.py
│   ├── pipelines.py         # PepParsePipeline: подсчёт статусов и сохранение сводки
│   └── settings.py
├── tests/
├── results/                 # CSV-файлы с результатами парсинга
├── .flake8
├── .gitignore
├── pytest.ini
├── README.md
├── requirements.txt
└── scrapy.cfg
