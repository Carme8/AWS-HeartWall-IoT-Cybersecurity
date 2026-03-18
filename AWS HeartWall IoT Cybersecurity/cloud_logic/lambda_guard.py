import json
import boto3
import os

# Client AWS
runtime = boto3.client('runtime.sagemaker')
sns = boto3.client('sns')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    # 1. Ricezione dati dal Pacemaker
    pacemaker_data = json.dumps(event)
    
    # 2. Chiamata a SageMaker Active Model
    response = runtime.invoke_endpoint(
        EndpointName='HeartWall-Active-Model',
        ContentType='application/json',
        Body=pacemaker_data
    )
    
    result = json.loads(response['Body'].read().decode())
    
    # 3. Logica di Protezione (Zero-Day)
    if result['anomaly_score'] > 0.8:  # Soglia di pericolo
        # ALERT: Invio notifica immediata via SNS
        sns.publish(
            TopicArn=os.environ['SNS_TOPIC_ARN'],
            Message=f"ATTENZIONE: Rilevata anomalia critica sul dispositivo! Score: {result['anomaly_score']}",
            Subject="HEARTWALL ALERT"
        )
        
        # BACKUP: Salva l'attacco su S3 per il re-training
        s3.put_object(
            Bucket=os.environ['THREAT_BUCKET'],
            Key=f"threats/{context.aws_request_id}.json",
            Body=pacemaker_data
        )
        return {"status": "BLOCKED", "reason": "Anomaly detected"}

    return {"status": "ALLOWED", "data": "Telemetry OK"}