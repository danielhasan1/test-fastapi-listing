from typing import Optional

from fastapi_listing.strategies import QueryStrategy
from fastapi_listing.factory import strategy_factory
from fastapi import Request
from sqlalchemy.orm import Query

from app.dao.employee_dao import EmployeeDao


class EmployeesQueryByManager(QueryStrategy):
    """Context driven query strategy class"""
    def get_query(self, *, request: Optional[Request] = None, dao: EmployeeDao = None,
                  extra_context: dict = None) -> Query:
        manager = extra_context["manager_id"]
        dept_under_manager = dao.get_dept_by_manager(manager_emp_no=manager)
        query = dao.get_employees_by_dept(depts=dept_under_manager)
        return query


strategy_factory.register_strategy("emp_qry_by_manager", EmployeesQueryByManager)