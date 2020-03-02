
import serial
#import ev3dev.ev3 as ev3
import time

class Arduino:

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0',9600, serial.EIGHTBITS, serial.PARITY_NONE, serial.STOPBITS_ONE)
        #self.motor = ev3.LargeMotor('outA')
        # self.discover()

    def discover(self):
        # [cell number, command, data1, data2]
        # Command 0: Cell Discovery
        #self.ser.write(bytearray([255,0,0,1]), )
        self.ser.write(b'acaa')
        #time.sleep(5.0)
        ack=self.ser.read(4) #TODO: Check ack
        discovery_result = self.ser.read(4)
        print(discovery_result)
        return discovery_result[3] - 96

    def convert_to_base(self,angle):
        if angle <= 255:
            return [0,angle]
        else:
            return [int(angle/256), angle % 256]

    def run_to_rel_pos(self, rel_angle, cell_index):
        if rel_angle >= 0:
            #self.motor.run_to_rel_pos(position_sp = rel_angle, speed_sp = 250, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 150)
            self.ser.write(bytearray([96+cell_index,102]+self.convert_to_base(rel_angle)))
        else:
            #self.motor.run_to_rel_pos(position_sp = rel_angle, speed_sp = 250, stop_action = 'hold', ramp_up_sp = 0, ramp_down_sp = 150)
             self.ser.write(bytearray([96+cell_index,103]+self.convert_to_base((-1)*rel_angle)))

        #self.motor.wait_until('holding')
        #time.sleep(0.4)