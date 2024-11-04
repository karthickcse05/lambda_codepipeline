import boto3
import os

def lambda_handler(event, context):
    # Environment variables for target account details
    target_account_role_arn = os.environ['TARGET_ACCOUNT_ROLE_ARN']
    target_pipeline_name = os.environ['TARGET_PIPELINE_NAME']
    
    # Assume the role in the target account
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn=target_account_role_arn,
        RoleSessionName='CrossAccountPipelineTriggerSession'
    )
    
    # Extract temporary credentials
    credentials = assumed_role['Credentials']
    
    # Create a CodePipeline client using the temporary credentials
    codepipeline_client = boto3.client(
        'codepipeline',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    
    # Trigger the pipeline in the target account
    response = codepipeline_client.start_pipeline_execution(
        name=target_pipeline_name
    )
    
    return {
        'statusCode': 200,
        'body': f"Pipeline {target_pipeline_name} triggered successfully in target account."
    }

