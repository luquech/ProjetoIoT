#define LED_PIN 13
#define DEVICE_NAME "ESP32_DESESPERO"

#include <BluetoothSerial.h>


#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif

BluetoothSerial SerialBT;

void onBluetoothConnect() {
  Serial.println("Conectado via Bluetooth!");
  delay(1000);
}

void onBluetoothDisconnect() {
  Serial.println("Desconectado via Bluetooth! Tentando reconectar...");
  delay(1000);

  // Tentar reconectar
  SerialBT.begin(DEVICE_NAME);
}

void setup() {
  Serial.begin(115200);
  SerialBT.begin(DEVICE_NAME);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  if (SerialBT.hasClient()) {
    // Verifica se há um dispositivo Bluetooth conectado
    onBluetoothConnect(); // Chama a função onBluetoothConnect quando conectado
  } else {
    // Se não houver cliente Bluetooth, chama a função onBluetoothDisconnect
    onBluetoothDisconnect();
  }

  if (SerialBT.available()) {
    String command = SerialBT.readString(); // Lê a string recebida via Bluetooth

    // Controlar o LED com base no comando recebido
    if (command == "LOW") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("Luz Ligada (LOW)");
    } else if (command == "HIGH") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("Luz Desligada (HIGH)");
    }
  }
}


