from pydantic import BaseModel, Field

# 공통 페이지네이션 베이스 클래스
class PaginationRequest(BaseModel):
    """페이지네이션 공통 요청 파라미터"""
    page: int = Field(1, description="페이지 번호 (1부터 시작)", ge=1, le=9999)
    page_size: int = Field(10, description="페이지 크기", ge=1, le=100)


# OpenAPI 요청 스키마들
class ParkingPlaceAvailabilityInfoRequest(BaseModel):
    """주차장 이용가능 정보 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    laeId: str | None = Field(None, description="지방자치단체ID (선택)")


class RoadInfoRequest(BaseModel):
    """도로 정보 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")


class ParkingPlaceInfoListRequest(BaseModel):
    """주차장 정보 목록 요청"""
    serviceKey: str = Field(..., description="발급받은 키값")
    laeId: str | None = Field(None, description="지방자치단체ID (선택)")


class ParkingPlaceInfoRequest(BaseModel):
    """주차장 정보 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    laeId: str | None = Field(None, description="지방자치단체ID (선택)")


class IncidentInfoRequest(BaseModel):
    """돌발상황 정보 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    routeId: str | None = Field(None, description="도로 ID (선택)")
    linkId: str | None = Field(None, description="링크 ID (선택)")


class RoadLinkInfoListRequest(BaseModel):
    """도로 링크 정보 목록 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    routeId: str = Field(..., description="도로 ID")


class RoadTrafficInfoListRequest(BaseModel):
    """도로 교통 정보 목록 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    routeId: str | None = Field(None, description="도로 ID (선택)")


class RoadLinkTrafficInfoListRequest(BaseModel):
    """도로 링크 교통 정보 목록 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    routeId: str = Field(..., description="도로 ID")


class RoadLinkTrafficInfoRequest(BaseModel):
    """도로 링크 교통 정보 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    linkId: str = Field(..., description="링크 ID")


class RoadLinkCongestInfoRequest(BaseModel):
    """도로 링크 혼잡 정보 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    routeId: str | None = Field(None, description="도로 ID (선택)")
    linkId: str | None = Field(None, description="링크 ID (선택)")


# 페이지네이션이 필요한 요청들 (OpenAPI + 페이지네이션)
class RoadInfoPageRequest(PaginationRequest):
    """도로 정보 페이지네이션 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    # 필터링 옵션들
    roadRank: str | None = Field(None, description="도로 등급 필터")
    routeTp: str | None = Field(None, description="도로 종류 필터")


class RoadTrafficInfoPageRequest(PaginationRequest):
    """도로 교통 정보 페이지네이션 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    routeId: str | None = Field(None, description="도로 ID 필터")
    routeNm: str | None = Field(None, description="도로 이름 필터")
    congGrade: str | None = Field(None, description="혼잡 등급 필터 (0:정보없음, 1:원활, 2:지체, 3:정체)")
    min_speed: int | None = Field(None, description="최소 속도 필터", ge=0, le=300)
    max_speed: int | None = Field(None, description="최대 속도 필터", ge=0, le=300)


class ParkingPlaceInfoPageRequest(PaginationRequest):
    """주차장 정보 페이지네이션 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    laeId: str | None = Field(None, description="지방자치단체ID 필터")
    laeNm: str | None = Field(None, description="지방자치단체명 필터")
    pkplcNm: str | None = Field(None, description="주차장명 검색 (부분 일치)")
    pkplcTypeNm: str | None = Field(None, description="주차장 유형 필터")


class IncidentInfoPageRequest(PaginationRequest):
    """돌발상황 정보 페이지네이션 요청 스키마"""
    serviceKey: str = Field(..., description="발급받은 키값")
    routeId: str | None = Field(None, description="도로 ID 필터")
    restrictType: str | None = Field(None, description="제한 유형 필터")
    is_active: bool | None = Field(None, description="진행중인 돌발상황만 조회")
    start_date: str | None = Field(None, description="시작 날짜 필터 (YYYY-MM-DD)")
    end_date: str | None = Field(None, description="종료 날짜 필터 (YYYY-MM-DD)")



