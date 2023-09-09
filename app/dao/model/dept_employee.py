from sqlalchemy import CHAR, Column, Date, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class DeptEmp(Base):
    __tablename__ = "dept_emp"

    emp_no = Column(
        ForeignKey("employees.emp_no", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    dept_no = Column(
        ForeignKey("departments.dept_no", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    from_date = Column(Date, nullable=False)
    to_date = Column(Date, nullable=False)

    # department = relationship('Department')
    # employee = relationship('Employee')
