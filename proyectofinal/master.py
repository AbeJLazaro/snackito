import os
import threading

def run_script(script_name):
	os.system(f'python {script_name}.py') 

if __name__ =="__main__":
	# creating thread
	t1 = threading.Thread(target=run_script, args=("app",))
	t2 = threading.Thread(target=run_script, args=("bot",))
	t3 = threading.Thread(target=run_script, args=("variables",))

	# starting thread 1
	t1.start()
	# starting thread 2
	t2.start()
	# starting thread 3
	t3.start()

	# wait until thread 1 is completely executed
	#t1.join()
	# wait until thread 2 is completely executed
	#t2.join()
	# wait until thread 2 is completely executed
	#t3.join()
