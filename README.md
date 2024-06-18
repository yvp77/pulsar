# Pulsar-16M
Скрипт для опроса УСПД Пульсар-16M через USB-RS485 <br>

git clone https://github.com/yvp77/pulsar.git


# Сканер
Сканер адресов

Подготовка:<br>
pip install modbus_crc<br>
pip install argparse<br>
pip install pyserial<br>
pip install struct<br>

Запуск linux:<br>
./pulsar_scan.py /dev/ttyUSB0 9600 65000 65100<br>
<br>
Запуск в Windows:<br>
./pulsar_scan.py COM5 9600 65000 65100<br>

Возможные параметры запуска:<br>
./pulsar_scan.py <КОМ_ПОРТ> <СКОРОСТЬ><br>
./pulsar_scan.py <КОМ_ПОРТ> <СКОРОСТЬ> <НАЧ_НОМЕР_ПРИБОРА> <ПОСЛЕДНИЙ_НОМЕР_ПРИБОРА> <br>
./pulsar_scan.py /dev/ttyUSB0 9600 65000 65100


# Опрос

Подготовка:<br>
pip install modbus_crc<br>
pip install argparse<br>
pip install pyserial<br>
pip install struct<br>
pip install re<br>
pip install json<br>

Скрипт запускается с параметрами:<br>
./pulsar_m.py <КОМ_ПОРТ> <СКОРОСТЬ> <АДРЕС> <ФОРМАТ><br>

<КОМ_ПОРТ> /dev/ttyUSB0 или для Windows COM1<br>
<СКОРОСТЬ> стандартные скорости портов, по умолчанию 9600<br>
<АДРЕС> адрес УСПД по умолчанию - 0, адрес указывается на корпусе УСПД
<ФОРМАТ> в каком формате выдавать данные csv или json, по умолчанию json<br>

Запуск linux:

./pulsar_m.py /dev/ttyUSB0 9600 65000<br>
./pulsar_m.py /dev/ttyUSB0 9600 65000 csv<br>
./pulsar_m.py /dev/ttyUSB0 9600 65000 json<br>


Запуск в Windows:

./pulsar_m.py COM1 9600 65000<br>
./pulsar_m.py COM1 9600 65000 csv<br>
./pulsar_m.py COM1 9600 65000 json<br>

