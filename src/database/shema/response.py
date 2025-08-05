from pydantic import BaseModel
from typing import ClassVar # 클래스 변수에 대한 타입 힌트를 제공하기 위해 사용

class ToDoSchema(BaseModel): # sqlalchmy의 ORM 모델을 Pydantic 모델로 변환, 다양한 유즈케이스 대비
    id: int
    contents: str
    is_done: bool

    model_config: ClassVar[dict] ={
        "from_attributes": True,  # Pydantic이 ORM 객체를 지원하도록 설정합니다.
        # 이 설정은 Pydantic이 SQLAlchemy 모델의 속성을 읽을 수 있게 해줍니다.
        # 이는 SQLAlchemy ORM 모델을 Pydantic 모델로 변환할 때 유용합니다.

    } # 예전에는 class Config: orm_mode = True로 설정했지만, Pydantic v2부터는 model_config를 사용합니다.
