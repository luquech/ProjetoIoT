# Projeto de IoT 2023.2 com ESP32, Gateway Ubuntu e Google Firebase

Este repositório contém o código-fonte para um projeto de Internet das Coisas (IoT) que utiliza ESP32 como dispositivos de borda (nodes), um gateway executado em um ambiente Ubuntu e integração com o Google Firebase para armazenamento e controle remoto.

## Componentes do Projeto

### Nodes IoT (ESP32)
- Dois nodes IoT baseados em ESP32, programados em C++ e Python, respectivamente.
- Um node é responsável por acionar uma luz.
- O outro node monitora a luminosidade do ambiente.

### Gateway (Ubuntu)
- Um gateway que atua como intermediário entre os nodes e o Google Firebase.
- Desenvolvido para ser executado em um ambiente Ubuntu.
- Usa Bluetooth para se comunicar com os nodes IoT.

### Integração com o Google Firebase
- O gateway se comunica com o Google Firebase para enviar e receber dados dos nodes.
- Utiliza Firebase Realtime Database para armazenamento e sincronização em tempo real.

### Aplicativo de Controle
- Um aplicativo de controle programado em JavaScriot que interage com o Google Firebase para permitir o monitoramento e controle remoto dos nodes IoT. Pode ser acessado via https://ldrteste.andersonlucas.repl.co/

## Tecnologias Utilizadas
- Linguagens: C++, Python, JavaScript (para o aplicativo de controle).
- Plataformas: ESP32, Ubuntu.
- Protocolos: Bluetooth, Firebase Realtime Database.

Este projeto demonstra a integração de dispositivos de borda (ESP32) com um gateway e uma plataforma de armazenamento em nuvem (Google Firebase), permitindo controle remoto e monitoramento de dispositivos IoT.
