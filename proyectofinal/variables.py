import datetime
from bot_helper import enviar_mensaje
from time import sleep

# Variables control
porcentaje_alimento = "files/porcentaje_alimento.txt"
porcentaje_alimento_aux = None
tiempo_porcion = "files/tiempo_porcion.txt"
tamano_porcion = "files/tamano_porcion.txt"
chat_id = "files/chat_id.txt"
chat_id_ = None
last_drop = None
notification_time = datetime.datetime.now() - datetime.timedelta(minutes=30)

# getters y setters
def get_porcentaje_alimento():
	with open(porcentaje_alimento, "r") as file:
		data = file.readline()
	if data == "":
		print("LOG INFO: Problems with porcentaje_alimento.txt consistency")
		return 100
	return int(data)

def set_porcentaje_alimento(valor):
	with open(porcentaje_alimento, "w") as file:
		file.write(valor)

def get_tiempo_porcion():
	with open(tiempo_porcion, "r") as file:
		data = file.readline()
	return int(data)

def set_tiempo_porcion(valor):
	with open(tiempo_porcion, "w") as file:
		file.write(valor)

def get_tamano_porcion():
	with open(tamano_porcion, "r") as file:
		data = file.readline()
	return int(data)

def set_tamano_porcion(valor):
	with open(tamano_porcion, "w") as file:
		file.write(valor)

def get_last_drop():
	global last_drop
	try:
		with open("files/last_drop.txt", "r") as file:
			data = file.readline().split(" ")
			date = data[0].split("/")
			time = data[1].split(":")
			last_drop = datetime.datetime(
				int(date[2]), 
				int(date[1]), 
				int(date[0]), 
				int(time[0]), 
				int(time[1]),
				)
	except (FileNotFoundError, FileExistsError):
		print("LOG INFO: Error reading last_drop")

def set_last_drop():
	global last_drop
	last_drop = datetime.datetime.now()
	with open("files/last_drop.txt", "w") as file:
		file.write(datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))

def get_chat_id():
	global chat_id_
	try:
		with open("files/chat_id.txt", "r") as file:
			chat_id_ = file.readline()
	except (FileNotFoundError, FileExistsError):
		print("LOG INFO: Error reading chat_id")

def generate_time():
	return datetime.datetime.now().strftime("%H:%M del %Y/%m/%d")

# funciones control telegram
def alimentar():
	soltar_alimento()
	print("Se arroja una porción de comida")
	return ""

# funciones embebidas
def checar_nivel():
	global porcentaje_alimento_aux
	# realiar lectura con el sensor
	valor = 70
	if valor != porcentaje_alimento_aux:
		porcentaje_alimento_aux = valor 
		set_porcentaje_alimento(str(valor))

def soltar_alimento():
	valor = get_tamano_porcion()
	# mover el motor valor veces

# funciones control sistema
def alimento_programado():
	soltar_alimento()
	enviar_mensaje(chat_id_, f"Se ha arrojado una porción de alimento a las {generate_time()}")
	return True

def limite_bajo():
	global notification_time
	if notification_time + datetime.timedelta(minutes=10) <= datetime.datetime.now():
		enviar_mensaje(chat_id_, "El comedero cuenta con un nivel bajo de comida, se recomienda rellenar")
		notification_time = datetime.datetime.now()
	return True

def control_sistema():
	global porcentaje_alimento_aux

	if last_drop == None:
		print("LOG INFO: Gettin last_drop time")
		get_last_drop()

	if chat_id_ == None:
		print("LOG INFO: Getting chat_id for notification")
		get_chat_id()

	if porcentaje_alimento_aux == None:
		print("LOG INFO: Getting porcentaje_alimento")
		porcentaje_alimento_aux = get_porcentaje_alimento()
	
	checar_nivel()

	if int(get_porcentaje_alimento()) < 40:
		limite_bajo()
	
	intervalo = get_tiempo_porcion()
	if last_drop + datetime.timedelta(hours=intervalo) <= datetime.datetime.now():
		print("LOG INFO: Time to drop food")
		alimento_programado()
		set_last_drop()

if __name__ == "__main__":
	while 1:
		control_sistema()
		sleep(10)
else:
	print(__name__)