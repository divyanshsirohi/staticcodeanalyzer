from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.data.database import Base


class Repository(Base):
    __tablename__ = "repositories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    files = relationship("File", back_populates="repository")


class File(Base):
    __tablename__ = "files"
    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer, ForeignKey("repositories.id"))
    file_path = Column(String)
    loc = Column(Integer)
    repository = relationship("Repository", back_populates="files")
    functions = relationship("Function", back_populates="file")
    issues = relationship("Issue", back_populates="file")


class Function(Base):
    __tablename__ = "functions"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    name = Column(String)
    loc = Column(Integer)
    cyclomatic_complexity = Column(Integer)
    nesting_depth = Column(Integer)
    num_arguments = Column(Integer)
    file = relationship("File", back_populates="functions")


class Issue(Base):
    __tablename__ = "issues"
    id = Column(Integer, primary_key=True, index=True)
    file_id = Column(Integer, ForeignKey("files.id"))
    line_number = Column(Integer)
    code = Column(String)
    message = Column(Text)
    file = relationship("File", back_populates="issues")
