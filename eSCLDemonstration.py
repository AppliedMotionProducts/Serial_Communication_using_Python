
import socket, time

DriveIP = "10.10.10.10" #Drive IP can be configured

#header and end required for each eSCL message
header = bytes([0x00, 0x07])
end = bytes([0xD])

UDP_PORT = 7775

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Binding to your computer or external device running Python will vary.
sock.bind(('10.10.10.11', 7771)) #Match to your device

# This function encodes the message attaches header and adds carriage return to
# the end. It also recieves the drive response and prints it.
def command(Message):
    encodeMessage = Message.encode()
    toSend = header + encodeMessage + end
    sock.sendto(toSend,(DriveIP,UDP_PORT))
    recMessage = sock.recv(1024).decode()
    print(recMessage[2:])
    
# Drives should jog for 5 seconds in each direction        
command('DI1')    
time.sleep(.1)
command('JS1')
time.sleep(.1)
command('CJ')
time.sleep(5)
command('SJ')
time.sleep(.1)
command('DI-1')
time.sleep(.1)
command('CJ')
time.sleep(5)
command('SJ')
