from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel, Field


Base = declarative_base()  # SQLAlchemy의 선언적 베이스 클래스를 생성합니다. 이 클래스는 ORM 모델의 기본 클래스가 됩니다.


class CommonBase(Base):
    __abstract__ = True  # 이 클래스는 추상 클래스로, 실제 테이블을 생성하지 않음

    headerCd = Column(String(10))
    headerMsg = Column(String(100))
    resultCode = Column(String(10))

class RoadInfoList(CommonBase):
    __tablename__ = "road_info_list"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 primary key 추가
    routeId = Column(String(50), unique=True)  # 도로 ID (고유하지만 primary key는 아님)
    roadRank = Column(String(20))  # 도로 등급
    routeTp = Column(String(20))  # 도로 종류
    routeNo = Column(String(20))  # 도로 번호
    routeNm = Column(String(100))  # 도로 이름

    def __repr__(self):
        return f"<RoadInfoList(routeId={self.routeId}, roadRank={self.roadRank}, routeTp={self.routeTp}, routeNo={self.routeNo}, routeNm={self.routeNm})>"
    
class getRoadLinkInfoList(CommonBase):
    __tablename__ = "road_link_info_list"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 primary key 추가
    routeWay = Column(String(20))  # 도로 방향
    routeSeq = Column(Integer)  # 도로 순서
    linkId = Column(String(50), unique=True)  # 링크 ID (고유하지만 primary key는 아님)
    startNodeId = Column(String(50))  # 시작 노드 ID
    startNodeNm = Column(String(100))  # 시작 노드 이름
    endNodeId = Column(String(50))  # 끝 노드 ID
    endNodeNm = Column(String(100))  # 끝 노드 이름
    linkLength = Column(Integer)  # 링크 길이

    def __repr__(self):
        return f"<getRoadLinkInfoList(routeWay={self.routeWay}, routeSeq={self.routeSeq}, linkId={self.linkId}, startNodeId={self.startNodeId}, startNodeNm={self.startNodeNm}, endNodeId={self.endNodeId}, endNodeNm={self.endNodeNm}, linkLength={self.linkLength})>"
    
class getRoadTrafficInfoList(CommonBase):
    __tablename__ = "road_traffic_info_list"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 primary key 추가
    routeId = Column(String(50))  # 도로 ID
    routeNm = Column(String(100))  # 도로 이름
    routeWay = Column(String(20))  # 도로 방향
    routeSeq = Column(Integer)  # 도로 순서
    linkId = Column(String(50))  # 링크 ID
    startNodeId = Column(String(50))  # 시작 노드 ID
    startNodeNm = Column(String(100))  # 시작 노드 이름
    endNodeId = Column(String(50))  # 끝 노드 ID
    endNodeNm = Column(String(100))  # 끝 노드 이름
    collDate = Column(String(20))  # 수집 날짜
    spd = Column(Integer)  # 속도
    vol = Column(Integer)  # 교통량
    trvlTime = Column(Integer)  # 여행 시간
    linkDelayTime = Column(Integer)  # 링크 지연 시간
    congGrade = Column(String(20))  # 혼잡 등급

    def __repr__(self):
        return (f"<getRoadTrafficInfoList(routeId={self.routeId}, routeNm={self.routeNm}, routeWay={self.routeWay}, "
                f"routeSeq={self.routeSeq}, linkId={self.linkId}, startNodeId={self.startNodeId}, "
                f"startNodeNm={self.startNodeNm}, endNodeId={self.endNodeId}, endNodeNm={self.endNodeNm}, "
                f"collDate={self.collDate}, spd={self.spd}, vol={self.vol}, trvlTime={self.trvlTime}, "
                f"linkDelayTime={self.linkDelayTime}, congGrade={self.congGrade})>")

class getRoadLinkTrafficInfoList(CommonBase):
    __tablename__ = "road_link_traffic_info_list"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 primary key 추가
    routeId = Column(String(50))  # 도로 ID
    routeNm = Column(String(100))  # 도로 이름
    routeWay = Column(String(20))  # 도로 방향
    routeSeq = Column(Integer)  # 도로 순서
    linkId = Column(String(50))  # 링크 ID
    startNodeId = Column(String(50))  # 시작 노드 ID
    startNodeNm = Column(String(100))  # 시작 노드 이름
    endNodeId = Column(String(50))  # 끝 노드 ID
    endNodeNm = Column(String(100))  # 끝 노드 이름
    collDate = Column(String(20))  # 수집 날짜
    spd = Column(Integer)  # 속도
    vol = Column(Integer)  # 교통량
    trvlTime = Column(Integer)  # 여행 시간
    linkDelayTime = Column(Integer)  # 링크 지연 시간
    congGrade = Column(String(20))  # 혼잡 등급(0:정보없음, 1:원활, 2:지체, 3:정체)

    def __repr__(self):
        return (f"<getRoadLinkTrafficInfoList(routeId={self.routeId}, routeNm={self.routeNm}, routeWay={self.routeWay}, "
                f"routeSeq={self.routeSeq}, linkId={self.linkId}, startNodeId={self.startNodeId}, "
                f"startNodeNm={self.startNodeNm}, endNodeId={self.endNodeId}, endNodeNm={self.endNodeNm}, "
                f"collDate={self.collDate}, spd={self.spd}, vol={self.vol}, trvlTime={self.trvlTime}, "
                f"linkDelayTime={self.linkDelayTime}, congGrade={self.congGrade})>")

class getRoadLinkTrafficInfo(CommonBase):
    __tablename__ = "road_link_traffic_info"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 primary key 추가
    routeId = Column(String(50))  # 도로 ID
    routeNm = Column(String(100))  # 도로 이름
    routeWay = Column(String(20))  # 도로 방향
    routeSeq = Column(Integer)  # 도로 순서
    linkId = Column(String(50))  # 링크 ID
    startNodeId = Column(String(50))  # 시작 노드 ID
    startNodeNm = Column(String(100))  # 시작 노드 이름
    endNodeId = Column(String(50))  # 끝 노드 ID
    endNodeNm = Column(String(100))  # 끝 노드 이름
    collDate = Column(String(20))  # 수집 날짜
    spd = Column(Integer)  # 속도
    vol = Column(Integer)  # 교통량
    trvlTime = Column(Integer)  # 여행 시간
    linkDelayTime = Column(Integer)  # 링크 지연 시간
    congGrade = Column(String(20))  # 혼잡 등급(0:정보없음, 1:원활, 2:지체, 3:정체)


    def __repr__(self):
        return (f"<getRoadLinkTrafficInfo(routeId={self.routeId}, routeNm={self.routeNm}, routeWay={self.routeWay}, "
                f"routeSeq={self.routeSeq}, linkId={self.linkId}, startNodeId={self.startNodeId}, "
                f"startNodeNm={self.startNodeNm}, endNodeId={self.endNodeId}, endNodeNm={self.endNodeNm}, "
                f"collDate={self.collDate}, spd={self.spd}, vol={self.vol}, trvlTime={self.trvlTime})>")
    

class getRoadLinkCongestInfo(CommonBase):
    __tablename__ = "road_link_congest_info"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 primary key 추가
    routeId = Column(String(50))  # 도로 ID
    routeNm = Column(String(100))  # 도로 이름
    routeWay = Column(String(20))  # 도로 방향
    routeSeq = Column(Integer)  # 도로 순서
    linkId = Column(String(50))  # 링크 ID
    startNodeId = Column(String(50))  # 시작 노드 ID
    startNodeNm = Column(String(100))  # 시작 노드 이름
    endNodeId = Column(String(50))  # 끝 노드 ID
    endNodeNm = Column(String(100))  # 끝 노드 이름
    collDate = Column(String(20))  # 수집 날짜
    spd = Column(Integer)  # 속도
    vol = Column(Integer)  # 교통량
    trvlTime = Column(Integer)  # 여행 시간

    def __repr__(self):
        return (f"<getRoadLinkCongestInfo(routeId={self.routeId}, routeNm={self.routeNm}, routeWay={self.routeWay}, "
                f"routeSeq={self.routeSeq}, linkId={self.linkId}, startNodeId={self.startNodeId}, "
                f"startNodeNm={self.startNodeNm}, endNodeId={self.endNodeId}, endNodeNm={self.endNodeNm}, "
                f"collDate={self.collDate}, spd={self.spd}, vol={self.vol}, trvlTime={self.trvlTime})>")

class getIncidentInfo(CommonBase):
    __tablename__ = "incident_info"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 기본 primary key 추가
    routeId = Column(String(50))  # 도로 ID
    linkId = Column(String(50))  # 표준링크 ID
    spotId = Column(String(50))  # 지점 ID
    regSeq  = Column(Integer)  # 돌발상황 고유번호
    confirmDate = Column(String(20))  # 감지 시간
    startDate = Column(String(20))  # 시작 시간
    estEndDate = Column(String(20))  # 예상 종료 시간
    endDate = Column(String(20))  # 종료 시간
    restrictType = Column(String(20))  # 제한 유형
    inciDesc = Column(String(200))  # 돌발 상황 설명
    inciplace1 = Column(String(100))  # 돌발 장소1
    inciplace2 = Column(String(100))  # 돌발 장소2
    coord_x = Column(String(20))  # 좌표 X
    coord_y = Column(String(20))  # 좌표 Y

    def __repr__(self):
        return (f"<getIncidentInfo(routeId={self.routeId}, linkId={self.linkId}, spotId={self.spotId}, "
                f"regSeq={self.regSeq}, confirmDate={self.confirmDate}, startDate={self.startDate}, "
                f"estEndDate={self.estEndDate}, endDate={self.endDate}, restrictType={self.restrictType}, "
                f"inciDesc={self.inciDesc}, inciplace1={self.inciplace1}, inciplace2={self.inciplace2}, "
                f"coord_x={self.coord_x}, coord_y={self.coord_y})>")


class associatedParkingPlaceInfoList(Base):
    __tablename__ = "associated_parking_place_info_list"

    laeId = Column(String(20), primary_key=True)  # 지방자치단체ID
    laeNm = Column(String(50), nullable=True)  # 지방자치단체명

    def __repr__(self):
        return f"<associatedParkingPlaceInfoList(laeId={self.laeId}, laeNm={self.laeNm})>"

class getParkingPlaceInfoList(CommonBase):
    __tablename__ = "parking_place_info_list"


    laeId = Column(String(20), primary_key=True)  # 지방자치단체ID
    laeNm = Column(String(50))  # 지방자치단체명
    pkplcId = Column(String(50), primary_key=True)  # 주차장ID
    pkplcNm = Column(String(100))  # 주차장명
    pkplcDivNm = Column(String(50))  # 주차장 구분
    pkplcTypeNm = Column(String(50))  # 주차장 유형
    latCrdn = Column(String(30))  # 위도
    lonCrdn = Column(String(30))  # 경도
    roadNmZip = Column(String(10))  # 도로명 우편번호
    roadNmAddr = Column(String(200))  # 도로명 주소
    lotnoAddr = Column(String(200))  # 지번 주소
    pklotCnt = Column(String(10))  # 주차구획 수
    sbcmpctPklotCnt = Column(String(10))  # 경차 주차구획 수
    pwdbsPrvusePklotCnt = Column(String(10))  # 장애인전용 주차구획 수
    femalePrfncPklotCnt = Column(String(10))  # 여성우대 주차구획 수
    olmanPrfncPklotCnt = Column(String(10))  # 노인우대 주차구획 수
    evPklotCnt = Column(String(10))  # 전기차 주차구획 수
    lndlvDivNm = Column(String(10))  # 급지
    wkdayOprtStartTime = Column(String(10))  # 평일 운영 시작
    wkdayOprtEndTime = Column(String(10))  # 평일 운영 종료
    satOprtStartTime = Column(String(10))  # 토요일 운영 시작
    satOprtEndTime = Column(String(10))  # 토요일 운영 종료
    hldyOprtStartTime = Column(String(10))  # 휴일 운영 시작
    hldyOprtEndTime = Column(String(10))  # 휴일 운영 종료
    parkingBscTime = Column(String(10))  # 기본 시간
    parkingBscFare = Column(String(10))  # 기본 요금
    addUnitTime = Column(String(10))  # 추가 단위 시간
    addUnitFare = Column(String(10))  # 추가 단위 요금
    ddPktckFareAplcnTime = Column(String(10))  # 일 주차권 적용 시간
    ddPktckFare = Column(String(10))  # 일 주차권 요금
    mmCmmtktFare = Column(String(10))  # 월 정기권 요금

    def __repr__(self):
        return (f"<getParkingPlaceInfoList(laeId={self.laeId}, laeNm={self.laeNm}, pkplcId={self.pkplcId}, "
                f"pkplcNm={self.pkplcNm}, pkplcDivNm={self.pkplcDivNm}, pkplcTypeNm={self.pkplcTypeNm}, "
                f"latCrdn={self.latCrdn}, lonCrdn={self.lonCrdn}, roadNmZip={self.roadNmZip}, "
                f"roadNmAddr={self.roadNmAddr}, lotnoAddr={self.lotnoAddr}, pklotCnt={self.pklotCnt}, "
                f"sbcmpctPklotCnt={self.sbcmpctPklotCnt}, pwdbsPrvusePklotCnt={self.pwdbsPrvusePklotCnt}, "
                f"femalePrfncPklotCnt={self.femalePrfncPklotCnt}, olmanPrfncPklotCnt={self.olmanPrfncPklotCnt}, "
                f"evPklotCnt={self.evPklotCnt}, lndlvDivNm={self.lndlvDivNm}, wkdayOprtStartTime={self.wkdayOprtStartTime}, "
                f"wkdayOprtEndTime={self.wkdayOprtEndTime}, satOprtStartTime={self.satOprtStartTime}, "
                f"satOprtEndTime={self.satOprtEndTime}, hldyOprtStartTime={self.hldyOprtStartTime}, "
                f"hldyOprtEndTime={self.hldyOprtEndTime}, parkingBscTime={self.parkingBscTime}, "
                f"parkingBscFare={self.parkingBscFare}, addUnitTime={self.addUnitTime}, addUnitFare={self.addUnitFare}, "
                f"ddPktckFareAplcnTime={self.ddPktckFareAplcnTime}, ddPktckFare={self.ddPktckFare}, mmCmmtktFare={self.mmCmmtktFare})>")


class getParkingPlaceAvailabilityInfoList(CommonBase):
    __tablename__ = "parking_place_availability_info_list"

    laeId = Column(String(20), primary_key=True)  # 지방자치단체ID
    laeNm = Column(String(50))  # 지방자치단체명
    pkplcId = Column(String(50), primary_key=True)  # 주차장ID
    pkplcNm = Column(String(100))  # 주차장명
    pklotCnt = Column(Integer)  # 주차구획 수
    avblPklotCnt = Column(Integer)  # 가용 주차구획 수
    ocrnDt = Column(String(20))  # 제공시간

    def __repr__(self):
        return (f"<getParkingPlaceAvailabilityInfoList(laeId={self.laeId}, laeNm={self.laeNm}, "
                f"pkplcId={self.pkplcId}, pkplcNm={self.pkplcNm}, pklotCnt={self.pklotCnt}, "
                f"avblPklotCnt={self.avblPklotCnt}, ocrnDt={self.ocrnDt})>")