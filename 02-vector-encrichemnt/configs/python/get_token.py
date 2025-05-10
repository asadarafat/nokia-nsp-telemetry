import http.client
import json
import ssl
import base64
import os
import time

# Load configuration from environment variables
NSP_AUTH_URL = os.getenv("NSP_AUTH_URL", "/rest-gateway/rest/api/v1/auth/token")
NSP_IP = os.getenv("NSP_IP", "127.0.0.1")
PORT = int(os.getenv("AUTH_PORT", "443"))
NSP_USER = os.getenv("NSP_USER", "")
NSP_PASS = os.getenv("NSP_PASS", "")
TOKEN_FILE = os.getenv("AUTH_TOKEN_FILE", "/tmp/access_token.json")

TOKEN_FILE_TXT = os.getenv("AUTH_TOKEN_FILE_TXT", "/tmp/access_token.txt")


TOKEN_EXPIRY_BUFFER = int(os.getenv("AUTH_TOKEN_EXPIRY_BUFFER", "60"))
REFRESH_CHECK_INTERVAL = int(os.getenv("AUTH_REFRESH_INTERVAL", "30"))  # in seconds

# Create an unverified SSL context (only for dev or test environments)
SSL_CONTEXT = ssl._create_unverified_context()

def load_cached_token():
    """
    Load cached token from file if it exists and is not expired.
    Returns the token string if valid, otherwise None.
    """
    if not os.path.isfile(TOKEN_FILE):
        return None

    try:
        with open(TOKEN_FILE, "r") as f:
            token_data = json.load(f)

        expires_at = token_data.get("fetched_at", 0) + token_data.get("expires_in", 0) - TOKEN_EXPIRY_BUFFER
        if time.time() < expires_at:
            return token_data.get("access_token")
    except Exception:
        pass  # Silently ignore and force token refresh

    return None

def fetch_token():
    """
    Fetch a new access token from the authentication endpoint.
    Save it to a file with expiry metadata.
    Returns the access token string if successful.
    """
    credentials = f"{NSP_USER}:{NSP_PASS}"
    encoded_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded_credentials}"
    }

    payload = json.dumps({
        "grant_type": "client_credentials"
    })

    conn = http.client.HTTPSConnection(NSP_IP, PORT, context=SSL_CONTEXT)
    conn.request("POST", NSP_AUTH_URL, body=payload, headers=headers)
    response = conn.getresponse()
    data = response.read()
    conn.close()

    try:
        response_json = json.loads(data.decode("utf-8"))
        access_token = response_json.get("access_token")
        expires_in = response_json.get("expires_in", 3600)

        if access_token:
            token_data = {
                "expires_in": expires_in,
                "fetched_at": int(time.time()),
                "access_token": access_token
            }
            with open(TOKEN_FILE, "w") as f:
                json.dump(token_data, f, indent=2)

            with open(TOKEN_FILE_TXT, "w") as f:
                # f.write(f'TOKEN=" \\"{access_token}\\""')
                f.write(f'TOKEN={access_token}')

            return access_token
    except json.JSONDecodeError:
        pass

    return None

def get_access_token():
    """
    Retrieve a valid access token from cache or refresh if expired.
    Returns the access token string.
    """
    token = load_cached_token()
    if token:
        return token
    return fetch_token()

def run_token_refresher():
    """
    Periodically check and refresh the access token if needed.
    """
    while True:
        token = get_access_token()
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        if token:
            print(f"[{timestamp}] Access token is valid.")
        else:
            print(f"[{timestamp}] Failed to obtain a valid token.")

        time.sleep(REFRESH_CHECK_INTERVAL)

if __name__ == "__main__":
    run_token_refresher()
