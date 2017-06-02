from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()
metadata = Model.metadata

from database.models import *
