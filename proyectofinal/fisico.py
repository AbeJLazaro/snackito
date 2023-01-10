import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
TRIG = 4
ECHO = 18
total_distance = 50 #CM
 
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

def leer_sensor():
	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)
	
	while GPIO.input(ECHO) == False:
		start = time.time()
	
	while GPIO.input(ECHO) == True:
		end = time.time()
	
	sig_time = end-start
	
	#CM:
	distance = sig_time / 0.000058
	
	GPIO.cleanup()

	porcentaje = (distance / 100) * total_distance

	return (round(porcentaje/10)*10)%100

def mover_motor(n):
	print(f"El motor se movio {n} veces")
