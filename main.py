# Matthew Bond
# Mar 25, 2010
# main.py

import car
import lane

lanel = lane.Lane(10000)
laner = lane.Lane(10000, w_lane=lanel)
lanel.e_lane = laner

laner.add_car(car.Car(0, 2, 0, 15, 6.5, 2/3.0, -3, -3.5))
lanel.add_car(car.Car(1, 2, 0, 23, 6.5, 2/3.0, -3, -3.5))
for step in range(1, 100):
	if laner.car_queue[0].offset > 6.5:
		laner.add_car(car.Car(step, 2, 0, 29, 6.5, 2/3.0, -3, -3.5))
	print "*****STEP", step, "*****"
	laner.print_lane()
	lanel.print_lane()
	print
	############################################
	lane_info = [[laner.get_index_offset(), laner],
				 [lanel.get_index_offset(), lanel]]
	lane_info.sort(reverse=True)
	while lane_info[0][0] is not None:
		lane_info[0][1].update_lane()
		lane_info[0][0] = lane_info[0][1].get_index_offset()
		lane_info.sort(reverse=True)
	############################################

	laner.check_offsets()
	lanel.check_offsets()
