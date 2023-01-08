from flask import *
import datetime
import variables

# Aplicación principal servidor web
app = Flask(__name__)

# Rutas del servidor web
@app.route('/',)
def home():
	data = {	
		"hora" 	: datetime.datetime.now().strftime("%H:%M"),
		"fecha" : datetime.datetime.now().strftime("%Y/%m/%d"),
		"porcentaje" : variables.get_porcentaje_alimento(),
	}
	return render_template('index.html', **data)

@app.route("/postmethod", methods=['POST'])
def view():
	print("*"*100)
	if "food_time" in request.form.keys():
		food_time = request.form['food_time']
		print("LOG INFO. Interval of food changed to: %s hours" % food_time)
		variables.set_tiempo_porcion(food_time)
	if "food_amount" in request.form.keys():
		food_amount = request.form['food_amount']
		print("LOG INFO. Amount of food changed to: %s portions" % food_amount)
		variables.set_tamano_porcion(food_amount)
	
	return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)