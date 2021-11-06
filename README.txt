1 запустить main
2 заполнить столбец SereviceType в ports.csv
3 ctrl+S --> Да
4 Закрыть --> Сохранить? --> Нет
5 Жмешь Enter в скрипте
6 Проверяешь 0.0.0.0 Должна поменяться строка

config traffic control [l3] broadcast enable multicast enable action shutdown
config traffic control 1 broadcast enable multicast enable action shutdown