import requests
import json

# Constants
API_ENDPOINT = "http://0.0.0.0:3050/tm-api/v1/userManagement" 

HEADERS = {
    "Content-Type": "application/json"  
}

def test_api(logo, product_image):
    # Construct the JSON payload
    payload = json.dumps({
        'logo': logo,
        'product_image':product_image
    })

    # Make the POST request to the API
    response = requests.post(API_ENDPOINT, headers=HEADERS, data=payload)
    
    # Check the status code and print the result
    if response.status_code == 200:
        print("Request was successful!")
        print("Response:")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response:")
        print(response.text)
        
if __name__ == "__main__":
    test_api()
