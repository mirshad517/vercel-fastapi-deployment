from time import time
from fastapi import FastAPI, __version__, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import requests

app = FastAPI(
    title="My Apis",
    description="Developer : Mirshad"
)
app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>My Apis</title>
    <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 flex items-center justify-center h-screen">
    <div class="bg-white p-8 rounded-lg shadow-lg">
        <h1 class="text-2xl font-bold mb-4">My Portfolio</h1>
        <ul class="mb-4">
            <li><a href="/docs" class="text-blue-500">/docs (apis)</a></li>
            <li><a href="/redoc" class="text-blue-500">/redoc (apis)</a></li>
        </ul>
        <p>Powered by <a href="https://vercel.com" target="_blank" class="text-blue-500">Vercel</a></p>
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



@app.post("/api/rc/challaninfo", tags=['Rto'])
async def get_challan_info(regn_no: str, token:str):
    url = "https://rto-challan-information-verification-india.p.rapidapi.com/api/rc/challaninfo"

    payload = {
        "regn_no": regn_no,
        "consent": "yes",
        "consent_text": "I hear by declare my consent agreement for fetching my information via AITAN Labs AP"
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



@app.post("/api/v1/rc/vehicleinfo", tags=['Rto'])
async def get_vehicle_info(reg_no: str, token:str):
    url = "https://rto-vehicle-information-verification-india.p.rapidapi.com/api/v1/rc/vehicleinfo"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": token,
        "X-RapidAPI-Host": "rto-vehicle-information-verification-india.p.rapidapi.com"
    }
    payload = {
        "reg_no": reg_no,
        "consent": 'Y',
        "consent_text": "I hear by declare my consent agreement for fetching my information via AITAN Labs AP"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise exception for 4XX and 5XX status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        # Catch any request exceptions and raise HTTPException with 500 status code
        raise HTTPException(status_code=500, detail=str(e))



@app.get('/api/v1/challan/tokens',tags=['Rto'])
def challantokens():
    data = [{"mirshadkvr19":"4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c"},{"mirshadrahman":"c054ac9b60mshd55e8424cbb5ad2p137e8djsn1e1c963c6a6f"},{"sparteck":"2ad016f13fmsh8581f9352e2defcp1535c6jsn279380adfedf"}]
    return {"status":"200","data":data}


@app.get('/api/v1/vehicleinfo/tokens',tags=['Rto'])
def vehicleinfotokens():
    data = [{"mirshadkvr19":"4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c"},{"spartck":"2ad016f13fmsh8581f9352e2defcp1535c6jsn279380adfedf"},{"mirshad":"c054ac9b60mshd55e8424cbb5ad2p137e8djsn1e1c963c6a6f"}]
    return  {"status":"200","data":data}

@app.get("/api/v1/football/matches",tags=['Football'])
async def get_football_live_stream():
    url = "https://football-live-stream-api.p.rapidapi.com/index.php"

    headers = {
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "football-live-stream-api.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch data from external API: {str(e)}")

@app.get("/api/v1/football/stream",tags=['Football'])
async def get_football_stream(id:str):
    url = "https://football-live-stream-api.p.rapidapi.com/stream.php"
    querystring = {"matchid": id}
    headers = {
        "X-RapidAPI-Key": "4c611e7488mshadd6a1b53609893p132b90jsn7af42493986c",
        "X-RapidAPI-Host": "football-live-stream-api.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Raises an exception for 4xx or 5xx status codes
        return response.json()
    except requests.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch football stream: {e}")
