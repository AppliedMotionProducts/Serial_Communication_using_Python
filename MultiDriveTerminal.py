"""
This program is designed as at terminal to send SCL commands to multiple drives
over Ethernet, you will need to adjust the program for your setup. Program is
written in Python 3.6
"""

import socket, time
"""
This section sets up some of our parameters including the ability to make
a table of IP addresses. To add more addresses simply add more values to the
drive list
"""
time.sleep(1)
#a0 = "10.10.10.19" #Your drive addresses may vary, make sure to correctly add
a1 = "10.10.10.10"
Drive_List = [a1]; #List is for 2 drives you may add more

# The header and carriage return are necessary and defined in our HCR
header = bytes([0x00, 0x07])
end = bytes([0xD])

UDP_PORT = 7775

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Binding to your computer or external device running Python will vary.
sock.bind(('10.10.10.11', 7771))

"""
I have included all steps into a single function due to the simplicity of the
program. For additional functionality or for organizational purposes you may
want to reorganize. Use instructions are found in the terminal prompt. Note
commands are not synchronized they are sent to each drive in succession.
"""
def command():
    command = input(">:")
    if command[0].isdigit():
        address = int(command[0])
        targetDrive = Drive_List[address]
        Message = command[1:]
        encodeMessage = Message.encode()
        toSend = header + encodeMessage + end
        sock.sendto(toSend,(targetDrive,UDP_PORT))
        recMessage = sock.recv(1024).decode()
        print(recMessage[2:])
   
    elif  command == 'esc':
        quit()
    
    else:
        i = 0 
        for val in Drive_List:
            Message = command
            encodeMessage = Message.encode()
            toSend = header + encodeMessage + end
            sock.sendto(toSend,(val,UDP_PORT))  
            recMessage = sock.recv(1024).decode()
            print('Drive ' + str(i)+ "  " + recMessage[2:])
            i=i+1
        

print("ATTENTION")
print("Enter Commands Below, commands with no leading address will be sent to all drives")
print("0RS will request status of drive at address zero, RS will request the status of all drives")
print('')
print("type esc to exit")

"""
The main loop. There is currently almost no additional functionality or error 
handling built in, it is just designed to show you the basics of sending UDP
packets to multiple ethernet drives.
"""
while True:
    command()
