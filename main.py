from time import time
from fastapi import FastAPI, __version__, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(
    title="My APIs",
    description="Developer: Mirshad"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>My APIs</title>
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="bg-white p-8 rounded-lg shadow-lg">
        <h1 class="text-2xl font-bold mb-4">My Portfolio</h1>
        <ul class="mb-4">
            <li><a href="/docs" class="text-blue-500">/docs (APIs)</a></li>
            <li><a href="/redoc" class="text-blue-500">/redoc (APIs)</a></li>
        </ul>
        <p>Powered by <a href="https://mirshadkvr.xyz" target="_blank" class="text-blue-500">Mirshad</a></p>
    </div>
</body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)

@app.get('/api/v1/ping')
async def hello():
    return {'res': 'pong', 'version': __version__, "time": time()}

@app.post("/api/rc/challaninfo", tags=['RTO'])
async def get_challan_info(regn_no: str, token: str):
    url = "https://rto-challan-information-verification-india.p.rapidapi.com/api/rc/challaninfo"
    payload = {
        "regn_no": regn_no,
        "consent": "yes",
        "consent_text": "I hereby declare my consent agreement for fetching my information via AITAN Labs API"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": token,
        "X-RapidAPI-Host": "rto-challan-information-verification-india.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data from external API")

@app.post("/api/v1/rc/vehicleinfo", tags=['RTO'])
async def get_vehicle_info(reg_no: str, token: str):
    url = "https://rto-vehicle-information-verification-india.p.rapidapi.com/api/v1/rc/vehicleinfo"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": token,
        "X-RapidAPI-Host": "rto-vehicle-information-verification-india.p.rapidapi.com"
    }
    payload = {
        "reg_no": reg_no,
        "consent": 'Y',
        "consent_text": "I hereby declare my consent agreement for fetching my information via AITAN Labs API"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX and 5XX status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Catch any request exceptions and raise HTTPException with 500 status code
        raise HTTPException(status_code=500, detail=str(e))

@app.get('/api/v1/challan/tokens', tags=['RTO'])
def challan_tokens():
    data = [
        {"mirshadkvr19": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c"},
        {"mirshadrahman": "c054ac9b60mshd55e8424cbb5ad2p137e8djsn1e1c963c6a6f"},
        {"sparteck": "2ad016f13fmsh8581f9352e2defcp1535c6jsn279380adfedf"}
    ]
    return {"status": "200", "data": data}

@app.get('/api/v1/vehicleinfo/tokens', tags=['RTO'])
def vehicle_info_tokens():
    data = [
        {"mirshadkvr19": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c"},
        {"spartck": "2ad016f13fmsh8581f9352e2defcp1535c6jsn279380adfedf"},
        {"mirshad": "c054ac9b60mshd55e8424cbb5ad2p137e8djsn1e1c963c6a6f"}
    ]
    return {"status": "200", "data": data}

@app.post("/api/v1/music/search", tags=['Song'])
async def get_data(search: str):
    url = "https://jio-saavan-unofficial.p.rapidapi.com/getdata"
    querystring = {"q": search}
    headers = {
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "jio-saavan-unofficial.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch data")

@app.post("/api/v1/song/link", tags=['Song'])
async def get_song(link: str):
    url = "https://jio-saavan-unofficial.p.rapidapi.com/getsong"
    payload = {
        "encrypted_media_url": link
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "jio-saavan-unofficial.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch song")

@app.post("/api/v1/book", tags=['Books'])
async def get_books_info(required_param: str):
    url = "https://getbooksinfo.p.rapidapi.com/"
    querystring = {"s": required_param}
    headers = {
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "getbooksinfo.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch book info")

@app.post("/api/v1/phone_validate", tags=['Phone'])
async def phone_validate(number: str, country_code: str):
    url = "https://neutrinoapi-phone-validate.p.rapidapi.com/phone-validate"
    payload = {
        "number": number,
        "country-code": country_code
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "neutrinoapi-phone-validate.p.rapidapi.com"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to validate phone number")

@app.get("/api/v1/get_temp_email", tags=['Email'])
async def get_temp_email():
    url = "https://temp-mail44.p.rapidapi.com/api/v3/email/new"
    payload = {
        "key1": "value",
        "key2": "value"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch temporary email")

@app.post("/api/v1/get_temp_email_messages", tags=['Email'])
async def get_temp_email_messages(email: str):
    url = f"https://temp-mail44.p.rapidapi.com/api/v3/email/{email}/messages"
    headers = {
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "temp-mail44.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch temporary email messages")

@app.post("/api/v1/get_whatsapp_data", tags=["WhatsApp"])
async def get_whatsapp_data(phone_number: str):
    url = f"https://whatsapp-data1.p.rapidapi.com/number/{phone_number}"
    headers = {
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "whatsapp-data1.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch WhatsApp data")

@app.post("/api/v1/gpt_3", tags=["ChatGPT"])
async def fetch_chatgpt_response(message: str):
    url = "https://api.safone.dev/chatgpt"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "message": message,
        "version": 3,
        "chat_mode": "assistant",
        "dialog_messages": "[{\"bot\":\"\",\"user\":\"\"}]"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    
    # Extract the message content from the response
    message_content = response_data.get("choices", [])[0].get("message", {}).get("content", "")
    
    # Return the message content
    return {"message": message_content}
