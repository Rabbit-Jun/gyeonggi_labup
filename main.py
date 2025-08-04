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

@app.get("/road-info")
def road_info_handler(lae_id: str = "31010"):
    if not API_URL or not SERVICE_KEY:
        raise HTTPException(status_code=500, detail="환경 변수(API_URL, SERVICE_KEY) 설정 안됨")

    encoded_key = quote_plus(SERVICE_KEY)

    full_url = (
        f"{API_URL}?"
        f"serviceKey={encoded_key}&"
        f"laeId={lae_id}&"
        f"pageNo=1&"
        f"numOfRows=10"
    )

    try:
        response = requests.get(full_url, timeout=10)
        response.raise_for_status()

        # ✅ XML 파싱
        root = ET.fromstring(response.text)
        item_list = root.findall(".//itemList")

        # ✅ 필요한 정보 추출
        result = []
        for item in item_list:
            result.append({
                "주차장명": item.findtext("pkplcNm"),
                "유형": item.findtext("pkplcTypeNm"),
                "종류": item.findtext("pkplcDivNm"),
                "주소": item.findtext("roadNmAddr"),
                "전체면수": item.findtext("pklotCnt"),
                "가용 주차구획 수": item.findtext("avblPklotCnt"),
                "제공시간": item.findtext("ocrnDt")
            })

        return {"count": len(result), "data": result}

    except ET.ParseError as parse_err:
        raise HTTPException(status_code=502, detail=f"XML 파싱 실패: {str(parse_err)}")
    except requests.exceptions.RequestException as req_err:
        raise HTTPException(status_code=502, detail=f"요청 실패: {str(req_err)}")
