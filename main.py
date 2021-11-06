import re
import csv
import functions
import os
from classes import Port, Vlan

portList =[]
vlanList = []
#resultConfigName = 'test-sw01.txt'
#origin = '10.1.6.32.DES-3200-28'

#--- Ф-ция получения списка с метками ---
def dictSearch(dictList, value: str):
    listMatch = []
    for port in dictList:
        if port.service == value:
            listMatch.append(port.number)
    return listMatch


#--- Чтение файла шаблона в объект ----
with open('data/template.txt', 'r') as file:
    filedata = file.read()

#--- Получение списков меток по типам скобок ---
portMarksList_dupl = re.findall(r'\[(.*?)\]', filedata)
switchMarksList_dupl = re.findall(r'(\{.*?\})', filedata)
portMarksList = list(set(portMarksList_dupl))
switchMarksList = list(set(switchMarksList_dupl))

#--- Обработка меток в {} ---

for i in switchMarksList:
    filedata = filedata.replace(i, input('Введите данные для ' + i + ': '))


origin = input('Введите имя исходного конфига в папке data(с указанием расширения файла): ')
resultConfigName = input('Имя генерируемого конфига (с указанием расширения файла): ')

#--- Вызов функции получения данных из файла конфигурации ---
functions.prepare(origin)

#--- Получение данных из ports.csv ---
os.startfile(r'data\ports.csv')
input('\nЗаполните столбец ServiceType (l2, l3, trunk)'
      '\nПри необходимости можно добавить в список новые порты'
      '\nДля сохранения изменений используйте CTRL+S, от сохранения при закрытии откажитесь'
      '\nНажмите Enter для продолжения... ')
with open('data/ports.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        portList.append(Port(row['Port'], row['Description'], row['ServiceType']))

#--- Обработка меток в [] ---
for i in portMarksList:
    marksList_splitted = i.split(' ')
    matchedPorts = []
    for j in marksList_splitted:
        matchedPorts.extend(dictSearch(portList, j))
        matchedPorts = [str(k) for k in matchedPorts]
    filedata = filedata.replace('[' + i + ']', ",".join(matchedPorts))
    
#--- Обработка метки <ports> ---1
configPorts = []
for i in portList:
    configPorts.append(i.create_port())
filedata = filedata.replace('<ports>', "".join(configPorts))


#--- Получение данных из vlans.csv ---
os.startfile(r'data\vlans.csv')
input('\nПроверьте и при необходимости отредактируйте таблицу vlans'
      '\nДля сохранения изменений используйте CTRL+S, от сохранения при закрытии нужно отказаться'
      '\nНажмите Enter для продолжения... ')
with open('data/vlans.csv', 'r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        vlanList.append(Vlan(row['VlanName'], row['VlanID'], row['untag'], row['tag']))
    
#--- Обработка метки <vlans> ---
configVlans = []
for i in vlanList:
    configVlans.append(i.create_vlan())
filedata = filedata.replace('<vlans>', "".join(configVlans))
    
#--- Сохранение всех результатов в новый файл ---
with open('data/' + resultConfigName, 'w') as file:
    file.write(filedata)

os.startfile(r'data\\' + resultConfigName)
input()
