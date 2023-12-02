import firebase_admin
from firebase_admin import credentials, db
import time
import bluetooth

# Configuração do Firebase
cred = credentials.Certificate("/home/lucas/Downloads/projetoiot-6f20f-firebase-adminsdk-zwnv8-d892e9e87c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projetoiot-6f20f-default-rtdb.firebaseio.com/'
})

# Configuração do dispositivo Bluetooth
bluetooth_device_name = "ESP32_DESESPERO"  # Substitua pelo nome do seu dispositivo Bluetooth

def discover_device_address(device_name):
    devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in devices:
        if name == device_name:
            return addr

    raise ValueError(f"Device with name '{device_name}' not found.")

# Descubra o endereço Bluetooth do dispositivo
bluetooth_address_control = discover_device_address(bluetooth_device_name)

# Escolha o canal RFCOMM desejado (você pode ajustar conforme necessário)
bluetooth_channel_control = 1

# Configuração do socket Bluetooth
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bluetooth_address_control, bluetooth_channel_control))

def control_lights(value):
    sock.send(value.encode())

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
finally:
    sock.close()  # Certifique-se de fechar o socket ao finalizar o programa
