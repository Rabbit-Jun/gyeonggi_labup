from fastapi import FastAPI, HTTPException
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
import xml.etree.ElementTree as ET

load_dotenv()

API_URL = os.getenv("API_URL", "").strip()
SERVICE_KEY = os.getenv("SERVICE_KEY", "").strip()

app = FastAPI()

api_key=['getRoadInfoList','getRoadLinkInfoList',
         'getRoadTrafficInfoList','getRoadLinkTrafficInfoList',
         'getRoadLinkTrafficInfo','getRoadLinkCongestInfo',
         'getIncidentInfo','getParkingPlaceInfoList',
         'getParkingPlaceAvailabilityInfoList']


@app.get("/getRoadInfoList")
def getRoadInfoList_handler():
    if not API_URL or not SERVICE_KEY:
        raise HTTPException(status_code=500, detail="환경 변수(API_URL, SERVICE_KEY) 설정 안됨")

    encoded_key = quote_plus(SERVICE_KEY)

    full_url = (
        f"{API_URL}?"
        f"serviceKey={encoded_key}&"
        
    )

    try:
        response = requests.get(full_url+api_key[0], timeout=10)
        response.raise_for_status()

        # XML 파싱
        root = ET.fromstring(response.text)
        item_list = root.findall(".//itemList")

        # 필요한 정보 추출
        result = []
        for item in item_list:
            result.append({
                "도로ID": item.findtext("routeId"),
                "링크 ID": item.findtext("linkId"),
                "교통량": item.findtext("vol"),
                "여행시간": item.findtext("trvlTime"),
                "구간 속도": item.findtext("spd"),
                # "가용 주차구획 수": item.findtext("avblPklotCnt"),
                # "제공시간": item.findtext("ocrnDt")
            })

        return {"count": len(result), "data": result}

    except ET.ParseError as parse_err:
        raise HTTPException(status_code=502, detail=f"XML 파싱 실패: {str(parse_err)}")
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=502, detail=f"요청 실패: {str(req_err)}")
