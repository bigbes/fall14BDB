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


# Тестирующая система

Для использование необходимо поставить PyYAML:

* `pip install pyyaml`
* `sudo apt-get install python-yaml` # на Ubuntu/Debian


Она состоит из двух файлов:

* `test/gen_workload.py`
* `test/runner.py`


## test/gen_workload.py

Первый из них отвечает за создание файлов для тестирования, а второй за запуск их на вашем хранилище.

### Конфигурационный файл

В первый файл вы можете передать конфигурационный файл, например:

```
---
get: 20
put: 80
shuffle: True
distrib: "uniform"
ops: 10000
...
```


* get + put = 100 - процентное отношение обеих операций (int)
* shuffle, отвечает за то, чтобы операции put/get были перемешаны (иначе, сначала будут идти все put, а затем все get) (True/False)
* distrib - тип распределения ("uniform"/"latest"/"oldest"/"none")
* ops - итоговое кол-во операций (int)


### Аргументы командной строки

Передавать конфигурационный файл можно с помощью `--config`
Указывать имя файла нагрузки можно с помощью `--output`

### Пример

Находясь в папке example:
```
> python ../test/gen_workload.py --output workload
--------------------------------------------------------------------------------
Workload successfully generated
Output: /home/bigbes/src/hw1/example/workload.in
--------------------------------------------------------------------------------
> python ../test/gen_workload.py --output workload --config example.schema.yml
--------------------------------------------------------------------------------
Workload successfully generated
Output: /home/bigbes/src/hw1/example/workload.in
Config: /home/bigbes/src/hw1/example/example.schema.yml
--------------------------------------------------------------------------------
```

## test/runner.py

Для запуска `*.in` файла используется test/runner.py. На вход ему подается путь к вашей библиотеке(--so) и файл для тестирования (--workload).  
В случае если подается флаг `--new`, то создается `*.out` файл, в котором находятся все значения, которые вернула ваша БД. Иначе он будет сравнивать с `*.out` файлом.  
В случае успеха сравнения скрипт вернет "Result is OK", в случае неравенства вернется "Result is not OK" и будет создан файл '*.out.bad', в котором будет лежать те значения, которые вернуло ваше хранилище.  

### Пример

Находясь в папке example:
```
> python ../test/gen_workload.py --output workload
--------------------------------------------------------------------------------
Workload successfully generated
Output: /home/bigbes/src/hw1/example/workload.in
--------------------------------------------------------------------------------
> python ../test/runner.py --new --workload workload.in --so ./libdbsophia.so
================================================================================
Library: /home/bigbes/src/hw1/example/./libdbsophia.so
Workload output successfully generated
Output: /home/bigbes/src/hw1/example/workload.out
================================================================================
> python ../test/runner.py --workload workload.in --so ./libdbsophia.so
================================================================================
Library: /home/bigbes/src/hw1/example/./libdbsophia.so
Test with workload '/home/bigbes/src/hw1/example/workload.in'
Result is OK
================================================================================
> echo "1" >> workload.out
> python ../test/runner.py --workload workload.in --so ./libdbsophia.so
================================================================================
Library: /home/bigbes/src/hw1/example/./libdbsophia.so
Test with workload '/home/bigbes/src/hw1/example/workload.in'
Result is not OK
================================================================================
```

### Ограничения

Для того, чтобы ваша библиотека смогла загрузиться нужны следующие глобальные методы:
```
struct DB *dbcreate(const char *path, const struct DBC conf);

int db_close(struct DB *db);
int db_del(const struct DB *, void *, size_t);
int db_get(const struct DB *, void *, size_t, void **, size_t *);
int db_put(const struct DB *, void *, size_t, void * , size_t  );
```

Данная библиотека (`test/lib/database.py`) использует модуль ctypes, для загрузки DLL и импорта функций из неё.
