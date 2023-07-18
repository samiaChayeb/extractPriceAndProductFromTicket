import cv2
import numpy as np
import pytesseract
import re
from tabulate import tabulate
from flask import Flask, jsonify, request

app = Flask(__name__)

# Define the API route
@app.route('/api', methods=['POST'])
def api():
    # Get the uploaded image from the request
    # Preprocess the image
    image = request.files['image']
    # Read the image using OpenCV
    image = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR)
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Apply image preprocessing (adjust based on your image characteristics)
    preprocessed = cv2.medianBlur(gray, 3)

    # Perform OCR to extract text from the image
    ticket_text = pytesseract.image_to_string(preprocessed)

    # Split the text into lines
    lines = ticket_text.split('\n')

    # Remove empty lines and lines containing irrelevant information
    lines = [line.strip() for line in lines if line.strip()]
    strings = [line for line in lines if re.search(r'\d{3}d', line)]

    product_price_pattern = r'(\d+(?:\s*\w+)*\s+(?:\w+\s*)+\d+\.\s*\d+d)'
    data=[]
    for string in strings:
        price = re.findall(r'\d+\s*\.\s*\d+d', string)[0]
        product = re.sub(price, "", string).strip().rstrip(".")
        data.append([product, price])
    table = tabulate(data, headers=['product','price'], tablefmt="grid")
    return jsonify(data)

# Run the Flask app


if __name__ == '__main__':
    app.run()