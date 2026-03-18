# 🩺 HeartWall: AI-Driven Cybersecurity for IoT Pacemakers

**HeartWall** è un prototipo avanzato di sicurezza informatica progettato per proteggere i dispositivi medici impiantabili (IMD) da attacchi **Zero-Day** e manipolazioni biometriche. Il sistema utilizza un'architettura **MLOps su AWS** per rilevare anomalie in tempo reale e far evolvere le difese autonomamente.

https://github.com/user-attachments/assets/5c590927-940c-48dc-90c3-f3c3228df338

## 🚀 Key Features
* **Real-time Guard:** Una Lambda "Sentinella" che intercetta ogni pacchetto dati prima che raggiunga il sistema centrale.
* **Behavioral AI:** Analisi tramite AWS SageMaker che distingue tra aritmie naturali e tentativi di hacking (Bio-Tampering).
* **Self-Healing Loop:** Gli attacchi rilevati vengono isolati su S3 e usati per ri-addestrare automaticamente il modello.
* **Interactive Dashboard:** Interfaccia futuristica per il monitoraggio live dell'ECG e dei vettori di attacco.

## 🏗️ Architettura AWS & AI
* **AWS SageMaker:** Utilizzato per l'addestramento e il deployment del modello di Machine Learning specializzato nel rilevamento di anomalie Zero-Day.
* **AWS Lambda:** Funge da "Sentinella" serverless, processando ogni pacchetto dati con latenza minima.
* **Amazon S3:** Data Lake per l'archiviazione della telemetria sicura e dei campioni di attacco (Threat Repository).
* **AWS IoT Core:** Broker per la gestione sicura della messaggistica MQTT tra dispositivi medici e cloud.
* **IAM (Identity and Access Management):** Implementazione di policy *Least Privilege* per la massima sicurezza dei dati medici.

### 🔒 Sicurezza e Cifratura
Per proteggere i dati sensibili dei pazienti (PHI - Protected Health Information), l'architettura implementa:
* **AWS KMS (Key Management Service):** Cifratura a riposo per tutti i log e i dati salvati su S3.
* **VPC & Security Groups:** Tutte le comunicazioni tra Lambda e SageMaker avvengono all'interno di una rete isolata.
* **IAM Least Privilege:** Ogni servizio ha permessi limitati esclusivamente alle azioni necessarie (es. la Lambda può solo *leggere* da IoT Core e *scrivere* su S3).
  
![Architecture_diagram](https://github.com/user-attachments/assets/c461cc76-212c-4fd3-b892-9e931f482852)

### 🎬 Demo: Sincronizzazione Backend-Frontend
Questo video mostra il "cuore" operativo di HeartWall. A sinistra, il terminale **PowerShell** esegue il Super-Server Flask, mentre a destra la **Dashboard** visualizza i dati in tempo reale.

**Cosa osservare nel video:**
1. **Avvio del Server**: Il terminale mostra l'inizializzazione del bridge e la connessione a LocalStack (S3).
2. **Logging in Tempo Reale**: Ogni richiesta GET/POST proveniente dalla dashboard viene loggata istantaneamente nel terminale, mostrando il flusso continuo di telemetria.
3. **Trigger degli Attacchi**: Quando viene cliccato un pulsante sulla dashboard (es. *CMD Injection* o *Bio-Tampering*), si vede il cambio di stato immediato nel terminale (`Attack mode → CMD`), seguito dalla variazione dei parametri ECG e dai log di allerta.
4. **Sincronizzazione Dati**: Il server processa i dati simulati e li prepara per l'invio al cloud simulato, garantendo che la dashboard rifletta sempre l'esatto stato di sicurezza del dispositivo.

https://github.com/user-attachments/assets/a4cb7eec-0835-4027-b1c2-9dd0e6eb10ed

## 🛡️ Scenari di Attacco Simulati (Cyber-Attack Vectors)

Il sistema HeartWall è testato contro tre principali vettori di attacco IoT, visualizzabili in tempo reale nella dashboard:

### 1. 🟢 Normal Operation (Stato Sicuro)
* **Descrizione**: Il pacemaker invia parametri biometrici regolari.
* **Segnale**: Battito cardiaco tra 60-100 BPM, voltaggio stabile.
* **Risposta IA**: Score di anomalia basso (< 0.1). Il traffico è permesso.

![Dashboard_Normal](https://github.com/user-attachments/assets/09ca4e5f-d878-466f-af09-9d13f05f92c7)

### 2. ⚡ CMD Injection (Attacco al Protocollo)
* **Descrizione**: Un hacker tenta di iniettare comandi non autorizzati nel payload JSON per modificare le impostazioni del dispositivo.
* **Segnale**: Presenza di flag `command_override` o stringhe di sistema inaspettate nel pacchetto dati.
* **Risposta IA**: Identificazione di pattern sintattici sospetti. Segnalazione su dashboard e blocco del pacchetto.

![Attack_Injection Zero-Day](https://github.com/user-attachments/assets/fdc46d94-49cf-4cdf-9a8f-5a9129c549b8)

### 3. 🔘 Bio-Tampering (Manipolazione Biometrica)
* **Descrizione**: L'attaccante altera i dati medici inviati per indurre il sistema di monitoraggio a prendere decisioni errate (es. somministrazione di shock non necessari).
* **Segnale**: Frequenza cardiaca alterata artificialmente (es. 250 BPM istantanei) o cali di voltaggio improvvisi.
* **Risposta IA**: Rilevamento di deviazione comportamentale estrema. Trigger immediato dell'allarme SNS.

![Biosignal Tampering](https://github.com/user-attachments/assets/9f7c3225-f4c7-485b-bd4b-73c0ca675df3)

### 4. 💀 Combo P0 (Zero-Day Multi-Vettore)
* **Descrizione**: L'attacco più critico. Unisce la manipolazione dei dati biometrici all'iniezione di codice per tentare di bypassare i controlli standard.
* **Segnale**: Anomalie simultanee su più sensori e pacchetti formattati in modo malevolo.
* **Risposta IA**: Rilevamento di minaccia complessa. Isolamento totale della telemetria nel "Threat Repository" per analisi forense.

![Attack_Combo](https://github.com/user-attachments/assets/7da473d0-ad9b-49a2-9a63-8c4076343ea0)

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

## 🛠️ Tech Stack

### ⚙️ Backend & Simulation
* **Python 3.x:** Linguaggio core per la logica di analisi e automazione.
* **Flask:** Micro-framework utilizzato per creare il "Super-Server" bridge tra il simulatore e la dashboard.
* **Boto3:** SDK ufficiale di AWS per l'integrazione Pythonica con i servizi cloud.
* **Thread management:** Gestione parallela della telemetria real-time e dei processi di sincronizzazione cloud.

### 📊 Frontend & Visualization
* **HTML5 & CSS3:** Interfaccia utente ad alto contrasto (Cyber-Style) progettata per centri di monitoraggio medico (SOC).
* **Vanilla JavaScript:** Gestione dinamica dei grafici ECG e degli alert senza dipendenze pesanti.
* **Fetch API:** Sincronizzazione asincrona dei dati con il server locale ogni 100ms.

### 🔧 DevOps & Development Tools
* **Docker:** Containerizzazione dell'ambiente di test.
* **LocalStack:** Emulazione locale dei servizi AWS per lo sviluppo e il testing a costo zero.
* **PowerShell:** Gestione del workflow di sviluppo e automazione dei task locali.
  
## 💻 How to Run
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
@ AWS HeartWall IoT Cybersecurity 2026
