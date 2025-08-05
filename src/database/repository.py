from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database.orm import (getParkingPlaceAvailabilityInfoList,getIncidentInfo,
                          getRoadLinkInfoList,
                          getRoadTrafficInfoList, getRoadLinkTrafficInfoList,
                          getRoadLinkTrafficInfo, getRoadLinkCongestInfo,
                          getParkingPlaceInfoList )
from typing import List


MODEL_MAP = {
    "getParkingPlaceAvailabilityInfoList": getParkingPlaceAvailabilityInfoList,
    "getIncidentInfo": getIncidentInfo,
    "getRoadLinkInfoList": getRoadLinkInfoList,
    "getRoadTrafficInfoList": getRoadTrafficInfoList,
    "getRoadLinkTrafficInfoList": getRoadLinkTrafficInfoList,
    "getRoadLinkTrafficInfo": getRoadLinkTrafficInfo,
    "getRoadLinkCongestInfo": getRoadLinkCongestInfo,
    "getParkingPlaceInfoList": getParkingPlaceInfoList
}

def insert_data(db: Session, model_name: str, data: List[dict]):
    """
    데이터베이스에 데이터를 삽입합니다.
    
    :param db: SQLAlchemy 세션 객체
    :param model_name: 삽입할 모델의 이름
    :param data: 삽입할 데이터 리스트
    """
    if model_name not in MODEL_MAP:
        raise ValueError(f"지원하지 않는 모델 이름입니다: {model_name}")

    model = MODEL_MAP[model_name]
    
    for item in data:
        db.add(model(**item))
    
    db.commit()

def get