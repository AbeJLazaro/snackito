import telepot
import variables
from time import sleep

chat_id_global = False

# mapeo de comandos
comandos = {
	"hola" : "Hola! Este es el canal de telegram de Snackito",
	"nivel": "El comedero esta al {}% de su capacidad total",
	"alimentar": "Se arrojó una porción de alimento! {}",
	"instrucciones": """A continuación te muestro los comandos que puedes utilizar:
		* nivel: Muestra el nivel de comida del alimentador
		* alimentar: Libera una porción de comida
	""",
}

def set_chat_id(chat_id):
	global chat_id_global
	with open("files/chat_id.txt","w") as file:
		file.write(str(chat_id))
	chat_id_global = True

# handler de telegram
def handle(msg):

	# Datos importantes para manejo de comandos
	chat_id = msg['chat']['id']
	command = msg['text'].lower()

	if not chat_id_global:
		set_chat_id(chat_id)

	print('Comando recibido: %s' % command)
	
	if command == "hola":
		bot.sendMessage(chat_id, comandos[command])
	elif command == "nivel":
		bot.sendMessage(chat_id, comandos[command].format(variables.get_porcentaje_alimento()))
	elif command == "alimentar":
		bot.sendMessage(chat_id, comandos[command].format(variables.alimentar()))
	else:
		bot.sendMessage(chat_id, comandos["instrucciones"])

# Conexión a telegram
bot = telepot.Bot('5915592221:AAEYqmzN4jRcsGoew19re9uiO_gMJ8Yibrk')
bot.message_loop(handle)

while 1:
	sleep(10)