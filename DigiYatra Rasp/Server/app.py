from flask import Flask, render_template, request, jsonify,g
from flask_cors import CORS  # Import the CORS extension
import qrcode
import base64
import json
from decimal import Decimal 

import mysql.connector

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes



# --------------------------------- <- json encoder -> ----------------------------------
class CustomEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        elif isinstance(o, bytes):
            return base64.b64encode(o).decode('utf-8')
        return super().default(o)




def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            host=app.config['DB_HOST'],
            user=app.config['DB_USER'],
            password=app.config['DB_PASSWORD'],
            database=app.config['DB_DATABASE']
        )
    return g.db


# --------------------------------- <- close db -> ---------------------------------
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()



    

def isPNR(PNR):
    try:
        db = get_db()
        with db.cursor(dictionary=True) as cursor:
            check_query = "SELECT COUNT(*) AS count FROM FlightInformation where PNR=%s"
            cursor.execute(check_query, (PNR,))
            result = cursor.fetchone()
            
            if(result['count']>0):
                return True
            else:
                return False
            

    except Exception as e:
        print(e)
        return False
    finally:
        close_db()


def getData(PNR):
    try:
        db = get_db()
        with db.cursor(dictionary=True) as cursor:
            check_query = "SELECT * FROM FlightInformation where PNR=%s"
            cursor.execute(check_query, (PNR,))
            result = cursor.fetchone()
            return result

    except Exception as e:
        print(e)
        return False
    finally:
        close_db()


@app.route('/process_barcode', methods=['POST'])
def barcode():
    PNR = request.json.get('barcode', '')
    print('Received barcode:', PNR)

    data = isPNR(PNR)
    print(data)
    if data:
        userData = getData(PNR)
        json_data = json.dumps(userData, indent=4, cls=CustomEncoder)
        return json_data
    else:
        return jsonify(False)

if __name__ == '__main__':
    app.config['DB_HOST'] = '172.16.16.176'
    app.config['DB_USER'] = 'digiyatra'
    app.config['DB_PASSWORD'] = 'Phoenix@001'
    app.config['DB_DATABASE'] = 'DigiYatra'

    app.run(host="0.0.0.0", port=5000, debug=True, ssl_context=('/home/alpha/DigiYatra/server.cert', '/home/alpha/DigiYatra/server.key'))



