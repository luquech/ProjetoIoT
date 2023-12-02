#define LDR_PIN A0  // Pino analógico ao qual o sensor LDR está conectado
#define DEVICE_NAME "ESP32_LDR"

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
  pinMode(LDR_PIN, INPUT);
}

void loop() {
  if (SerialBT.hasClient()) {
    // Verifica se há um dispositivo Bluetooth conectado
    onBluetoothConnect(); // Chama a função onBluetoothConnect quando conectado
  } else {
    // Se não houver cliente Bluetooth, chama a função onBluetoothDisconnect
    onBluetoothDisconnect();
  }

  // Leitura do sensor LDR
  float ldrValue = analogRead(LDR_PIN);

  // Envie o valor do sensor LDR via Bluetooth
  SerialBT.print("LDR Value: ");
  SerialBT.println(ldrValue);

  delay(1000);  // Atraso opcional para evitar leituras muito frequentes
}
