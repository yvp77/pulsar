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
#
# Скрипт для сканирования и поиска адресов Пульсар М
# запуск ./pulsar_scan.py /dev/ttyUSB0 <скорость_порта> <первый_номер_кв> <последний_номер_кв>
# <скорость_порта> - 9600,19200, и т.д.
#
# Примеры linux:
# ./pulsar_scan.py /dev/ttyUSB0 9600 60000 60100
#
#
# Примеры Windows:
# ./pulsar_scan.py COM5 9600 60000 60100




import argparse
import serial
import struct
import time
import random
import re

from modbus_crc import add_crc

# Parse args
parser = argparse.ArgumentParser(
		description='Сканер адресов Пульсар 16М',
		formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('serial',  nargs='?', default='/dev/ttyUSB0', help='COM-порт. Пример linux: /dev/ttyUSB0 Пример Windows: COM1')
parser.add_argument('baudrate',  nargs='?', default='9600', help='Скрость COM порта')
parser.add_argument('num_top',  nargs='?', default='60000', help='Начальный номер Пульсара')
parser.add_argument('num_end',  nargs='?', default='64000', help='Последний номер Пульсара')
parser.add_argument('info',  nargs='?', default='info', help='Показать дополнительную информацию')
args = parser.parse_args()



addr_top = int(args.num_top,16)
addr_end = int(args.num_end,16)
addr_top = int(addr_top)
addr_end = int(addr_end)
info = str(args.info)

addr_hex_t = hex(int(addr_top)).split('x')[-1]
addr_hex_e = hex(int(addr_end)).split('x')[-1]

com = args.serial
baudrate=args.baudrate


print ('Диапазон сканирования: ',addr_hex_t,'-',addr_hex_e) if info=='info' else ''

# Открываем порт с параметрами
ser = serial.Serial(com, baudrate, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
print ('Подключение через',com,':', ser.isOpen()) if info=='info' else ''

size = (struct.calcsize('>LBBBH'))+2 # Вычисляем длину запакованного пакета
print ('Размер отправляемого пакета:', size, ' байт') if info=='info' else ''



for addr in range(addr_top, addr_end+1):

    #addr = ((8*int(i))+3)+4194304000    # Расчитываем адрес наладчик+ по номеру квартиры
    cmd1 = 3
    cmd2 = 2
    cmd3 = 70
    idp = 1
    chunk = struct.pack('>LBBBH',addr,cmd1,cmd2,cmd3,idp) # Формируем пакет для отправки в КОМ порт
    #print ('Отправляю пакет HEXResult:', ':'.join('{:02x}'.format(c) for c in chunk))
    signed_package = add_crc(chunk)     # Контрольная сумма CRC14 MODBUS
    time.sleep(0.05)
    ser.write(signed_package)           # Отправляем пакет в КОМ порт
    time.sleep(0.2)                    # Ждем
    out = ser.read_all()                # Читаем из порта

    if not out:
        type_p = (b'\x00\x00')
        type_p = struct.unpack('H',type_p)
# Параметры собщения подставляем в вывод для печати в той же строке
        message = '-------'
        param1 = '\r' # Конец строки без перевода на новую
        param2 = True

    elif out:
      type_p = ''.join('{:02x}'.format(c) for c in out[6:8])
      message = '<<<---НАЙДЕН!!!'
      param1 = '\r\n' # Конец строки с переходом на новую строку
      param2 = False
      type_p = struct.unpack('H',out[6:8])
      type_p = int(re.sub(r'[()]', '', re.sub(',','',str(type_p))))
      if type_p >= 355:
         type_p = 65536
         message = '>>>---помехи'
# Выводим сообщение с параметрами назначенными ранее, в засисимости от того найден номер или нет
    print ('Адрес:',hex(int(addr)).split('x')[-1],'Тип прибора:',type_p, message, end=param1, flush=param2)
print('')
print('Сканирование окончено!', end='\r\n', flush=False);

"""
int(re.sub(r'[()]', '', re.sub(',','',type_p)))
    type_p = ''.join('{:02x}'.format(c) for c in out[6:8])
    message = '<<<--НАЙДЕН!!!'
    param1 = '\r\n' # Конец строки с переходом на новую строку
    param2 = False

# Параметры сообщение и подставляем в вывод для перевода строки
    if not out:                          #Если sn пусто, то принудительно ставим в 0
     type_p = (b'\x00\x00')
     type_p = struct.unpack('H',type_p)
# Параметры собщения подставляем в вывод для печати в той же строке
     message = '-------'
     param1 = '\r' # Конец строки без перевода на новую
     param2 = True



# Выводим сообщение с параметрами назначенными ранее, в засисимости от того найден номер или нет
    print ('Адрес:',hex(int(addr)).split('x')[-1],'Тип прибора:',type_p, message, end=param1, flush=param2)


else:
       print()
       print('Сканирование окончено!', end='\r\n', flush=False);
       ser.close()
"""
