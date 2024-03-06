"""
Run this script to simulate the third-party request to the service B application.
"""
import requests


if __name__ == "__main__":
    # Do the request that will hang on
    response = requests.get("http://localhost:8080/hang_on")

    # Even if the application is killed, it will return a 200 code
    if 200 == response.status_code:
        print("Yeah! The application replied with HTTP 200.")
    else:
        print("Oh no! Something went wrong.")

    print(f"Status Code: {response.status_code}")
    print(f"Reason: {response.reason}")
