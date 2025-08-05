from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from database.orm import (getParkingPlaceAvailabilityInfoList, getIncidentInfo,
                          getRoadLinkInfoList, RoadInfoList,
                          getRoadTrafficInfoList, getRoadLinkTrafficInfoList,
                          getRoadLinkTrafficInfo, getRoadLinkCongestInfo,
                          getParkingPlaceInfoList, associatedParkingPlaceInfoList)


MODEL_MAP = {
    "getParkingPlaceAvailabilityInfoList": getParkingPlaceAvailabilityInfoList,
    "getIncidentInfo": getIncidentInfo,
    "getRoadLinkInfoList": getRoadLinkInfoList,
    "RoadInfoList": RoadInfoList,
    "getRoadTrafficInfoList": getRoadTrafficInfoList,
    "getRoadLinkTrafficInfoList": getRoadLinkTrafficInfoList,
    "getRoadLinkTrafficInfo": getRoadLinkTrafficInfo,
    "getRoadLinkCongestInfo": getRoadLinkCongestInfo,
    "getParkingPlaceInfoList": getParkingPlaceInfoList,
    "associatedParkingPlaceInfoList": associatedParkingPlaceInfoList
}

def insert_data(db: Session, model_name: str, data: list[dict]):
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


def get_all_data(db: Session, model_name: str) -> list[object]:
    """
    특정 모델의 모든 데이터를 조회합니다.
    
    :param db: SQLAlchemy 세션 객체
    :param model_name: 조회할 모델의 이름
    :return: 조회된 데이터 리스트
    """
    if model_name not in MODEL_MAP:
        raise ValueError(f"지원하지 않는 모델 이름입니다: {model_name}")
    
    model = MODEL_MAP[model_name]
    return db.query(model).all()


def get_data_by_id(db: Session, model_name: str, record_id: str) -> object | None:
    """
    특정 모델에서 ID로 데이터를 조회합니다.
    
    :param db: SQLAlchemy 세션 객체
    :param model_name: 조회할 모델의 이름
    :param record_id: 조회할 레코드의 ID
    :return: 조회된 데이터 또는 None
    """
    if model_name not in MODEL_MAP:
        raise ValueError(f"지원하지 않는 모델 이름입니다: {model_name}")
    
    model = MODEL_MAP[model_name]
    # 대부분의 모델이 routeId나 다른 ID를 primary key로 사용
    primary_key_col = list(model.__table__.primary_key.columns)[0]
    return db.query(model).filter(primary_key_col == record_id).first()


def get_paginated_data(db: Session, model_name: str, page: int = 1, page_size: int = 10) -> tuple[list[object], int]:
    """
    페이지네이션을 적용하여 데이터를 조회합니다.
    
    :param db: SQLAlchemy 세션 객체
    :param model_name: 조회할 모델의 이름
    :param page: 페이지 번호 (1부터 시작)
    :param page_size: 페이지 크기
    :return: (데이터 리스트, 전체 데이터 수) 튜플
    """
    if model_name not in MODEL_MAP:
        raise ValueError(f"지원하지 않는 모델 이름입니다: {model_name}")
    
    model = MODEL_MAP[model_name]
    
    # 전체 데이터 수 조회
    total_count = db.query(model).count()
    
    # 페이지네이션 적용하여 데이터 조회
    offset = (page - 1) * page_size
    data = db.query(model).offset(offset).limit(page_size).all()
    
    return data, total_count


def delete_all_data(db: Session, model_name: str) -> int:
    """
    특정 모델의 모든 데이터를 삭제합니다.
    
    :param db: SQLAlchemy 세션 객체
    :param model_name: 삭제할 모델의 이름
    :return: 삭제된 레코드 수
    """
    if model_name not in MODEL_MAP:
        raise ValueError(f"지원하지 않는 모델 이름입니다: {model_name}")
    
    model = MODEL_MAP[model_name]
    deleted_count = db.query(model).delete()
    db.commit()
    return deleted_count


def update_or_insert_data(db: Session, model_name: str, data: list[dict]):
    """
    데이터를 업데이트하거나 삽입합니다 (Upsert).
    기존 데이터가 있으면 업데이트하고, 없으면 새로 삽입합니다.
    
    :param db: SQLAlchemy 세션 객체
    :param model_name: 대상 모델의 이름
    :param data: 업데이트/삽입할 데이터 리스트
    """
    if model_name not in MODEL_MAP:
        raise ValueError(f"지원하지 않는 모델 이름입니다: {model_name}")

    model = MODEL_MAP[model_name]
    primary_key_col = list(model.__table__.primary_key.columns)[0]
    
    for item in data:
        # Primary key 값으로 기존 레코드 찾기
        pk_value = item.get(primary_key_col.name)
        if pk_value:
            existing_record = db.query(model).filter(primary_key_col == pk_value).first()
            
            if existing_record:
                # 기존 레코드 업데이트
                for key, value in item.items():
                    setattr(existing_record, key, value)
            else:
                # 새 레코드 삽입
                db.add(model(**item))
        else:
            # Primary key가 없으면 새 레코드 삽입
            db.add(model(**item))
    
    db.commit()


# 특정 모델에 대한 전용 함수들
def get_road_traffic_info_by_route(db: Session, route_id: str) -> list[getRoadTrafficInfoList]:
    """특정 도로의 교통 정보를 조회합니다."""
    return db.query(getRoadTrafficInfoList).filter(getRoadTrafficInfoList.routeId == route_id).all()


def get_parking_info_by_location(db: Session, lae_id: str) -> list[getParkingPlaceInfoList]:
    """특정 지역의 주차장 정보를 조회합니다."""
    return db.query(getParkingPlaceInfoList).filter(getParkingPlaceInfoList.laeId == lae_id).all()


def get_available_parking_spaces(db: Session, min_spaces: int = 1) -> list[getParkingPlaceAvailabilityInfoList]:
    """이용 가능한 주차 공간이 있는 주차장을 조회합니다."""
    return db.query(getParkingPlaceAvailabilityInfoList).filter(
        getParkingPlaceAvailabilityInfoList.avblPklotCnt >= min_spaces
    ).all()


def get_active_incidents(db: Session) -> list[getIncidentInfo]:
    """진행 중인 돌발상황을 조회합니다."""
    return db.query(getIncidentInfo).filter(getIncidentInfo.endDate.is_(None)).all()