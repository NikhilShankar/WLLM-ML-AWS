import json
import base64
import os
import tempfile
from CosinePredictionHelper import CosinePredictionHelper
import boto3

# Initialize predictor at module level for reuse across invocations
modelmap = {
    "ModelA": "s3://your-s3-bucket-name/FinalizedModelsForAWS/WLLM-Model-0001",
    "ModelB": "s3://your-s3-bucket-name/FinalizedModelsForAWS/WLLM-Model-0002",
    "ModelC": "s3://your-s3-bucket-name/FinalizedModelsForAWS/WLLM-Model-0003"
}

image_dataset_path = "s3://your-s3-bucket-name/dataset"
predictor = None  # Will be initialized on first use

def init_predictor():
    global predictor
    if predictor is None:
        predictor = CosinePredictionHelper(
            models=modelmap,
            N=5,
            image_dataset_s3_path=image_dataset_path
        )

def lambda_handler(event, context):
    try:
        # Initialize predictor if not already done
        init_predictor()

        # Handle both API Gateway and direct Lambda invocations
        if 'body' in event:
            if isinstance(event['body'], str):
                body = json.loads(event['body'])
                image_data = base64.b64decode(body['image'])
            else:
                image_data = base64.b64decode(event['body'])
        else:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No image data provided'})
            }

        # Save image to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as temp_file:
            temp_file.write(image_data)
            temp_path = temp_file.name

        try:
            # Process image
            top_average, top_score = predictor.run_pipeline(temp_path)

            return {
                'statusCode': 200,
                'body': json.dumps({
                    'top_average': top_average.to_dict(),
                    'top_score': top_score.to_dict()
                })
            }
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }