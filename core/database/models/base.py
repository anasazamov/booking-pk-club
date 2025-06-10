from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import Integer, String, DateTime

class Base(DeclarativeBase):
    """
    Base class for all database models.
    This class uses SQLAlchemy's Declarative system to define the base model.
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    # created_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    # updated_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Automatically generate the table name based on the class name.
        """
        return f"{cls.__name__.lower()}s"
    
    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id}>"
    
    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id})"