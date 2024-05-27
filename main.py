import socket
import struct
import tkinter as tk
import serial

################### SERVER CONFIG ###################
# (change only if running the simuation in a external machine)
localIP = "127.0.0.1"
localPort = 30001
bufferSize = 1024
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
try:
    UDPServerSocket.bind((localIP, localPort))
    UDPServerSocket.settimeout(0.1)
except:
    print("Error trying to connect to the UDP server!")
else:
    print("Connected to the UDP server!")
#####################################################


################ DATA CONTROL ################
enable_rpm = True
enable_gear = True
enable_velocimetro = False
enable_posX = False
enable_Yaw = False
enable_Pitch = False
enable_Roll = False
enable_SerialWrite = True

enable_GUI = True
data_output = {}
##############################################

################ SERIAL CONFIG ##################
serial_connected = False
serial_com = None
def setup_serial():
    try:
        global serial_com
        serial_com = serial.Serial()
        serial_com.port = port_data.get()
        serial_com.baudrate = 9600
        serial_com.timeout = .1
        serial_com.open()
        serial_com.write(bytes("TEST", 'utf-8'))
        serial_com.close()
        global serial_connected
        serial_connected = True
        port_button.configure(bg="green")
    except Exception as e:
        port_button.configure(bg="red")
        print("Error opening the serial connection!")
        print(e)
##############################################

################ GUI CONFIG ##################
window = tk.Tk()
simulation_status = False
window.title("GP BIKES DATA")
window.geometry('900x200')
status_label = tk.Label(window, text="GPBikes connection status: ", font=("Helvetica", 15, "bold"), pady=10)
status_label.grid(row=0, column=0)
status_label_status = tk.Label(window, text="Disconnected", font=("Helvetica", 15, "bold"), fg="red", pady=10)
status_label_status.grid(row=0, column=1)
port_label = tk.Label(window, text="Seria data PORT:", font=("Helvetica", 15, "bold"), pady=10)
port_label.grid(row=2, column=0)
port_data = tk.Entry(width=20, font=("Helvetica", 15, "bold"))
port_data.grid(row=2, column=1)
port_button = tk.Button(text="Connect", font=("Helvetica", 15, "bold"), command=setup_serial)
port_button.grid(row=2, column=2)
#feel free to add you desired data!
##############################################


while (True):  # main loop server
    try:
        receivedData = UDPServerSocket.recvfrom(bufferSize)
        bytesAddressPair = receivedData[0]
        client_status = receivedData[1]
        simulation_status = True

        if (len(bytesAddressPair) > 20):
            if enable_rpm:
                rpm = bytesAddressPair[13].to_bytes(1, 'little') + bytesAddressPair[14].to_bytes(1, 'little') + \
                      bytesAddressPair[15].to_bytes(1, 'little') + bytesAddressPair[16].to_bytes(1, 'little')
                rpm = struct.unpack('i', rpm)
                rpm = rpm[0]
                data_output["rpm"] = rpm

            if enable_gear:
                gear = bytesAddressPair[25].to_bytes(1, 'little') + bytesAddressPair[26].to_bytes(1, 'little') + \
                       bytesAddressPair[27].to_bytes(1, 'little') + bytesAddressPair[28].to_bytes(1, 'little')
                gear = struct.unpack('i', gear)
                gear = gear[0]
                data_output["gear"] = gear

            if enable_velocimetro:
                velocimetro = bytesAddressPair[33].to_bytes(1, 'little') + bytesAddressPair[34].to_bytes(1, 'little') + \
                              bytesAddressPair[35].to_bytes(1, 'little') + bytesAddressPair[36].to_bytes(1, 'little')
                velocimetro = struct.unpack('f', velocimetro)
                velocimetro = float(velocimetro[0]) * 3.6
                data_output["velocimetro"] = velocimetro

            if enable_posX:
                posX = bytesAddressPair[37].to_bytes(1, 'little') + bytesAddressPair[38].to_bytes(1, 'little') + \
                       bytesAddressPair[39].to_bytes(1, 'little') + bytesAddressPair[40].to_bytes(1, 'little')
                posX = struct.unpack('f', posX)
                posX = posX[0]
                data_output["posX"] = posX

            if enable_Yaw:
                yaw = bytesAddressPair[109].to_bytes(1, 'little') + bytesAddressPair[110].to_bytes(1, 'little') + \
                      bytesAddressPair[111].to_bytes(1, 'little') + bytesAddressPair[112].to_bytes(1, 'little')
                yaw = struct.unpack('f', yaw)
                yaw = yaw[0]
                data_output["yaw"] = yaw

            if enable_Pitch:
                pitch = bytesAddressPair[113].to_bytes(1, 'little') + bytesAddressPair[114].to_bytes(1, 'little') + \
                        bytesAddressPair[115].to_bytes(1, 'little') + bytesAddressPair[116].to_bytes(1, 'little')
                pitch = struct.unpack('f', pitch)
                pitch = pitch[0]
                data_output["pitch"] = pitch

            if enable_Roll:
                roll = bytesAddressPair[117].to_bytes(1, 'little') + bytesAddressPair[118].to_bytes(1, 'little') + \
                       bytesAddressPair[119].to_bytes(1, 'little') + bytesAddressPair[120].to_bytes(1, 'little')
                roll = struct.unpack('f', roll)
                roll = roll[0]
                data_output["roll"] = roll

            if enable_SerialWrite and serial_connected:
                data_RPM_fix = str(data_output['rpm'])
                while (len(data_RPM_fix) < 5):
                    data_RPM_fix = '0' + data_RPM_fix

                # The datagram is hardcoded in this part as a example
                # if you intend to change which data types are sent regularly
                # is advised to use a automated datagram constructor based on the
                # data_output keys, but try to follow the default datagram format
                data_out = "DATA,RPM=" + data_RPM_fix + ",GEAR=" + str(data_output['gear']) + '\n'
                serial_com.open()
                serial_com.write(bytes(data_out, 'utf-8'))
                serial_com.close()

    except:
        simulation_status = False

    if enable_GUI:
        # here you can Update you own GUI elements
        if simulation_status:
            if (len(bytesAddressPair) > 20):
                status_label_status.config(text="Connected", fg="green")
            else:
                status_label_status.config(text="Connected (simulation stopped)", fg="orange")
        else:
            status_label_status.config(text="Disconnected", fg="red")
        window.update()
