#include <BluetoothSerial.h>

BluetoothSerial SerialBT;

#define LED_PIN 13  // Pino do LED
#define LDR_PIN 34   // Pino de leitura do sensor LDR

void setup() {
  Serial.begin(115200);
  SerialBT.begin("ESP32_DESESPERO");  // Substitua pelo nome desejado

  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // Ler valor do sensor LDR
  int ldrValue = analogRead(LDR_PIN);

  // Enviar valor do sensor LDR via Bluetooth
  SerialBT.println(ldrValue);

  // Receber comando via Bluetooth
  if (SerialBT.available()) {
    String command = SerialBT.readString();

    // Controlar o LED com base no comando recebido
    if (command == "LOW") {
      digitalWrite(LED_PIN, LOW);
      Serial.println("Luz Ligada (LOW)");
    } else if (command == "HIGH") {
      digitalWrite(LED_PIN, HIGH);
      Serial.println("Luz Desligada (HIGH)");
    }
  }

  delay(1000);  // Aguardar um segundo antes da próxima iteração
}
