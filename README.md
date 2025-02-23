# DCT-Steganography
# DCT Steganography

This project implements **Discrete Cosine Transform (DCT) Steganography** using Python and Flask. It allows users to **hide** and **extract** messages from images.

## Features
- Hide a secret message inside an image using DCT.
- Extract the hidden message from the stego-image.
- Web-based interface using Flask.

## Project Structure
```
DCT_Steganography/
│── app.py  # Main Flask application
│── templates/
│   └── index.html  # Web UI
│── static/
│── uploads/  # Stores images
│── requirements.txt  # Dependencies
│── README.md  # Documentation
```

## Dependencies
The required libraries are:
```sh
flask
opencv-python
numpy
```

