# DigiYatra System on Raspberry Pi

## Overview

The DigiYatra system implemented on a Raspberry Pi offers a fundamental yet effective solution for improving the boarding process at airports. By integrating simple QR code scanning and basic facial recognition capabilities, this project lays the groundwork for a more streamlined and efficient passenger experience.

## Project Setup and Execution Instructions

### Step 1: Prepare the Face Images

1. **Create Database on MySQL**:

    ```bash
        create database DigiYatra;

        create table FlightInformation (
            id INT PRIMARY KEY auto_increment,
            PNR int,
            Flight_information text,
            QR_code BLOB
        );
    ```

2. **insert data in table**:
    - use server/insert.py file to insert data in table
      
     ```bash
        python DigiYatra/DigiYatra Rasp/server/insert.py
    ```

1. **Upload Face Images**:
   - Upload the face images of the passengers to the `controller/Images` folder.

2. **Generate Encodings**:
   - Run the `encodeGenerator.py` script to create a ` pickle` file containing the encoded facial features of the uploaded images.

     ```bash
         python controller/encodeGenerator.py
     ```

### Step 2: Set Up and Run the Facial Recognition System

1. **Run the Facial Recognition Script**:
   - Execute the `main.py` script, which will detect the face of the passenger.

     ```bash
         python controller/main.py
     ```

2. **Run the QR Code Reader Script**:
   - Execute the `reader.py` script to read the QR code displayed on the website using a USB QR code reader.

     ```bash
         python controller/reader.py
     ```

### Step 3: Set Up and Run the Web Server

1. **Navigate to the Server Folder**:
   - Change to the `server` directory:

     ```bash
         cd server
     ```

2. **Run the Web Server**:
   - Execute the `server.py` script to serve the website over HTTPS.

     ```bash
         python server/server.py
     ```

3. **Run the API Server**:
   - Execute the `app.py` script to provide an API for the website.

     ```bash
         python server/app.py
     ```

### Step 4: Use the Web Interface

1. **Access the Website**:
   - Open a web browser and navigate to the URL served by `server.py`.

2. **Allow Camera Access**:
   - When prompted, allow the website to access the camera.

3. **Scan the Passenger Barcode**:
   - Place the passenger's boarding pass barcode in front of the camera. The website will scan the QR code and extract the PNR.

4. **Fetch Flight Information**:
   - The scanned PNR will be used to fetch the flight information from the MySQL database.

### Step 5: Scan the QR Code with Reader

1. **Use the USB QR Code Reader**:
   - The QR code displayed on the website can now be scanned using the `reader.py` script, which interacts with the USB QR code reader.

### Summary of Commands

1. **Generate face encodings**:
   ```bash
       python DigiYatra/DigiYatra Rasp/controller/encodeGenerator.py
   ```

2. **Run the facial recognition script**:
    ```bash
        python DigiYatra/DigiYatra Rasp/controller/main.py
    ```

3. **Run the QR code reader script**:
    ```bash
        python DigiYatra/DigiYatra Rasp/controller/reader.py
    ```

4. **Serve the website**:
    ```bash
        python DigiYatra/DigiYatra Rasp/server/server.py
    ```
5. **Run the flask API**:
    ```bash
        python DigiYatra/DigiYatra Rasp/server/app.py
    ```

By following these steps, you will set up the DigiYatra system on your Raspberry Pi, allowing you to scan QR codes, fetch flight information, and perform facial recognition for passenger verification.



**I created this project during my learning phase. If you'd like to contribute to this repository to improve the project, you're welcome to do so!**


