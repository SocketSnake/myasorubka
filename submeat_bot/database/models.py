from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, String, ForeignKey, DateTime, func, Text, Boolean
from database.base import Base
from typing import List


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True) # Telegram ID
    name: Mapped[str] = mapped_column(String(32))
    portfolio: Mapped[str] = mapped_column(Text)
    about: Mapped[str] = mapped_column(String(256))

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)

    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    projects: Mapped[list["Project"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    desc: Mapped[str] = mapped_column(String(256), nullable=False)

    categories: Mapped[list["Project"]] = relationship(
        back_populates="category", cascade="all, delete-orphan"
    )


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    name: Mapped[str] = mapped_column(String(32), nullable=False)
    link: Mapped[str] = mapped_column(Text, nullable=False)
    desc: Mapped[str] = mapped_column(String(256), nullable=False)
    uniq: Mapped[str] = mapped_column(String(128), nullable=False)

    is_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    is_checked: Mapped[bool] = mapped_column(Boolean, default=False)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())

    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user: Mapped["User"] = relationship(back_populates="projects")
    category: Mapped["Category"] = relationship(back_populates="projects")


