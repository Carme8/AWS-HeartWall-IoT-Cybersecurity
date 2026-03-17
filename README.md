# 🩺 HeartWall: AI-Driven Cybersecurity for IoT Pacemakers

**HeartWall** è un prototipo avanzato di sicurezza informatica progettato per proteggere i dispositivi medici impiantabili (IMD) da attacchi **Zero-Day** e manipolazioni biometriche. Il sistema utilizza un'architettura **MLOps su AWS** per rilevare anomalie in tempo reale e far evolvere le difese autonomamente.

## 🚀 Key Features
* **Real-time Guard:** Una Lambda "Sentinella" che intercetta ogni pacchetto dati prima che raggiunga il sistema centrale.
* **Behavioral AI:** Analisi tramite AWS SageMaker che distingue tra aritmie naturali e tentativi di hacking (Bio-Tampering).
* **Self-Healing Loop:** Gli attacchi rilevati vengono isolati su S3 e usati per ri-addestrare automaticamente il modello.
* **Interactive Dashboard:** Interfaccia futuristica per il monitoraggio live dell'ECG e dei vettori di attacco.

## 🏗️ Architettura del Sistema
Il sistema si basa su un flusso di dati circolare:
1. **IoT Device (Simulator)** → Invia telemetria cifrata.
2. **AWS Lambda (The Guard)** → Interroga il modello di Machine Learning.
3. **AWS SageMaker (The Brain)** → Valuta lo score di anomalia.
4. **AWS SNS (Alert)** → Notifica immediata in caso di attacco.
5. **Feedback Loop** → I dati salvati su S3 migliorano il modello per le minacce future.

## 💻 Setup Locale (Simulation Mode)
Per testare il progetto senza costi AWS reali, abbiamo utilizzato **LocalStack** e **Docker**.

1. **Avvia LocalStack:**
   ```bash
   docker run --rm -it -p 4566:4566 localstack/localstack
