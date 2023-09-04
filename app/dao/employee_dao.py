from typing import List

from fastapi_listing.dao import GenericDao
from app.dao.model.employee import Employee
from app.dao.model.dept_manager import DeptManager
from app.dao.model.dept_employee import DeptEmp

from sqlalchemy.orm import Query


class EmployeeDao(GenericDao):
    name = "employee"
    model = Employee

    def get_emp_ids_contain_full_name(self, full_name: str) -> list[int]:
        from sqlalchemy import func
        objs = self._read_db.query(Employee.emp_no).filter(func.concat(Employee.first_name, ' ', Employee.last_name
                                                                       ).contains(full_name)).all()
        return [obj.emp_no for obj in objs]

    # def get_employees_with_designations(self):
    #     query = self._read_db.query(Employee.emp_no, Employee.first_name, Employee.last_name, Employee.gender,
    #                                 Title.title).join(Title, Employee.emp_no == Title.emp_no)
    #     return query

    def get_employees_by_dept(self, depts: List[str]) -> Query:
        query = self._read_db.query(Employee).join(DeptEmp, Employee.emp_no == DeptEmp.emp_no
                                                   ).filter(DeptEmp.dept_no.in_(depts))
        return query

    def get_dept_by_manager(self, manager_emp_no) -> List[str]:
        objs = self._read_db.query(DeptManager.dept_no).filter(DeptManager.emp_no == manager_emp_no).all()
        return [obj.dept_no for obj in objs]