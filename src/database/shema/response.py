from pydantic import BaseModel, Field, ConfigDict
from typing import List
from datetime import datetime


# 공통 베이스 응답 스키마
class CommonBaseResponse(BaseModel):
    """공통 API 응답 헤더 정보"""
    headerCd: str | None = Field(None, description="헤더 코드")
    headerMsg: str | None = Field(None, description="헤더 메시지")
    resultCode: str | None = Field(None, description="결과 코드")
    
    model_config = ConfigDict(from_attributes=True)


# 도로 정보 관련 응답 스키마
class RoadInfoResponse(CommonBaseResponse):
    """도로 정보 응답 스키마"""
    routeId: str = Field(..., description="도로 ID")
    roadRank: str | None = Field(None, description="도로 등급")
    routeTp: str | None = Field(None, description="도로 종류")
    routeNo: str | None = Field(None, description="도로 번호")
    routeNm: str | None = Field(None, description="도로 이름")


class RoadLinkInfoResponse(CommonBaseResponse):
    """도로 링크 정보 응답 스키마"""
    routeWay: str | None = Field(None, description="도로 방향")
    routeSeq: int | None = Field(None, description="도로 순서")
    linkId: str = Field(..., description="링크 ID")
    startNodeId: str | None = Field(None, description="시작 노드 ID")
    startNodeNm: str | None = Field(None, description="시작 노드 이름")
    endNodeId: str | None = Field(None, description="끝 노드 ID")
    endNodeNm: str | None = Field(None, description="끝 노드 이름")
    linkLength: int | None = Field(None, description="링크 길이")


class RoadTrafficInfoResponse(CommonBaseResponse):
    """도로 교통 정보 응답 스키마"""
    routeId: str = Field(..., description="도로 ID")
    routeNm: str | None = Field(None, description="도로 이름")
    routeWay: str | None = Field(None, description="도로 방향")
    routeSeq: int | None = Field(None, description="도로 순서")
    linkId: str | None = Field(None, description="링크 ID")
    startNodeId: str | None = Field(None, description="시작 노드 ID")
    startNodeNm: str | None = Field(None, description="시작 노드 이름")
    endNodeId: str | None = Field(None, description="끝 노드 ID")
    endNodeNm: str | None = Field(None, description="끝 노드 이름")
    collDate: str | None = Field(None, description="수집 날짜")
    spd: int | None = Field(None, description="속도", ge=0)
    vol: int | None = Field(None, description="교통량", ge=0)
    trvlTime: int | None = Field(None, description="여행 시간", ge=0)
    linkDelayTime: int | None = Field(None, description="링크 지연 시간", ge=0)
    congGrade: str | None = Field(None, description="혼잡 등급 (0:정보없음, 1:원활, 2:지체, 3:정체)")


class RoadLinkCongestInfoResponse(CommonBaseResponse):
    """도로 링크 혼잡 정보 응답 스키마"""
    routeId: str = Field(..., description="도로 ID")
    routeNm: str | None = Field(None, description="도로 이름")
    routeWay: str | None = Field(None, description="도로 방향")
    routeSeq: int | None = Field(None, description="도로 순서")
    linkId: str | None = Field(None, description="링크 ID")
    startNodeId: str | None = Field(None, description="시작 노드 ID")
    startNodeNm: str | None = Field(None, description="시작 노드 이름")
    endNodeId: str | None = Field(None, description="끝 노드 ID")
    endNodeNm: str | None = Field(None, description="끝 노드 이름")
    collDate: str | None = Field(None, description="수집 날짜")
    spd: int | None = Field(None, description="속도", ge=0)
    vol: int | None = Field(None, description="교통량", ge=0)
    trvlTime: int | None = Field(None, description="여행 시간", ge=0)


# 돌발상황 정보 응답 스키마
class IncidentInfoResponse(CommonBaseResponse):
    """돌발상황 정보 응답 스키마"""
    routeId: str = Field(..., description="도로 ID")
    linkId: str | None = Field(None, description="표준링크 ID")
    spotId: str | None = Field(None, description="지점 ID")
    regSeq: int | None = Field(None, description="돌발상황 고유번호")
    confirmDate: str | None = Field(None, description="감지 시간")
    startDate: str | None = Field(None, description="시작 시간")
    estEndDate: str | None = Field(None, description="예상 종료 시간")
    endDate: str | None = Field(None, description="종료 시간")
    restrictType: str | None = Field(None, description="제한 유형")
    inciDesc: str | None = Field(None, description="돌발 상황 설명")
    inciplace1: str | None = Field(None, description="돌발 장소1")
    inciplace2: str | None = Field(None, description="돌발 장소2")
    coord_x: str | None = Field(None, description="좌표 X")
    coord_y: str | None = Field(None, description="좌표 Y")


# 주차장 정보 연계 지자체ID 응답 스키마
class AssociatedParkingPlaceInfoResponse(BaseModel):
    """연관 주차장 정보 응답 스키마"""
    laeId: str = Field(..., description="지방자치단체ID")
    laeNm: str | None = Field(None, description="지방자치단체명")
    
    model_config = ConfigDict(from_attributes=True)


class ParkingPlaceInfoResponse(CommonBaseResponse):
    """주차장 정보 응답 스키마"""
    laeId: str = Field(..., description="지방자치단체ID")
    laeNm: str | None = Field(None, description="지방자치단체명")
    pkplcId: str = Field(..., description="주차장ID")
    pkplcNm: str | None = Field(None, description="주차장명")
    pkplcDivNm: str | None = Field(None, description="주차장 구분")
    pkplcTypeNm: str | None = Field(None, description="주차장 유형")
    latCrdn: str | None = Field(None, description="위도")
    lonCrdn: str | None = Field(None, description="경도")
    roadNmZip: str | None = Field(None, description="도로명 우편번호")
    roadNmAddr: str | None = Field(None, description="도로명 주소")
    lotnoAddr: str | None = Field(None, description="지번 주소")
    pklotCnt: str | None = Field(None, description="주차구획 수")
    sbcmpctPklotCnt: str | None = Field(None, description="경차 주차구획 수")
    pwdbsPrvusePklotCnt: str | None = Field(None, description="장애인전용 주차구획 수")
    femalePrfncPklotCnt: str | None = Field(None, description="여성우대 주차구획 수")
    olmanPrfncPklotCnt: str | None = Field(None, description="노인우대 주차구획 수")
    evPklotCnt: str | None = Field(None, description="전기차 주차구획 수")
    lndlvDivNm: str | None = Field(None, description="급지")
    wkdayOprtStartTime: str | None = Field(None, description="평일 운영 시작")
    wkdayOprtEndTime: str | None = Field(None, description="평일 운영 종료")
    satOprtStartTime: str | None = Field(None, description="토요일 운영 시작")
    satOprtEndTime: str | None = Field(None, description="토요일 운영 종료")
    hldyOprtStartTime: str | None = Field(None, description="휴일 운영 시작")
    hldyOprtEndTime: str | None = Field(None, description="휴일 운영 종료")
    parkingBscTime: str | None = Field(None, description="기본 시간")
    parkingBscFare: str | None = Field(None, description="기본 요금")
    addUnitTime: str | None = Field(None, description="추가 단위 시간")
    addUnitFare: str | None = Field(None, description="추가 단위 요금")
    ddPktckFareAplcnTime: str | None = Field(None, description="일 주차권 적용 시간")
    ddPktckFare: str | None = Field(None, description="일 주차권 요금")
    mmCmmtktFare: str | None = Field(None, description="월 정기권 요금")


class ParkingPlaceAvailabilityInfoResponse(CommonBaseResponse):
    """주차장 이용가능 정보 응답 스키마"""
    laeId: str = Field(..., description="지방자치단체ID")
    laeNm: str | None = Field(None, description="지방자치단체명")
    pkplcId: str = Field(..., description="주차장ID")
    pkplcNm: str | None = Field(None, description="주차장명")
    pklotCnt: int | None = Field(None, description="주차구획 수", ge=0)
    avblPklotCnt: int | None = Field(None, description="가용 주차구획 수", ge=0)
    ocrnDt: str | None = Field(None, description="제공시간")


# 리스트 응답을 위한 컨테이너 스키마들
class RoadInfoListResponse(BaseModel):
    """도로 정보 목록 응답"""
    items: List[RoadInfoResponse] = Field(default_factory=list, description="도로 정보 목록")
    total_count: int = Field(0, description="전체 항목 수")
    page: int = Field(1, description="현재 페이지")
    page_size: int = Field(10, description="페이지 크기")
    
    model_config = ConfigDict(from_attributes=True)


class RoadTrafficInfoListResponse(BaseModel):
    """도로 교통 정보 목록 응답"""
    items: List[RoadTrafficInfoResponse] = Field(default_factory=list, description="도로 교통 정보 목록")
    total_count: int = Field(0, description="전체 항목 수")
    page: int = Field(1, description="현재 페이지")
    page_size: int = Field(10, description="페이지 크기")
    
    model_config = ConfigDict(from_attributes=True)


class ParkingPlaceInfoListResponse(BaseModel):
    """주차장 정보 목록 응답"""
    items: List[ParkingPlaceInfoResponse] = Field(default_factory=list, description="주차장 정보 목록")
    total_count: int = Field(0, description="전체 항목 수")
    page: int = Field(1, description="현재 페이지")
    page_size: int = Field(10, description="페이지 크기")
    
    model_config = ConfigDict(from_attributes=True)


class IncidentInfoListResponse(BaseModel):
    """돌발상황 정보 목록 응답"""
    items: List[IncidentInfoResponse] = Field(default_factory=list, description="돌발상황 정보 목록")
    total_count: int = Field(0, description="전체 항목 수")
    page: int = Field(1, description="현재 페이지")
    page_size: int = Field(10, description="페이지 크기")
    
    model_config = ConfigDict(from_attributes=True)


# API 공통 응답 래퍼
class ApiResponse(BaseModel):
    """API 공통 응답 래퍼"""
    success: bool = Field(True, description="API 호출 성공 여부")
    message: str = Field("Success", description="응답 메시지")
    data: dict | None = Field(None, description="응답 데이터")
    error_code: str | None = Field(None, description="에러 코드")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="응답 시간")
    
    model_config = ConfigDict(from_attributes=True)


# 에러 응답 스키마
class ErrorResponse(BaseModel):
    """에러 응답 스키마"""
    success: bool = Field(False, description="API 호출 성공 여부")
    message: str = Field(..., description="에러 메시지")
    error_code: str = Field(..., description="에러 코드")
    details: dict | None = Field(None, description="에러 상세 정보")
    timestamp: str = Field(default_factory=lambda: datetime.now().isoformat(), description="응답 시간")
    
    model_config = ConfigDict(from_attributes=True)


# 간소화된 응답 스키마 (단순 조회용)
class SimpleRoadInfoResponse(BaseModel):
    """간소화된 도로 정보 응답"""
    routeId: str
    routeNm: str | None = None
    roadRank: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class SimpleParkingInfoResponse(BaseModel):
    """간소화된 주차장 정보 응답"""
    pkplcId: str
    pkplcNm: str | None = None
    avblPklotCnt: int | None = None
    pklotCnt: int | None = None
    
    model_config = ConfigDict(from_attributes=True)


# 통계 및 집계 응답 스키마
class TrafficStatisticsResponse(BaseModel):
    """교통 통계 응답 스키마"""
    routeId: str = Field(..., description="도로 ID")
    routeNm: str | None = Field(None, description="도로 이름")
    avg_speed: float | None = Field(None, description="평균 속도")
    avg_volume: float | None = Field(None, description="평균 교통량")
    avg_travel_time: float | None = Field(None, description="평균 여행 시간")
    congestion_level: str | None = Field(None, description="혼잡 수준")
    last_updated: str | None = Field(None, description="최종 업데이트 시간")
    
    model_config = ConfigDict(from_attributes=True)


class ParkingStatisticsResponse(BaseModel):
    """주차장 통계 응답 스키마"""
    laeId: str = Field(..., description="지방자치단체ID")
    laeNm: str | None = Field(None, description="지방자치단체명")
    total_parking_lots: int = Field(0, description="총 주차장 수")
    total_parking_spaces: int = Field(0, description="총 주차 공간 수")
    total_available_spaces: int = Field(0, description="총 이용가능 공간 수")
    occupancy_rate: float | None = Field(None, description="점유율")
    
    model_config = ConfigDict(from_attributes=True)
