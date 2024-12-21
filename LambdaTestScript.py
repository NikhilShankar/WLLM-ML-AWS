import base64
import json
import requests
import sys

def test_lambda_function(image_path):
    """
    Test the Lambda function with an image file
    """
    # Read and encode the image
    with open(image_path, 'rb') as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
    
    # Prepare the request payload
    payload = {
        "body": {
            "image": encoded_image
        }
    }
    
    # Make the request to local Lambda
    response = requests.post(
        "http://localhost:9000/2015-03-31/functions/function/invocations",
        json=payload
    )
    
    # Print results
    print("\nStatus Code:", response.status_code)
    print("\nResponse Body:")
    print(json.dumps(response.json(), indent=2))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_lambda.py <path_to_image>")
        sys.exit(1)
    
    test_lambda_function(sys.argv[1])