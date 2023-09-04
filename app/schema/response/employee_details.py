from pydantic import Field, BaseModel
import enum
from datetime import date
from fastapi_listing.paginator import BaseListingPage
from typing import TypeVar, Generic

T = TypeVar("T")


class GenderEnum(enum.Enum):
    MALE = "M"
    FEMALE = "F"


class EmployeeListDetails(BaseModel):
    emp_no: int = Field(alias="empid", title="Employee ID")
    birth_date: date = Field(alias="bdt", title="Birth Date")
    first_name: str = Field(alias="fnm", title="First Name")
    last_name: str = Field(alias="lnm", title="Last Name")
    gender: GenderEnum = Field(alias="gdr", title="Gender")
    hire_date: date = Field(alias="hdt", title="Hiring Date")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CustomListingPage(BaseListingPage[T], Generic[T]):
    # hasNext: bool = Field(alias="next_page")
    currentPageNumber: int = Field(alias="page")
    # currentPageSize: int = Field(alias="page_limit")
    # totalCount: int = Field(alias="total_results")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
