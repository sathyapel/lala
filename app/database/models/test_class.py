from app.database.models.base_class import Base
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
class TestTable(Base):
    __tablename__ ="some_new_Table"

    id = mapped_column("id",String(10),primary_key=True)
    value = mapped_column("value",String(20))
    extra_value = mapped_column("some_extra_value",String(20))