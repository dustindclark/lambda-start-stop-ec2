import boto3
import os

# Enter the region your instances are in, e.g. 'us-east-1'
region = 'us-east-1'

# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']
instances =  ['X-XXXXXXXX', 'X-XXXXXXXX']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ses = boto3.client('ses', region_name=region)
    instanceStatuses = ec2.describe_instance_status(InstanceIds=[instances[0]])['InstanceStatuses']
    message = ''
    if instanceStatuses and instanceStatuses[0]['InstanceState']['Code'] == 16:
        ec2.stop_instances(InstanceIds=instances)
        message = 'EC2 - Stopped Instances: ' + str(instances)
    else:
        ec2.start_instances(InstanceIds=instances)
        message = 'EC2 - Started Instances: ' + str(instances)
    response = ses.send_email(
        Source = os.environ['email_from'],
        Destination={
            'ToAddresses': [
                os.environ['email_to'],
            ]
        },
        Message={
            'Subject': {
                'Data': message
            },
            'Body': {
                'Text': {
                    'Data': message
                },
                'Html': {
                    'Data': message
                }
            }
        }
    )