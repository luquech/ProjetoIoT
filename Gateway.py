import serial
import firebase_admin
from firebase_admin import credentials, db
import time
import bluetooth

# Configuração do Firebase
cred = credentials.Certificate("/home/lucas/Downloads/projetoiot-6f20f-firebase-adminsdk-zwnv8-d892e9e87c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projetoiot-6f20f-default-rtdb.firebaseio.com/'
})

# Configuração da porta serial Bluetooth para o segundo ESP32
bluetooth_device_name = "Nome_do_Dispositivo"  # Substitua pelo nome do seu dispositivo Bluetooth
baud_rate_control = 9600

def discover_device_address(device_name):
    devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name, _ in devices:
        if name == device_name:
            return addr

# Função para enviar comandos para o segundo ESP32 com base na variável do Firebase
def control_lights(value):
    bluetooth_address_control = discover_device_address(bluetooth_device_name)
    ser_control = serial.Serial(bluetooth_address_control, baud_rate_control)
    ser_control.write(value.encode())
    ser_control.close()

# Função para ler a variável do Firebase e enviar para o segundo ESP32
def read_and_send():
    while True:
        luz_state = db.reference("luz").get()
        print("Luz State:", luz_state)

        # Enviar o estado da luz para o segundo ESP32
        control_lights("LOW" if luz_state else "HIGH")

        time.sleep(10)  # Ajuste o intervalo conforme necessário

try:
    read_and_send()

except KeyboardInterrupt:
    print("Programa encerrado.")
