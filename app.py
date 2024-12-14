from flask import Flask, jsonify, request
import uuid
import re
import math

app = Flask(__name__)

#to check the server
@app.route("/", methods=["GET"])
def home():
    return "hello world"

#in-memory dictionary
receipt_store = {}

@app.route("/store", methods=["GET"])
def store():
    return jsonify(receipt_store), 200

@app.route("/receipts/process", methods=["POST"])
def process_receipt():
    # Add print statements to debug
    print("Received request", request)
    print("Request method:", request.method)
    print("Request content type:", request.content_type)
    
    data = request.get_json()
    # print("Received data:", data)
    
    if not validate_data(data):
        return "Invalid Format", 400
    print("Data is Validated")
    
    points = calculate_points(data)
    print("Points Calculated: ", points)
    receipt_id = str(uuid.uuid4())
    receipt_store[receipt_id] = {
        "receipt": data,
        "points": points
    }
    # print("Reipt stored: ", receipt_store)
    
    return jsonify({"id": receipt_id}), 200

@app.route("/receipts/<receipt_id>/points", methods=["GET"])
def receipt_point(receipt_id):
    result = receipt_store[receipt_id]
    if not result:
        return "Not found result", 404
    return jsonify({"points": result["points"]}), 200

def validate_data(receipt):
    required_fields = ["retailer", "purchaseDate", "purchaseTime", "items", "total"]
    if any(field not in receipt for field in required_fields):
        return False
    retailer = receipt["retailer"]
    purchaseDate = receipt["purchaseDate"]
    purchaseTime = receipt["purchaseTime"]
    items = receipt["items"]
    total = receipt["total"]
    
    #Now start Validating basic formats
    if not retailer or not items or not total: # we should do something about the purchase dates and time if not avaialable
        print("No retailer or items or total")
        return False
    if len(items) < 1: # if there are no items
        print("No items inside")
        return False
    
    #validating the price of total
    # if not validate_price(total):
    #     print("No total")
    #     return False
    
    if not validate_date(purchaseDate):
        print("Not valid date")
        return False
    if not validate_time(purchaseTime):
        print("Not valid time")
        return False
    
    for item in items:
        if "shortDescription" not in item or "price" not in item:
            print("Not desc or no price")
            return False
        # if not validate_price(item["price"]):
        #     print("Not price")
        #     return False
    return True
    


def calculate_points(receipt):
    points = 0
    retailer = receipt["retailer"]
    purchaseDate = receipt["purchaseDate"]
    purchaseTime = receipt["purchaseTime"]
    items = receipt["items"]
    total = receipt["total"]
    
    
    # One point for every alphanumeric character in the retailer name.
    points += count_alphanumeric(retailer)
    # 50 points if the total is a round dollar amount with no cents.
    if round_dollar(total):
        points += 50
    # 25 points if the total is a multiple of 0.25.
    if multiple_of_25(total):
        points += 25
    # 5 points for every two items on the receipt.
    points += (len(items) // 2) * 5
    # If the trimmed length of the item description is a multiple of 3, multiply the price by 0.2 and round up to the nearest integer. The result is the number of points earned.
    for item in items:
        desc = item["shortDescription"].strip()
        if len(desc) % 3 == 0:
            item_price = float(item["price"])
            item_points = math.ceil(item_price * 0.2)
            points += item_points
        
    # 6 points if the day in the purchase date is odd.
    if date_odd(purchaseDate):
        points += 6
    # 10 points if the time of purchase is after 2:00pm and before 4:00pm.
    if purchase_time(purchaseTime):
        points += 10
    return points


def validate_price(price):
    if not re.match(r"^\d+\.\d{2}$", price):
        return False
    
def validate_date(buyDate):
    date_parts = buyDate.split("-")
    if len(date_parts) != 3:
        return False
    year, month, day = date_parts
    if not(year.isdigit() or month.isdigit() or day.isdigit()):
        return False
    y, m, d = int(year), int(month), int(day)
    if y < 1 or m < 1 or m > 12 or d < 1 or d > 31:
        return False
    
    return True

def validate_time(buyTime):
    time_parts = buyTime.split(":")
    if len(time_parts) != 2:
        return False
    hh, mm = time_parts
    print(hh,mm)
    if not (hh.isdigit() or mm.isdigit()):
        return False
    h , m = int(hh), int(mm)
    if h < 0 or h > 23 or m < 0 or m > 59:
        return False
    return True

def count_alphanumeric(ret):
    point = 0
    for c in ret:
        if c.isalnum():
            point += 1
    return point

def round_dollar(price):
    price = float(price)
    return price.is_integer() 

def multiple_of_25(price):
    price = float(price)
    factors = price / 0.25
    return abs(factors - round(factors)) < 1e-9

def date_odd(purchase_date):
    date_parts = purchase_date.split("-")
    day = date_parts[2]
    if int(day) % 2 == 1:
        return True
    else:
        return False

def purchase_time(purchase_time):
    hh, mm = purchase_time.split(":")
    h , m = int(hh), int(mm)
    time_in_mintue = h*60 + m 
    start = 14*60
    end = 16*60
    if start <= time_in_mintue <= end:
        return True
    else:
        return False
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)