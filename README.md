# Receipt Processor Application

## Project Setup and Installation

### Prerequisites
- Docker installed on your system
- Thunder Client (or similar API testing tool)

### Steps to Run the Application

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd receipt-processor
   ```

2. **Build Docker Image**
   ```bash
   docker build -t receipt-processor .
   ```

3. **Run Docker Container**
   ```bash
   docker run -p 3000:3000 receipt-processor
   ```

### API Endpoints

#### 1. Process Receipt
- **URL:** `http://localhost:3000/receipts/process`
- **Method:** POST
- **Headers:** 
  - `Content-Type: application/json`

#### 2. Get Receipt Points
- **URL:** `http://localhost:3000/receipts/<receipt-id>/points`
- **Method:** GET

### Example Request Body
```json
{
  "retailer": "Target",
  "purchaseDate": "2022-01-01",
  "purchaseTime": "13:01",
  "items": [
    {
      "shortDescription": "Mountain Dew 12PK",
      "price": "6.49"
    },
    {
      "shortDescription": "Emils Salsa",
      "price": "2.99"
    }
  ],
  "total": "9.48"
}
```

### Testing with Thunder Client
1. Open Thunder Client
2. Create a new POST request
3. Set URL to `http://localhost:3000/receipts/process`
4. Add Header:
   - Key: `Content-Type`
   - Value: `application/json`
5. Set request body to the example JSON above
6. Send the request

### Scoring Points
The application calculates points based on various receipt characteristics:
- Alphanumeric characters in retailer name
- Round dollar amounts
- Specific time of purchase
- Number of items
- Item description length

### Troubleshooting
- Ensure Docker is running
- Check that port 3000 is not in use by another application
- Verify all dependencies are installed

## Development

### Local Development
If you want to run the application without Docker:
```bash
python3 -m pip install flask
python3 app.py
```

### Contributing
Please read the contributing guidelines before making any changes.
