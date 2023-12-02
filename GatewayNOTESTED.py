import firebase_admin
from firebase_admin import credentials, db
import time
import bluetooth
import datetime

# Configuração do Firebase
cred = credentials.Certificate("/home/lucas/Downloads/projetoiot-6f20f-firebase-adminsdk-zwnv8-d892e9e87c.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://projetoiot-6f20f-default-rtdb.firebaseio.com/'
})

# Configuração do dispositivo Bluetooth (Gateway)
gateway_device_name = "ESP32_DESESPERO"  # Substitua pelo nome do seu dispositivo Bluetooth

def discover_device_address(device_name):
    devices = bluetooth.discover_devices(lookup_names=True)
    for addr, name in devices:
        if name == device_name:
            return addr

    raise ValueError(f"Device with name '{device_name}' not found.")

# Descubra o endereço Bluetooth do dispositivo Gateway
gateway_address = discover_device_address(gateway_device_name)

# Escolha o canal RFCOMM desejado (você pode ajustar conforme necessário)
gateway_channel = 1

# Configuração do socket Bluetooth para o Gateway
gateway_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
gateway_sock.connect((gateway_address, gateway_channel))

# Configuração do dispositivo Bluetooth (ESPLDR)
ldr_device_name = "ESPLDR"  # Substitua pelo nome do seu dispositivo Bluetooth

# Descubra o endereço Bluetooth do dispositivo ESPLDR
ldr_address = discover_device_address(ldr_device_name)

# Escolha o canal RFCOMM desejado para o ESPLDR
ldr_channel = 2

# Configuração do socket Bluetooth para o ESPLDR
ldr_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
ldr_sock.connect((ldr_address, ldr_channel))

def control_lights(value):
    gateway_sock.send(value.encode())

def read_ldr_data():
    ldr_data = ldr_sock.recv(1024).decode()
    return ldr_data

def upload_ldr_data():
    current_ldr_data_str = read_ldr_data()
    
    try:
        current_ldr_data_float = float(current_ldr_data_str)
        print("LDR Data (float):", current_ldr_data_float)
        
        # Enviar os dados LDR como float para o caminho "LDRATUAL" do Firebase
        db.reference("LDRATUAL").set(current_ldr_data_float)
        
    except ValueError:
        print(f"Erro ao converter os dados LDR: {current_ldr_data_str} não é um valor válido em ponto flutuante.")

# Restante do código...

def log_ldr_data():
    while True:
        # Aguardar 30 minutos
        time.sleep(1800)

        # Obter dados LDR
        current_ldr_data_str = read_ldr_data()

        try:
            # Tentar converter os dados LDR para float
            current_ldr_data_float = float(current_ldr_data_str)
            
            # Obter data e hora atual no formato desejado
            current_datetime = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")

            # Criar registro com apenas o valor do LDR
            log_entry = {"value": current_ldr_data_float}

            # Adicionar registro ao caminho "LDR" no Firebase com a chave única como data e hora
            db.reference(f"LDR/{current_datetime}").set(log_entry)

        except ValueError:
            print(f"Erro ao converter os dados LDR para float: {current_ldr_data_str}")

try:
    upload_ldr_data()

except KeyboardInterrupt:
    print("Programa encerrado.")
finally:
    gateway_sock.close()
    ldr_sock.close()

# Iniciar a função de log em uma thread separada
import threading
log_thread = threading.Thread(target=log_ldr_data)
log_thread.start()
