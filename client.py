﻿import socket
import json
import os

#SERVER = "127.0.0.1" #(localhost в диапазоне 127.0.0.1 — 127.255.255.255)
#PORT = 8080 #системные (0—1023), пользовательские (1024—49151) и частные (49152—65535)

#вывод правил игры
def print_rule():
	print("ПРАВИЛА ИГРЫ:\n")
	print("Каждый игрок управляет роботом, который обладает\n"+
							"изначально здоровьем=15, энергией=25 и набором способностей:"+
							"\nатаковать(-5 энергии,-5 здоровья у противника (или -0 если он защищается));"+
							"\nзащищаться(-5 энергии,действует один ход(при атаке на вас вместо -5  будет -0 здоровья));"+
							"\nвосстановить энергию(-0 энергии,энергия становится равной 15).\n"+
							"Роботы могут по очереди использовать свои способности,\n"+
							"тратя на них энергию. Когда здоровье одного из роботов\n"+
							"перестанет быть положительным целыми числом, другой робот выигрывает.\n")

try:
	SERVER=input("Введите IP-адрес сервера(Например,localhost)>")
	PORT=int(input("Введите номер порта(Например,8080)>"))
	os.system("cls")#очищаем консоль
	print("Л/р№3 Вар№6")
	print_rule()
	var=input("Нажмите что-нибудь...\n")
	os.system("cls")

	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)#создаем сокет
	client.connect((SERVER, PORT))#конектимся к серверу
	
	try:
		while True:
			print("Ожидаем...")
			msg	= json.loads(client.recv(1024).decode())
			client.send(json.dumps("Окей").encode())
			print(msg)
			if msg!="Ваш ход...":#если пришла не эта строчка,
				break#то конец игры
			else:
				os.system("cls")
				info=json.loads(client.recv(1024).decode())#принимаем здоровье и энергию нашего робота
				print(info)#вывод здоровья и энергии нашего робота
				while True:
					select=input("Выберите:"+
					"\n1-атаковать;"+
					"\n2-защищаться;"+
					"\n3-восстановить энергию;"+
					"\n4-вывести правила игры:\n")
					while select!="1" and select!="2" and select!="3":#если пришла не способность робота
						os.system("cls")
						if select=="4":#хотим посомтреть правила игры (забыли их)
							print_rule()
							var=input("Нажмите что-нибудь...\n")
							os.system("cls")
						else:
							print("Ошибка!Нет такого варианта!Попробуйте еще раз!")
						print(info)#вывод здоровья и энергии нашего робота
						select=input("Выберите:"+
						"\n1-атаковать;"+
						"\n2-защищаться;"+
						"\n3-восстановить энергию;"+
						"\n4-вывести правила игры:\n")
					client.send(json.dumps(select).encode())#если пришла способность робота,то отправляем серверу 
					if json.loads(client.recv(1024).decode())=="Окей":#если у нас хватает энергии на способность
						break
					else:#если у нас не хватает энергии на способность
						os.system("cls")
						print("Ошибка!Не хватает энергии для данной способности!Попробуйте еще раз!")
						print(info)#вывод здоровья и энергии нашего робота
				
	except BaseException:#ловим все возможные исключения 
		print("Ошибка!!!")
	#закрывем сокет
	client.close()
	
except BaseException:#ловим все возможные исключения 
	print("Ошибка!!!")
