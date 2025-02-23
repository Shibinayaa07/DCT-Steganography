 
from flask import Flask, render_template, request, send_file
import cv2
import numpy as np
import os
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load Encryption Key
def load_key():
    return open("secret.key", "rb").read()

# Encrypt Message
def encrypt_message(message):
    key = load_key()
    cipher = Fernet(key)
    encrypted_message = cipher.encrypt(message.encode())
    return base64.b64encode(encrypted_message).decode()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/hide", methods=["POST"])
def hide():
    file = request.files["image"]
    message = request.form["message"]
    file_path = os.path.join(UPLOAD_FOLDER, "input.png")
    file.save(file_path)
    return f"Stego-image created successfully."

if __name__ == "__main__":
    app.run(debug=True)

# Extract Message from Stego Image (DCT)
def extract_message_from_dct(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    dct = cv2.dct(np.float32(img))

    # Extract bits from the DCT coefficients (Example: Simple LSB Extraction)
    message_bits = []
    for i in range(0, 8):
        for j in range(0, 8):
            message_bits.append(int(dct[i, j]) & 1)

    message = ''.join([chr(int(''.join(map(str, message_bits[i:i+8])), 2)) 
                   for i in range(0, len(message_bits), 8)])


def extract_message(stego_image_path):
    # Load the stego image
    img = cv2.imread(stego_image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print("Error: Could not load stego image.")
        return None

    # Apply DCT to extract frequency components
    dct_img = cv2.dct(np.float32(img))

    # Extract least significant bits from DCT coefficients
    message_bits = []
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            message_bits.append(int(dct_img[i, j]) % 2)  # Extract LSB

    # Convert bits to characters (group 8 bits at a time)
    message = ''.join(
        [chr(int(''.join(map(str, message_bits[i:i+8])), 2)) 
         for i in range(0, len(message_bits), 8)]
    )

    # Extract actual message before null character
    message = message.split("\0")[0]  # Stops at null termination

    return message

# Test the extraction
extracted_message = extract_message("stego_image.png")
print("Extracted Message:", extracted_message)

