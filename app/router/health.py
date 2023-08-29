from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

health_v1 = APIRouter(
    prefix="/v1/health"
)

from typing import Sequence, TypeVar, Generic, List, Dict, Union
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from typing_extensions import TypedDict


class ListingResponseType(TypedDict):
    hasNext: bool
    totalCount: int
    currentPageSize: int
    currentPageNumber: int
    data: List[Dict[str, Union[int, str, list, dict]]]

c = ListingResponseType(totalCount=1, currentPageSize=1, data=[{"a":1}, {"b":1}], currentPageNumber=1)
print(c)
T = TypeVar('T')
class Page(GenericModel,Generic[T]):
    data: Sequence[T]
    # hasNext: bool = Field(alias="hasNext")
    # currentPageSize: int = Field(alias="currentPageSize")
    # currentPageNumber: int = Field(alias="currentPageNumber")
    # totalCount: int = Field(alias="totalCount")
    # @classmethod
    # def create(cls,
    #            items: Sequence[T],
    #            ):
    #     raise ValueError
    #     return cls(data=items)

    class Config:
        arbitrary_types_allowed=True

a = [{"a":1}]

class ABC(BaseModel):
    a: bool

@health_v1.get("", response_model=Page[ABC])
def server_is_up(request: Request):
    resp =  {"a":a}
    return {"data": a}
    # return JSONResponse(
    #     {
    #         "status":"up",
    #         "service":"test-fastapi-listing",
    #         "version":"v1"
    #     }
    # )
