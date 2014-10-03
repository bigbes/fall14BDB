# Структура репозитория:

```
├── example                    - Папка с примером (с использованием библиотеки sophia)
│   ├── bdb_sphia.c            - Пример реализации
│   ├── bdb_sphia.h            - Копия mydb.h с небольшими изменениями
│   ├── example.schema.yml     - Пример файла для создания Workload'а
│   ├── Makefile               - Makefile для сборки проекта и примера тестирования
│   ├── README.rst
│   └── third_party
│       └── sophia             - Submodule с репозитоорием библиотеки sophia
├── Makefile                   - Базовый Makefile, сборка, создания тестовой нагрузки и.т.д.
├── mydb.c                     - Базовая реализация
├── mydb.h                     - Базовый хедер
├── README.md
└── test                       - Католог с тестовой системой
    ├── data                   - Каталог с данными для тестовой системы
    │   ├── keys.txt           - Ключи для ТС
    │   └── values.txt         - Значения для ТС
    ├── gen_workload.py        - Скрипт для генерации Workload'a
    ├── lib
    │   ├── database.py
    │   ├── __init__.py
    │   └── ordered_set.py
    ├── README.md
    └── runner.py              - Скрипт для Запуска Workload'а
```

Для того, чтобы собрать `example` нужно скачать репозиторий с помощью
`git clone git://github.com/bigbes/fall14BDB.git --recursive`
или в уже скачанном репозитории сделать `git submodule update --init`
