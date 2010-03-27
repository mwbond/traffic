# Matthew Bond
# Mar 25, 2010
# main.py

import car
import lane

lane = lane.Lane(1600)

lane.add_car(car.Car(0, 2, 0, 20, 6.5, 2/3.0, -3, -3.5))
for step in range(1,200):
	if lane._car_queue[0].offset > 6.5:
		lane.add_car(car.Car(step, 2, 0, 29, 6.5, 2/3.0, -3, -3.5))
	print "*****STEP", step, "*****"
	lane.print_lane()
	print
	lane.update_lane()
