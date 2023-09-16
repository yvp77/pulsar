#!/usr/bin/python3
#-*- coding: utf-8 -*-

# Mercury_remote, allows you to remotely receive data from an electricity meter
#
# Для работы необходимо установить модули
#
# pip install modbus_crc
# pip install argparse
# pip install pyserial
# pip install struct
# pip install re
# pip install json
#
# Скрипт для удаленного снятия показаний со счетчиков Меркурий 200.2Т
# запуск ./Mercury200.py /dev/ttyUSB0 <скорость_порта> <адрес_счетчика>
# <скорость_порта> - 9600,19200, и т.д.
# <адрес_счетчика> последние 6 цифр серийного номера, или в формате Наладчик+ kv<NNN>, где <NNN> номер квартиры/дома
#
# Примеры linux:
# ./Mercury200.py /dev/ttyUSB0 9600 123321
# ./Mercury200.py /dev/ttyUSB0 9600 kv125
# ./Mercury200.py /dev/ttyUSB0 9600 kv125 csv
# ./Mercury200.py /dev/ttyUSB0 9600 kv125 json
#
#
#
# Примеры Windows:
# ./Mercury200.py COM1 9600 123321
# ./Mercury200.py COM1 9600 kv125
# ./Mercury200.py COM1 9600 kv125 csv
# ./Mercury200.py COM1 9600 kv125 json

#
#
# ______________________________________________________________________________________
# Если у Вас адреса защифрованны  ПО Наладчик+ то их можно посчитать по формуле либо вводить в формате наладчика, например: kv125
# Расчет:
# номер счетчика = ((8*N)+3)+4194304000
# где N - это номер квартиры иди номер дома(если СНТ)
# можно быстро посчитать в Exel
#
# ______________________________________________________________________________________


import argparse
import serial
import struct
import time
import datetime
import random
import re
import modbus_crc
import json

from modbus_crc import add_crc

# Parse args
parser = argparse.ArgumentParser(
		description='Опрос данных счетчика Меркурий 200.2',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('serial',  nargs='?', default='/dev/ttyUSB0', help='COM-порт. Пример linux: /dev/ttyUSB0 Пример Windows: COM1')
parser.add_argument('baudrate',  nargs='?', default='9600', help='Скрость COM порта')
parser.add_argument('dev_sn',  nargs='?', default='0', help='Серийный номер Пульсар-16М')
parser.add_argument('format',  nargs='?', default='csv', help='Формат вывода данных csv или json')
parser.add_argument('info',  nargs='?', default='noinfo', help='Показать дополнительную информацию')
args = parser.parse_args()


addr = int(args.dev_sn,16)
format = str(args.format)
info = str(args.info)

com = args.serial
baudrate=args.baudrate
addr = int(addr)
#insn = int(args.dev_sn)
addr_hex = hex(int(addr)).split('x')[-1]
print ('Cетевой адрес BCD:',addr_hex) if info=='info' or format=='info' else ''
# Открываем порт с параметрами
ser = serial.Serial(com, baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
print ('Подключение через',com,':', ser.isOpen()) if info=='info' or format=='info' else ''

# There are commands for get different data:
# Команда
# \x01 - HEX, 01 - DEC read data 
#
#
#
#
#
#
# Длина пакета
# \x0a - HEX, 10 - DEC 10 байт
# \x0c - HEX, 12 - DEC 12 байт
# \x0e - HEX, 14 - DEC 14 байт
# \x10 - HEX, 14 - DEC 16 байт
# \x12 - HEX, 18 - DEC 14 байт
#
# More information you can get there: http://www.incotexcom.ru/doc/M20x.rev2015.02.15.pdf
#chunk += b'\x27'



# Send data формирование и запрос серийного номера
cmd = 1
size = (struct.calcsize('>LBBLH'))+2 # Вычисляем длину запакованного пакета
print ('Размер отправляемого пакета:', size, ' байт') if info=='info' or format=='info' else ''
ch_all = 4294901760
id = random.randrange(65535) # случайное число для идентификатора запроса (любые 2 байта); 
chunk = struct.pack('>LBBLH',addr,cmd,size,ch_all,id)
print ('Отправляю пакет HEXResult:', ':'.join('{:02x}'.format(c) for c in chunk)) if info=='info' or format=='info' else ''

signed_package = add_crc(chunk)
ser.write(signed_package)
time.sleep(0.22)
out = ser.read_all()

print ('Результат HEXResult:', ':'.join('{:02x}'.format(c) for c in out)) if info=='info' or format=='info' else ''
#k1 = ''.join('{:02x}'.format(c) for c in out[6:14])
k1 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[6:14])))))) # Распаковывем с 6-14 байт обрезаем все лишнее и задаем формат два знака после запятой

#k2 = ''.join('{:02x}'.format(c) for c in out[14:22])
k2 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[14:22])))))) # Распаковывем с 14-22 байт обрезаем все лишнее и задаем формат два знака после запятой

#k3 = ''.join('{:02x}'.format(c) for c in out[22:30])
k3 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[22:30])))))) # Распаковывем с 22-30 байт обрезаем все лишнее и задаем формат два знака после запятой

#k4 = ''.join('{:02x}'.format(c) for c in out[30:38])
k4 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[30:38])))))) # Распаковывем с 30-38 байт обрезаем все лишнее и задаем формат два знака после запятой

#k5 = ''.join('{:02x}'.format(c) for c in out[38:46])
k5 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[38:46])))))) # Распаковывем с 38-46 байт обрезаем все лишнее и задаем формат два знака после запятой

#k6 = ''.join('{:02x}'.format(c) for c in out[46:54])
k6 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[46:54])))))) # Распаковывем с 46-54 байт обрезаем все лишнее и задаем формат два знака после запятой

#k7 = ''.join('{:02x}'.format(c) for c in out[54:62])
k7 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[54:62])))))) # Распаковывем с 54-62 байт обрезаем все лишнее и задаем формат два знака после запятой

#k8 = ''.join('{:02x}'.format(c) for c in out[62:70])
k8 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[62:70])))))) # Распаковывем с 62-70 байт обрезаем все лишнее и задаем формат два знака после запятой

#k9 = ''.join('{:02x}'.format(c) for c in out[70:78])
k9 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[70:78])))))) # Распаковывем с 70-78 байт обрезаем все лишнее и задаем формат два знака после запятой

#k10 = ''.join('{:02x}'.format(c) for c in out[78:86])
k10 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[78:86])))))) # Распаковывем с 78-86 байт обрезаем все лишнее и задаем формат два знака после запятой

#k11 = ''.join('{:02x}'.format(c) for c in out[86:94])
k11 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[86:94])))))) # Распаковывем с 86-94 байт обрезаем все лишнее и задаем формат два знака после запятой

#k12 = ''.join('{:02x}'.format(c) for c in out[94:102])
k12 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[94:102])))))) # Распаковывем с 94-102 байт обрезаем все лишнее и задаем формат два знака после запятой

#k13 = ''.join('{:02x}'.format(c) for c in out[102:110])
k13 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[102:110])))))) # Распаковывем с 102-110 байт обрезаем все лишнее и задаем формат два знака после запятой

#k14 = ''.join('{:02x}'.format(c) for c in out[110:118])
k14 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[110:118])))))) # Распаковывем с 110-118 байт обрезаем все лишнее и задаем формат два знака после запятой

#k15 = ''.join('{:02x}'.format(c) for c in out[118:126])
k15 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[118:126])))))) # Распаковывем с 118-126 байт обрезаем все лишнее и задаем формат два знака после запятой

#k16 = ''.join('{:02x}'.format(c) for c in out[126:134])
k16 = '{:.3f}'.format(float(re.sub(r'[()]', '', re.sub(',','',str(struct.unpack('d',out[126:134])))))) # Распаковывем с 126-134 байт обрезаем все лишнее и задаем формат два знака после запятой



if format == 'csv' or format=='info':

   print ('Номер','k1','k2','k3','k4','k5','k6','k7','k8','k9','k10','k11','k12','k13','k14','k15','k16',sep=';')
   # Формат чисел  print('{:.2f}'.format(2323.12345) обрезает до 2-х знаков после .
   print ('Pulsar',k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11,k12,k13,k14,k15,k16,sep=';')

else:

   print(json.dumps({"Pulsar": {addr_hex: {"data": {"sn": addr_hex,"k1":k1,"k2":k2,"k3":k3,"k4":k4,"k5":k5,"k6":k6,"k7":k7,"k8":k8,"k9":k9,"k10":k10,"k11":k11,"k12":k12,"k13":k13,"k14":k14,"k15":k15,"k16":k16}}}}))


