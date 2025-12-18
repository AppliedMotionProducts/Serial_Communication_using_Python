import serial, time


# Initialization parameters. Note the serial port and baud rate of your project
# may vary. Our default baud rate is 9600
def motor_init():
    ser=serial.Serial()
    ser.port = "COM6"
    ser.baudrate = 9600
    ser.bytesize = serial.EIGHTBITS
    ser.parity = serial.PARITY_NONE
    ser.stopbits = serial.STOPBITS_ONE
    ser.timeout= .1
    ser.xonxoff = False
    ser.rtscts = False
    ser.dsrdtr = False
    ser.writeTimeout = 0
    return ser

# When we send a serial command, the program will check and print
# the response given by the drive.
def send(ser,command):
        ser.write((command+'\r').encode())
        response = ser.read(15).decode()
        if len(response) > 0:
            print (response)
            ser.flushInput()

def motor_setup(ser):
        """
        Setup initial motor parameters, also resets alarm
        """
        send(ser,'EG20000') # Sets microstepping to 20,000 steps per revolution
        send(ser,'IFD') # Sets the format of drive responses to decimal
        send(ser,'SP0') # Sets the starting position at 0
        send(ser,'AR') # Alarm reset
        send(ser,'AC10') # Acceleration 
        send(ser,'DE15') # Deceleration
        send(ser,'VE10') # Velocity 
        send(ser,'ME')  # Enable Motor
        
def move(ser):
        send(ser,'FL60000') # Moves 3 revs CW
        send(ser,'FL-120000') #Moves 6 revs CCW
        """
        This section demonstrates the drives ability to poll immediate position
        and check status to see if the move is done.
        """
        time.sleep(.5)
        send(ser, 'IP') # IP is immediate position
        time.sleep(1.2)
        send(ser,'IP')
        time.sleep(1)
        send(ser,'RS') # We end by requesting the status of the drive.

try:
    ser = motor_init() # Initialise the serial port
    ser.open()         # open the serial port
    time.sleep(1)
except Exception as e:
    print ('error opening serial port')
    exit()

if ser.isOpen():
    try:
        ser.flushInput()
        ser.flushOutput()
        motor_setup(ser)  # Complete motor setup and enable motor
        move(ser)         # perform the move command
        
    except Exception as e1:
        print ("Error Communicating...: " + str(e1))
else:
    print ("Cannot open serial port ")
