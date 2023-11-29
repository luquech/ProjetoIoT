#include <WiFi.h>
#include <FirebaseArduino.h>

const char *ssid = "moto g7";
const char *password = "12345678";
const char *host = "projetoiot-6f20f-default-rtdb.firebaseio.com";
const char *auth = "WLGlqx2B2UYzwOQenIkvRLwwQRidhgx1sTokE3k9";

const int pinLed = 14;  // Pino do LED
const int pinLDR = A0;  // Pino do LDR
const float limiarLDR = 2.0;  // Valor de limiar do LDR, ajuste conforme necessário

void setup() {
  Serial.begin(115200);

  // Inicialização do Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi");

  // Inicialização da conexão com o Firebase
  Firebase.begin(host, auth);
}

unsigned long lastReadingTime = 0;
unsigned long readingInterval = 59500;  // Intervalo de 60 segundos entre leituras

void loop() {
  unsigned long currentTime = millis();

  // Verifica se é hora de fazer uma nova leitura
  if (currentTime - lastReadingTime >= readingInterval) {
    leitura();  // Executa a leitura do sensor LDR e envia para o Firebase
    lastReadingTime = currentTime;  // Atualiza o último tempo de leitura
  }
  atual();
  // Verifica o estado da luz no Firebase
  if (Firebase.getBool(firebaseData, "/luz")) {
    if (firebaseData.boolData()) {
      Serial.println("Luz Acesa");
      acenderLed();
    } else {
      Serial.println("Luz Apagada");
      apagarLed();
    }
  } else {
    Serial.println("Não foi possível conectar ao Firebase");
  }
  delay(500);
}

void leitura() {
  // Leitura do sensor LDR
  int sensorValue = analogRead(pinLDR);
  float voltagem = sensorValue * (3.3 / 1023.0);  // Assume que o LDR está conectado a 3.3V

  // Mostra o valor da voltagem no monitor serial
  Serial.println("Valor armazenado do LDR: " + String(voltagem));

  String timestamp = Firebase.time();

  // Envia o dado da variável voltagem para a variável LDR no Firebase com um timestamp
  Firebase.pushFloat("LDR/" + timestamp, voltagem);
}

void atual() {
  // Leitura do sensor LDR
  int sensorValue = analogRead(pinLDR);
  float voltagem = sensorValue * (3.3 / 1023.0);  // Assume que o LDR está conectado a 3.3V

  // Mostrar valor da voltagem no monitor serial
  Serial.println("Valor Atual do LDR: " + String(voltagem));

  // Envia o dado da variável voltagem para a variável LDR no Firebase
  Firebase.setFloat("LDRATUAL/volt", voltagem);
}

void acenderLed() {
  digitalWrite(pinLed, HIGH);
}

void apagarLed() {
  digitalWrite(pinLed, LOW);
}

