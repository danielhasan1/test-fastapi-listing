from fastapi import APIRouter, Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from fastapi_listing import FastapiListing, MetaInfo
from fastapi_listing.paginator import ListingPage
from fastapi_listing.factory import filter_factory

from app.dao.employee_dao import EmployeeDao
from app.schema.response import employee_details
from fastapi import Query, Request
from fastapi_listing.filters import generic_filters

rtr = APIRouter(prefix="")


def get_db() -> Session:
    """
    replicating sessionmaker for any fastapi app.
    anyone could be using a different way or opensource packages like fastapi-sqlalchemy
    it all comes down to a single result that is yielding a session.
    for the sake of simplicity and testing purpose I'm replicating this behaviour in this naive way.
    :return: Session
    """
    engine = create_engine(
        "mysql://root:123456@127.0.0.1:3307/employees", pool_pre_ping=1
    )
    sess = Session(bind=engine)
    return sess


emp_filter_mapper = {
    "gdr": ("Employee.gender", generic_filters.EqualityFilter),
    "bdt": ("Employee.birth_date", generic_filters.MySqlNativeDateFormateRangeFilter),
    "fnm": ("Employee.first_name", generic_filters.StringStartsWithFilter),
    "lnm": ("Employee.last_name", generic_filters.StringEndsWithFilter),
}
filter_factory.register_filter_mapper(emp_filter_mapper)


@rtr.get("/employees", response_model=ListingPage[employee_details.EmployeeListDetails])
def get_employees(request: Request, db=Depends(get_db)):
    """Global Employees Listing"""
    dao = EmployeeDao(read_db=db)
    filter = request.query_params.get("filter")
    paginator = request.query_params.get("pagination")
    return FastapiListing(
        dao=dao, pydantic_serializer=employee_details.EmployeeListDetails
    ).get_response(
        MetaInfo(
            default_srt_on="emp_no",
            filter_mapper=emp_filter_mapper,
            filter=filter,
            pagination=paginator,
        )
    )


@rtr.get(
    "/managers/{manager_id:int}/employees",
    response_model=employee_details.CustomListingPage[
        employee_details.EmployeeListDetails
    ],
)
def get_employees_by_manager_id(request: Request, manager_id: int, db=Depends(get_db)):
    """Employees list by employee manager"""
    dao = EmployeeDao(read_db=db)
    meta_info = MetaInfo(
        default_srt_on="emp_no",
        query_strategy="emp_qry_by_manager",
        manager_id=manager_id,
        allow_count_query_by_paginator=False,
    )
    resp = FastapiListing(request=request, dao=dao).get_response(meta_info)
    return resp
