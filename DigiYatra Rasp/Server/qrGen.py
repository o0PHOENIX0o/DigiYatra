import qrcode
import mysql.connector
from io import BytesIO

def get_db():
    db = mysql.connector.connect(
        host='192.168.0.112',
        user='digiyatra',
        password='Phoenix@001',
        database='DigiYatra',
    )
    return db

def close_db(db):
    if db is not None:
        db.close()

def insert_qr_code(id, data):
    # Create a QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Add data to the QR code
    qr.add_data(data)
    qr.make(fit=True)

    # Create an image from the QR code instance
    img = qr.make_image(fill_color="black", back_color="white")

    # Save the image to a buffer
    buffer = BytesIO()
    img.save(buffer)
    buffer.seek(0)
    image_data = buffer.read()

    # Insert into database
    try:
        db = get_db()
        with db.cursor() as cursor:
            insert_query = "UPDATE FlightInformation SET QRCode=%s WHERE id=%s;"
            cursor.execute(insert_query, (image_data, id))
            db.commit()
            print("Image inserted successfully")
    except Exception as e:
        print(e)
    finally:
        close_db(db)

# Example usage
insert_qr_code(10, "3")
