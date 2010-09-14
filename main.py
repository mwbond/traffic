# Matthew Bond
# Mar 25, 2010
# main.py

import car
import lane

lanel = lane.Lane(1000, None, None, None, None)
laner = lane.Lane(1000, None, None, None, lanel)
lanel.elane = laner

laner.add_car(car.Car(0, 2, 0, 20, 6.5, 2/3.0, -3, -3.5))
for step in range(1, 100):
	if laner.car_queue[0].offset > 6.5:
		laner.add_car(car.Car(step, 2, 0, 29, 6.5, 2/3.0, -3, -3.5))
	print "*****STEP", step, "*****"
	laner.print_lane()
	lanel.print_lane()
	print
	# laner.update_lane()
	# lanel.update_lane()
	master = []
	for lane in [lanel, laner]:
		for car in lane.car_queue:
			master.append([car.offset, lane, car])
	master.sort()
	for (offset, lane, car) in master:
		lane.update_lane(car)

	laner.check_offsets()
	lanel.check_offsets()
