import requests

# Constants
API_ENDPOINT = "http://127.0.0.1:3050/tm-api/v1/generateCompanyStyleImage"

def test_api(logo_path, product_image_path):
    # Open the files in binary mode
    with open(logo_path, 'rb') as logo_file, open(product_image_path, 'rb') as product_file:
        # Prepare the files to be sent in the request
        files = {
            'logo': logo_file,
            'product_image': product_file,
        }

        # Make the POST request to the API
        response = requests.post(API_ENDPOINT, files=files)

        # Check the status code and print the result
        if response.status_code == 200:
            print("Request was successful!")
            print("Response:")
            # Assuming the response is an image, save it to a file
            with open('output.png', 'wb') as output_file:
                output_file.write(response.content)
            print("Image saved as output.png")
        else:
            print(f"Request failed with status code: {response.status_code}")
            print("Response:")
            print(response.text)

# Specify the path to your image files
logo_path = 'D:\\Logo-placement\\test_images\\logo_images\\nasa_logo.jpg'
product_image_path = 'D:\\Logo-placement\\test_images\\product_images\\Astronaut-in-Space-Art-Concept.jpg'

# Call the function and test the API
if __name__ == "__main__":
    test_api(logo_path, product_image_path)
