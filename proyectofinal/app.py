from flask import *
import datetime
import telepot
from time import sleep

# Variables globales para control 

# Aplicación principal servidor web
app = Flask(__name__)

# Variables control
porcentaje_alimento = 10




def generate_time():
	return datetime.datetime.now().strftime("%H:%M del %Y/%m/%d")

# funciones para telegram
def nivel_alimento():
	return porcentaje_alimento

def alimentar():
	print("Se arroja una porción de comida")
	return ""

def alimento_programado():
	return f"Se ha arrojado una porción de alimento a las {generate_time()}"

def limite_bajo():
	return "El comedero cuenta con un nivel bajo de comida, se recomienda rellenar"

# mapeo de comandos
comandos = {
	"hola" : "Hola! Este es el canal de telegram de Snackito",
	"nivel": f"El comedero esta al {nivel_alimento()}% de su capacidad total",
	"alimentar": f"Se arrojó una porción de alimento! {alimentar()}",
	"otro": """A continuación te muestro los comandos que puedes utilizar:
		nivel: Muestra el nivel de comida del alimentador
		alimentar: Libera una porción de comida
	""",
}

# handler de telegram
def handle(msg):
    global led, ser

    chat_id = msg['chat']['id']
    command = msg['text'].lower()

    print('Recibimos el comando: %s' % command)

    if command.lower() == 'hola':
        bot.sendMessage(chat_id, "De quien sos?")
    elif command.lower() == 'fecha':
        today = date.today()
        bot.sendMessage(chat_id, "Fecha: "+str(today))
    elif command.lower() == "led":
        led = not led
        #GPIO.output(7, led)
        bot.sendMessage(chat_id, "Led!")
    elif command.lower() == "saludos":
        for i in range(10):
            #GPIO.output(7, True)
            sleep(0.1)
            #GPIO.output(7, False)
            sleep(0.1)
        bot.sendMessage(chat_id, "Amigo o enemigo!?")
        #GPIO.output(7, led)
    elif command.lower() == "estado":
        estado = "prendido" if led else "apagado"
        bot.sendMessage(chat_id, f"Estado del led: {estado}")
    elif "uart" in command.lower():
        try:
            numero = command.lower().split(" ")[1]
        except:
            bot.sendMessage(chat_id, f"Comando incorrecto")
        else:
            #ser.write(numero.encode())
            bot.sendMessage(chat_id, f"Enviando {numero} por comunicación UART")   
    else:
        bot.sendMessage(chat_id, "bip bup bip")

# Conexión a telegram
bot = telepot.Bot('5941481334:AAFmz--azDwUmulHLZbAf6w4Zk6GiYBOLyc')

# Rutas del servidor web
@app.route('/',)
def home():
	data = {	
		"hora" 	: datetime.datetime.now().strftime("%H:%M"),
		"fecha" : datetime.datetime.now().strftime("%Y/%m/%d"),
		"porcentaje" : porcentaje_alimento,
	}
	return render_template('index.html', **data)

@app.route("/postmethod", methods=['POST'])
def view():
	print("*"*100)
	if "food_time" in request.form.keys():
		food_time = request.form['food_time']
		print(food_time)
	if "food_amount" in request.form.keys():
		food_amount = request.form['food_amount']
		print(food_amount)
	
	return render_template('index.html')

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
	bot.message_loop(handle)
	print('Bot de telegram levantado con exito')