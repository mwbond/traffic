# Matthew Bond
# Mar 25, 2010
# main.py

import car
import intersection
import lane
import stream

max_accel = 2
vel = 0
desired_vel =  20
length = 6.5
prt = 2/3.0
max_brake = -3
obs_brake = -3.5

lane0 = lane.Lane(1000, 0)
lane1 = lane.Lane(1600, lane0)

add_car(stream_id, max_accel, vel, desired_vel, length, prt, max_brake,
		obs_brake)
lane1.add_car(car.Car(0, 2, 0, 20, 6.5, 2/3.0, -3, -3.5))
for step in range(1,300):
	if lane1.car_queue[0].offset > 6.5:
		lane1.add_car(car.Car(step, 2, 0, 29, 6.5, 2/3.0, -3, -3.5))
	print "*****STEP", step, "*****"
	lane0.print_lane()
	lane1.print_lane()
	print
	lane1.update_lane()
	lane0.update_lane()

	lane0.check_offsets()
