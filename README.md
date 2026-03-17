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

## 💰 Analisi dei Costi (AWS Lean Architecture)

Il progetto è progettato con un approccio **Serverless-First**, eliminando i costi fissi delle istanze accese 24/7 e pagando solo per l'effettivo utilizzo (Pay-per-use).

| Servizio AWS | Componente | Stima Mensile ($) | Modello di Costo |
| :--- | :--- | :--- | :--- |
| **AWS IoT Core & Lambda** | Ingestione dati e Logica Guard | $1.00 - $2.00 | Pay-per-invocation |
| **Amazon S3 & KMS** | Threat Repository & Cifratura | ~$1.50 | Storage & Key management |
| **SageMaker Serverless** | Inferenza AI Zero-Day | $5.00 - $10.00 | Pay-per-inference |
| **CloudWatch** | Logging e Alerting | ~$1.00 | Ingestione log |
| **TOTALE STIMATO** | **Protezione 24/7** | **$10.00 - $15.00** | **Risparmio > 80% vs EC2** |

> **Nota:** La stima si basa su un piccolo parco dispositivi. Grazie all'architettura serverless, se non c'è traffico, i costi si avvicinano allo zero (eccezion fatta per lo storage minimo e le chiavi KMS).

## 💻 Setup Locale (Simulation Mode)
Per testare il progetto senza costi AWS reali, abbiamo utilizzato **LocalStack** e **Docker**.

1. **Avvia LocalStack:**
   ```bash
   docker run --rm -it -p 4566:4566 localstack/localstack
   ```
2. **Lancio del Server:**
   ```bash
   heartwall_server.py
   ```
3. **Avvia la Dashboard:**
   ```bash
   heartwall_bridge.html
   ```
   
