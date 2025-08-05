from fastapi import FastAPI, HTTPException, Depends, Query
import requests
import os
from dotenv import load_dotenv
from urllib.parse import quote_plus
from sqlalchemy.orm import Session
import xml.etree.ElementTree as ET

from database.connection import get_db
from database.repository import (
    insert_data, get_all_data, get_paginated_data, 
    get_road_traffic_info_by_route, get_parking_info_by_location
)

load_dotenv()

API_URL = os.getenv("API_URL", "").strip()
SERVICE_KEY = os.getenv("SERVICE_KEY", "").strip()

app = FastAPI(
    title="경기도 교통정보 API",
    description="경기도 교통정보 및 주차장 정보 API",
    version="1.0.0"
)

# API 엔드포인트 목록
api_key = [
    'getRoadInfoList', 'getRoadLinkInfoList',
    'getRoadTrafficInfoList', 'getRoadLinkTrafficInfoList',
    'getRoadLinkTrafficInfo', 'getRoadLinkCongestInfo',
    'getIncidentInfo', 'getParkingPlaceInfoList',
    'getParkingPlaceAvailabilityInfoList'
]

# API 엔드포인트와 ORM 모델 매핑
API_MODEL_MAPPING = {
    'getRoadInfoList': 'RoadInfoList',
    'getRoadLinkInfoList': 'getRoadLinkInfoList',
    'getRoadTrafficInfoList': 'getRoadTrafficInfoList',
    'getRoadLinkTrafficInfoList': 'getRoadLinkTrafficInfoList',
    'getRoadLinkTrafficInfo': 'getRoadLinkTrafficInfo',
    'getRoadLinkCongestInfo': 'getRoadLinkCongestInfo',
    'getIncidentInfo': 'getIncidentInfo',
    'getParkingPlaceInfoList': 'getParkingPlaceInfoList',
    'getParkingPlaceAvailabilityInfoList': 'getParkingPlaceAvailabilityInfoList'
}


@app.get("/")
def health_check():
    """헬스 체크"""
    return {"status": "healthy", "message": "경기도 교통정보 API 서버가 정상 작동 중입니다."}


# =======================
# 데이터 수집 API (외부 API -> DB 저장)
# =======================

@app.post("/collect/road-info")
async def collect_road_info(db: Session = Depends(get_db)):
    """외부 API에서 도로 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[0], db)  # getRoadInfoList


@app.post("/collect/road-link-info")
async def collect_road_link_info(db: Session = Depends(get_db)):
    """외부 API에서 도로 링크 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[1], db)  # getRoadLinkInfoList


@app.post("/collect/road-traffic")
async def collect_road_traffic(db: Session = Depends(get_db)):
    """외부 API에서 도로 교통 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[2], db)  # getRoadTrafficInfoList

@app.post("/collect/road-link-traffic")
async def collect_road_link_traffic(db: Session = Depends(get_db)):
    """외부 API에서 도로 링크 교통 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[3], db)  # getRoadLinkTrafficInfoList  

@app.post("/collect/road-link-traffic-info")
async def collect_road_link_traffic_info(db: Session = Depends(get_db)):
    """외부 API에서 도로 링크 교통 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[4], db)  # getRoadLinkTrafficInfo

@app.post("/collect/road-link-congest")
async def collect_road_link_congest(db: Session = Depends(get_db)):
    """외부 API에서 도로 링크 혼잡 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[5], db)


@app.post("/collect/incident-info")
async def collect_incident_info(db: Session = Depends(get_db)):
    """외부 API에서 돌발상황 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[6], db)  # getIncidentInfo


@app.post("/collect/parking-info")
async def collect_parking_info(db: Session = Depends(get_db)):
    """외부 API에서 주차장 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[7], db)  # getParkingPlaceInfoList


@app.post("/collect/parking-availability")
async def collect_parking_availability(db: Session = Depends(get_db)):
    """외부 API에서 주차장 이용가능 정보를 수집하여 DB에 저장"""
    return await _collect_and_store_data(api_key[8], db)  # getParkingPlaceAvailabilityInfoList


@app.post("/collect/all")
async def collect_all_data(db: Session = Depends(get_db)):
    """모든 외부 API 데이터를 수집하여 DB에 저장"""
    results = []
    
    # 주요 API만 수집 (너무 많으면 시간이 오래 걸림)
    main_apis = [
        api_key[0],  # getRoadInfoList
        api_key[2],  # getRoadTrafficInfoList  
        api_key[6],  # getIncidentInfo
        api_key[7],  # getParkingPlaceInfoList
        api_key[8]   # getParkingPlaceAvailabilityInfoList
    ]
    
    for endpoint in main_apis:
        try:
            result = await _collect_and_store_data(endpoint, db)
            results.append({"endpoint": endpoint, "result": result})
        except Exception as e:
            results.append({"endpoint": endpoint, "error": str(e)})
    
    return {"message": "전체 데이터 수집 완료", "results": results}


# =======================
# 데이터 조회 API (DB -> 클라이언트)
# =======================

@app.get("/api/road-info")
def get_road_info(
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    road_rank: str | None = Query(None, description="도로 등급 필터"),
    route_tp: str | None = Query(None, description="도로 종류 필터"),
    route_nm: str | None = Query(None, description="도로명 검색 (부분 일치)"),
    db: Session = Depends(get_db)
):
    """도로 정보 목록 조회 - 다양한 필터링 옵션 지원"""
    # 기본 데이터 조회
    data, total_count = get_paginated_data(db, "RoadInfoList", page, page_size)
    
    # 클라이언트 사이드 필터링 (실제로는 DB 쿼리에서 처리하는 것이 좋음)
    filtered_data = data
    if road_rank:
        filtered_data = [item for item in filtered_data if hasattr(item, 'roadRank') and item.roadRank == road_rank]
    if route_tp:
        filtered_data = [item for item in filtered_data if hasattr(item, 'routeTp') and item.routeTp == route_tp]
    if route_nm:
        filtered_data = [item for item in filtered_data if hasattr(item, 'routeNm') and item.routeNm and route_nm in item.routeNm]
    
    return {
        "items": [
            {
                "id": item.id,
                "routeId": getattr(item, 'routeId', None),
                "routeNm": getattr(item, 'routeNm', None),
                "roadRank": getattr(item, 'roadRank', None),
                "routeTp": getattr(item, 'routeTp', None),
                "routeDesc": getattr(item, 'routeDesc', None)
            } for item in filtered_data
        ],
        "total_count": len(filtered_data),
        "original_count": total_count,
        "page": page,
        "page_size": page_size,
        "filters": {
            "road_rank": road_rank,
            "route_tp": route_tp,
            "route_nm": route_nm
        }
    }


@app.get("/api/road-traffic")
def get_road_traffic(
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    route_id: str | None = Query(None, description="도로 ID 필터"),
    route_nm: str | None = Query(None, description="도로 이름 필터"),
    cong_grade: str | None = Query(None, description="혼잡 등급 필터 (0:정보없음, 1:원활, 2:지체, 3:정체)"),
    min_speed: int | None = Query(None, description="최소 속도 필터", ge=0, le=300),
    max_speed: int | None = Query(None, description="최대 속도 필터", ge=0, le=300),
    db: Session = Depends(get_db)
):
    """도로 교통 정보 목록 조회 - 다양한 필터링 옵션 지원"""
    if route_id:
        # 특정 도로의 교통 정보만 조회
        data = get_road_traffic_info_by_route(db, route_id)
        total_count = len(data)
        # 페이지네이션 수동 적용
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        data = data[start_idx:end_idx]
    else:
        data, total_count = get_paginated_data(db, "getRoadTrafficInfoList", page, page_size)
    
    # 추가 필터링 적용
    filtered_data = data
    if route_nm:
        filtered_data = [item for item in filtered_data if hasattr(item, 'routeNm') and item.routeNm and route_nm in item.routeNm]
    if cong_grade:
        filtered_data = [item for item in filtered_data if hasattr(item, 'congGrade') and str(item.congGrade) == cong_grade]
    if min_speed is not None:
        filtered_data = [item for item in filtered_data if hasattr(item, 'spd') and item.spd and item.spd >= min_speed]
    if max_speed is not None:
        filtered_data = [item for item in filtered_data if hasattr(item, 'spd') and item.spd and item.spd <= max_speed]
    
    return {
        "items": [
            {
                "id": getattr(item, 'id', None),
                "routeId": getattr(item, 'routeId', None),
                "routeNm": getattr(item, 'routeNm', None),
                "linkId": getattr(item, 'linkId', None),
                "spd": getattr(item, 'spd', None),
                "vol": getattr(item, 'vol', None),
                "trvlTime": getattr(item, 'trvlTime', None),
                "congGrade": getattr(item, 'congGrade', None),
                "updateTime": getattr(item, 'updateTime', None)
            } for item in filtered_data
        ],
        "total_count": len(filtered_data),
        "original_count": total_count,
        "page": page,
        "page_size": page_size,
        "filters": {
            "route_id": route_id,
            "route_nm": route_nm,
            "cong_grade": cong_grade,
            "min_speed": min_speed,
            "max_speed": max_speed
        }
    }


@app.get("/api/parking-info")
def get_parking_info(
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    lae_id: str | None = Query(None, description="지방자치단체ID 필터"),
    lae_nm: str | None = Query(None, description="지방자치단체명 필터"),
    pkplc_nm: str | None = Query(None, description="주차장명 검색 (부분 일치)"),
    pkplc_type_nm: str | None = Query(None, description="주차장 유형 필터"),
    db: Session = Depends(get_db)
):
    """주차장 정보 목록 조회 - 다양한 필터링 옵션 지원"""
    if lae_id:
        # 특정 지역의 주차장 정보만 조회
        data = get_parking_info_by_location(db, lae_id)
        total_count = len(data)
        # 페이지네이션 수동 적용
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        data = data[start_idx:end_idx]
    else:
        data, total_count = get_paginated_data(db, "getParkingPlaceInfoList", page, page_size)
    
    # 추가 필터링 적용
    filtered_data = data
    if lae_nm:
        filtered_data = [item for item in filtered_data if hasattr(item, 'laeNm') and item.laeNm and lae_nm in item.laeNm]
    if pkplc_nm:
        filtered_data = [item for item in filtered_data if hasattr(item, 'pkplcNm') and item.pkplcNm and pkplc_nm in item.pkplcNm]
    if pkplc_type_nm:
        filtered_data = [item for item in filtered_data if hasattr(item, 'pkplcTypeNm') and item.pkplcTypeNm == pkplc_type_nm]
    
    return {
        "items": [
            {
                "id": getattr(item, 'id', None),
                "pkplcId": getattr(item, 'pkplcId', None),
                "pkplcNm": getattr(item, 'pkplcNm', None),
                "laeId": getattr(item, 'laeId', None),
                "laeNm": getattr(item, 'laeNm', None),
                "pkplcTypeNm": getattr(item, 'pkplcTypeNm', None),
                "addr": getattr(item, 'addr', None),
                "operTm": getattr(item, 'operTm', None),
                "totPkplcQty": getattr(item, 'totPkplcQty', None),
                "bscPkplcChrgAmt": getattr(item, 'bscPkplcChrgAmt', None)
            } for item in filtered_data
        ],
        "total_count": len(filtered_data),
        "original_count": total_count,
        "page": page,
        "page_size": page_size,
        "filters": {
            "lae_id": lae_id,
            "lae_nm": lae_nm,
            "pkplc_nm": pkplc_nm,
            "pkplc_type_nm": pkplc_type_nm
        }
    }


@app.get("/api/incident-info")
def get_incident_info(
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    route_id: str | None = Query(None, description="도로 ID 필터"),
    restrict_type: str | None = Query(None, description="제한 유형 필터"),
    is_active: bool | None = Query(None, description="진행중인 돌발상황만 조회"),
    start_date: str | None = Query(None, description="시작 날짜 필터 (YYYY-MM-DD)"),
    end_date: str | None = Query(None, description="종료 날짜 필터 (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """돌발상황 정보 목록 조회 - 다양한 필터링 옵션 지원"""
    data, total_count = get_paginated_data(db, "getIncidentInfo", page, page_size)
    
    # 필터링 적용
    filtered_data = data
    if route_id:
        filtered_data = [item for item in filtered_data if hasattr(item, 'routeId') and item.routeId == route_id]
    if restrict_type:
        filtered_data = [item for item in filtered_data if hasattr(item, 'restrictType') and item.restrictType == restrict_type]
    if is_active is not None:
        # 활성 상태 필터링 (예: endDt가 없거나 미래인 경우)
        if is_active:
            filtered_data = [item for item in filtered_data if hasattr(item, 'endDt') and (not item.endDt or item.endDt == '')]
        else:
            filtered_data = [item for item in filtered_data if hasattr(item, 'endDt') and item.endDt]
    
    return {
        "items": [
            {
                "id": getattr(item, 'id', None),
                "routeId": getattr(item, 'routeId', None),
                "routeNm": getattr(item, 'routeNm', None),
                "linkId": getattr(item, 'linkId', None),
                "restrictType": getattr(item, 'restrictType', None),
                "restrictNm": getattr(item, 'restrictNm', None),
                "incidentDesc": getattr(item, 'incidentDesc', None),
                "startDt": getattr(item, 'startDt', None),
                "endDt": getattr(item, 'endDt', None),
                "laneNm": getattr(item, 'laneNm', None)
            } for item in filtered_data
        ],
        "total_count": len(filtered_data),
        "original_count": total_count,
        "page": page,
        "page_size": page_size,
        "filters": {
            "route_id": route_id,
            "restrict_type": restrict_type,
            "is_active": is_active,
            "start_date": start_date,
            "end_date": end_date
        }
    }


@app.get("/api/parking-availability")
def get_parking_availability(
    page: int = Query(1, ge=1, description="페이지 번호"),
    page_size: int = Query(10, ge=1, le=100, description="페이지 크기"),
    min_spaces: int = Query(0, ge=0, description="최소 이용가능 공간 수"),
    max_spaces: int | None = Query(None, ge=0, description="최대 이용가능 공간 수"),
    lae_id: str | None = Query(None, description="지방자치단체ID 필터"),
    pkplc_nm: str | None = Query(None, description="주차장명 검색 (부분 일치)"),
    only_available: bool = Query(False, description="이용가능한 주차장만 조회"),
    db: Session = Depends(get_db)
):
    """주차장 이용가능 정보 조회 - 다양한 필터링 옵션 지원"""
    data, total_count = get_paginated_data(db, "getParkingPlaceAvailabilityInfoList", page, page_size)
    
    # 필터링 적용
    filtered_data = data
    
    # 최소/최대 공간 수 필터링
    if min_spaces > 0 or max_spaces is not None:
        temp_data = []
        for item in filtered_data:
            if hasattr(item, 'avblPklotCnt') and item.avblPklotCnt is not None:
                if min_spaces > 0 and item.avblPklotCnt < min_spaces:
                    continue
                if max_spaces is not None and item.avblPklotCnt > max_spaces:
                    continue
                temp_data.append(item)
        filtered_data = temp_data
    
    # 지역 필터링
    if lae_id:
        filtered_data = [item for item in filtered_data if hasattr(item, 'laeId') and item.laeId == lae_id]
    
    # 주차장명 검색
    if pkplc_nm:
        filtered_data = [item for item in filtered_data if hasattr(item, 'pkplcNm') and item.pkplcNm and pkplc_nm in item.pkplcNm]
    
    # 이용가능한 주차장만 조회
    if only_available:
        filtered_data = [item for item in filtered_data if hasattr(item, 'avblPklotCnt') and item.avblPklotCnt and item.avblPklotCnt > 0]
    
    return {
        "items": [
            {
                "id": getattr(item, 'id', None),
                "pkplcId": getattr(item, 'pkplcId', None),
                "pkplcNm": getattr(item, 'pkplcNm', None),
                "laeId": getattr(item, 'laeId', None),
                "laeNm": getattr(item, 'laeNm', None),
                "avblPklotCnt": getattr(item, 'avblPklotCnt', None),
                "totPkplcQty": getattr(item, 'totPkplcQty', None),
                "usageRate": round((1 - (getattr(item, 'avblPklotCnt', 0) / max(getattr(item, 'totPkplcQty', 1), 1))) * 100, 1) if getattr(item, 'totPkplcQty', 0) > 0 else 0,
                "ocrnDt": getattr(item, 'ocrnDt', None),
                "status": "available" if getattr(item, 'avblPklotCnt', 0) > 0 else "full"
            } for item in filtered_data
        ],
        "total_count": len(filtered_data),
        "original_count": total_count,
        "page": page,
        "page_size": page_size,
        "filters": {
            "min_spaces": min_spaces,
            "max_spaces": max_spaces,
            "lae_id": lae_id,
            "pkplc_nm": pkplc_nm,
            "only_available": only_available
        },
        "summary": {
            "available_parking_lots": len([item for item in filtered_data if getattr(item, 'avblPklotCnt', 0) > 0]),
            "full_parking_lots": len([item for item in filtered_data if getattr(item, 'avblPklotCnt', 0) == 0]),
            "total_available_spaces": sum([getattr(item, 'avblPklotCnt', 0) for item in filtered_data])
        }
    }


# =======================
# 개별 API 테스트 엔드포인트 (디버깅용)
# =======================

@app.get("/api/test/{api_endpoint}")
async def test_external_api(api_endpoint: str):
    """외부 API 호출 테스트 (DB 저장 없이)"""
    if api_endpoint not in api_key:
        raise HTTPException(status_code=404, detail=f"API 엔드포인트 '{api_endpoint}'를 찾을 수 없습니다.")
    
    if not API_URL or not SERVICE_KEY:
        raise HTTPException(status_code=500, detail="환경 변수(API_URL, SERVICE_KEY) 설정이 필요합니다.")
    
    encoded_key = quote_plus(SERVICE_KEY)
    # 당신이 원한 URL 구조: API_URL + api_endpoint + ?serviceKey=...
    full_url = f"{API_URL}{api_endpoint}?serviceKey={encoded_key}"
    
    try:
        response = requests.get(full_url, timeout=30)
        response.raise_for_status()
        
        # XML 파싱
        root = ET.fromstring(response.text)
        
        # 에러 체크
        result_code = root.findtext(".//resultCode")
        result_msg = root.findtext(".//resultMsg", "")
        
        if result_code and result_code != "00":
            return {
                "status": "error",
                "result_code": result_code,
                "result_message": result_msg,
                "url": full_url
            }
        
        # 데이터 개수 확인
        item_list = root.findall(".//itemList")
        
        return {
            "status": "success",
            "endpoint": api_endpoint,
            "url": full_url,
            "data_count": len(item_list),
            "result_code": result_code,
            "result_message": result_msg,
            "sample_data": _extract_sample_data(item_list[:2]) if item_list else None
        }
        
    except ET.ParseError as e:
        raise HTTPException(status_code=502, detail=f"XML 파싱 실패: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"API 요청 실패: {str(e)}")


# =======================
# 헬퍼 함수들
# =======================

async def _collect_and_store_data(api_endpoint: str, db: Session):
    """외부 API에서 데이터를 수집하고 DB에 저장하는 공통 함수"""
    if not API_URL or not SERVICE_KEY:
        raise HTTPException(status_code=500, detail="환경 변수(API_URL, SERVICE_KEY) 설정이 필요합니다.")
    
    # URL 구성 (당신이 원한 방식대로)
    encoded_key = quote_plus(SERVICE_KEY)
    full_url = f"{API_URL}{api_endpoint}?serviceKey={encoded_key}"
    
    try:
        response = requests.get(full_url, timeout=30)
        response.raise_for_status()
        
        # XML 파싱
        root = ET.fromstring(response.text)
        
        # 에러 체크
        result_code = root.findtext(".//resultCode")
        if result_code and result_code != "00":
            result_msg = root.findtext(".//resultMsg", "알 수 없는 오류")
            raise HTTPException(status_code=502, detail=f"API 오류 ({result_code}): {result_msg}")
        
        # 데이터 추출
        item_list = root.findall(".//itemList")
        if not item_list:
            return {
                "message": f"{api_endpoint}: 수집된 데이터가 없습니다.",
                "count": 0,
                "endpoint": api_endpoint,
                "url": full_url
            }
        
        # XML을 딕셔너리로 변환
        data = []
        for item in item_list:
            item_dict = {}
            for child in item:
                # 빈 값 처리
                value = child.text.strip() if child.text else None
                # 숫자 타입 변환 시도 (정수만)
                if value and value.isdigit():
                    value = int(value)
                item_dict[child.tag] = value
            data.append(item_dict)
        
        # DB에 저장 (ORM 모델명 가져오기)
        model_name = API_MODEL_MAPPING.get(api_endpoint, api_endpoint)
        insert_data(db, model_name, data)
        
        return {
            "message": f"{api_endpoint} 데이터 수집 및 저장 완료",
            "count": len(data),
            "endpoint": api_endpoint,
            "model": model_name,
            "url": full_url
        }
        
    except ET.ParseError as e:
        raise HTTPException(status_code=502, detail=f"XML 파싱 실패: {str(e)}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=502, detail=f"API 요청 실패: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"데이터 처리 실패: {str(e)}")


def _extract_sample_data(item_list):
    """샘플 데이터 추출 (디버깅용)"""
    sample_data = []
    for item in item_list:
        item_dict = {}
        for child in item:
            value = child.text.strip() if child.text else None
            if value and value.isdigit():
                value = int(value)
            item_dict[child.tag] = value
        sample_data.append(item_dict)
    return sample_data


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
