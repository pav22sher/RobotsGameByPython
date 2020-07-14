import socket
import json

class Robot(object):#класс-робот
	def __init__(self):#конструктор
		self.health = 15#здоровье
		self.energy = 25#энергия
		self.defence=False#защита:True-вкл.защиту;False-выкл.защиту
	def attack(self,obj):#атака
		self.defence=False#т.к. защита действует один ход
		self.energy = self.energy-5#атака стоит 5 единиц энергии
		if not obj.defence: obj.health=obj.health-5#если у второго робота выкл.защита
	def defend(self):#защита
		self.defence=True#вкл.защиту
		self.energy = self.energy-5#защита стоит 5 единиц энергии
	def restore(self):#восстановить энергию
		self.defence=False#т.к. защита действует один ход
		self.energy = 25#восстановить энергию до начального уровня

#обработка использования игроками способности робота
def make_action(action,rob1,rob2):
	if action=="1":#атака другова робота
		if rob1.energy>=5:#атака стоит 5 единиц энергии
			rob1.attack(rob2)
		else: return False#если не хватает энергии
	elif action=="2":#защита от атаки другова робота
		if rob1.energy>=5:#защита стоит 5 единиц энергии
			rob1.defend()
		else: return False#если не хватает энергии
	elif action=="3":#восстановить энергию до начального уровня
		rob1.restore()#восстановить энергию стоит 0 единиц энергии
	return True#если хватает энергии

#SERVER = "127.0.0.1" #(localhost в диапазоне 127.0.0.1 — 127.255.255.255)
#PORT = 8080 #системные (0—1023), пользовательские (1024—49151) и частные (49152—65535)

PORT=int(input("Введите номер порта(Например, 8080)>"))#Например, 8080

#JSON (англ. JavaScript Object Notation)
#json.dumps-сериализует объект Python в строку JSON-формата.
#json.loads-десериализует строку JSON-формата в объект Python.
#Сериализация — процесс перевода объекта Python
#в последовательность(серию) битов(байтов).

#string.encode('<название кодировки>') # переводим строку в байтовую строку
#b'<байт-строка>'.decode('<название кодировки>') # переводим байтовую строку в строку

try:
	#Метод socket создает сокет
	#Оператор with используется для автоматического закрытия сокета в конце блока.
	#domain указывающий семейство протоколов сокета: AF_INET для сетевого протокола IPv4
	#type SOCK_STREAM (надёжная потокоориентированная служба или потоковый сокет(TCP))
	#protocol=0 (протокол не указан) используется значение по умолчанию для данного вида соединений.
	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	#Метод bind свяжет сокет с хостом(IP-адресом) и портом 
	#Если указать "127.0.0.1", то подключиться можно будет только с этого же компьютера.
	#Если не указать хост или указать "0.0.0.0", сокет будет прослушивать все хосты
	server.bind(("", PORT))
	#Метод listen запускает режим прослушивания для сокета. 
	#Метод принимает один аргумент — максимальное количество подключений 
	server.listen(2)
	#Метод accept примет подключение и вернет сокет и адрес клиента
	print ("Ожидаем подключения игроков...")
	conn1, adr1 = server.accept()
	print ("Первый игрок подключился...")
	conn2, adr2 = server.accept()
	print ("Второй игрок подключился...")
	#создаем роботов для каждого игрока
	robot1=Robot()#для 1 игрока 
	robot2=Robot()#для 2 игрока
	win_num=0#номер игрока, который победил
	while True:#бесконечный цыкл(выход по break)
		#Метод recv получает данные.Тип возвращаемых данных — bytes.
		#Метод принимает один аргумент — количество байт для чтения
		#Метод send отправляет данные. Принимает он bytes.
		conn1.send(json.dumps("Ваш ход...").encode())#говорим 1 игроку, что его ход
		json.loads(conn1.recv(1024).decode())#1 игрок отвечает окей
		#говорим 1 игроку сколько у его робота здоровья и энергии
		conn1.send(json.dumps("У вас здоровье="+str(robot1.health)+" и энергии="+str(robot1.energy)).encode())
		action = json.loads(conn1.recv(1024).decode())#1 игрок говорит, какую способность робота применить 
		while not make_action(action,robot1,robot2):#пока он не скажет способность, на которую у него хватит энергии
			conn1.send(json.dumps("Ошибка").encode())#говорим 1 игроку, что у него не хватает энергии 
			action = json.loads(conn1.recv(1024).decode())#1 игрок опять говорит, какую способность робота применить 
		conn1.send(json.dumps("Окей").encode())#если 1 игрок сказал способность, на которую у него хватает энергии
		if robot2.health<=0:#если у робта 2 игрока закончилось здоровье, то мы победили
			win_num=1#номер игрока, который победил-1
			break#выходим из игры
		#тоже самое для 2 игрока	
		conn2.send(json.dumps("Ваш ход...").encode())
		json.loads(conn2.recv(1024).decode())
		conn2.send(json.dumps("У вас здоровье="+str(robot2.health)+" и энергии="+str(robot2.energy)).encode())
		action = json.loads(conn2.recv(1024).decode())
		while not make_action(action,robot2,robot1):
			conn2.send(json.dumps("Ошибка").encode())
			action = json.loads(conn2.recv(1024).decode())
		conn2.send(json.dumps("Окей").encode())
		if robot1.health<=0:
			win_num=2
			break
	
	#посылаем игрокам результаты игры
	msg="Результат игры: "
	if win_num==1:
		conn1.send(json.dumps(msg+"Вы победили!").encode())
		conn2.send(json.dumps(msg+"Вы проиграли!").encode())
	elif win_num==2:
		conn1.send(json.dumps(msg+"Вы проиграли!").encode())
		conn2.send(json.dumps(msg+"Вы победили!").encode())
	#Метод close закрывает сокет.
	conn1.close()
	conn2.close()

except BaseException:#ловим все возможные ошибки программы
	print("Ошибка!!!")