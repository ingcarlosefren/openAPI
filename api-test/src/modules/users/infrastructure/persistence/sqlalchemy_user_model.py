from sqlalchemy import Date
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from src.shared.infrastructure.database import Base


class SQLAlchemyUser(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="FREE")