# Simple Basic API

This project demonstrates a simple API with one model: User. The storage of these users is done via serialization/deserialization in files.

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/alx-backend-user-data.git
   cd alx-backend-user-data/0x01-Basic_authentication
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
   ```

## Usage

Send a GET request to the `/api/v1/status` endpoint:
```bash
curl "http://0.0.0.0:5000/api/v1/status" -vvv

