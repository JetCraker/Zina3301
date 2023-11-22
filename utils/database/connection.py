from sqlalchemy import create_engine, Column, select, BigInteger, Boolean, String, INTEGER, LargeBinary, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from data import config

db = create_engine(url=config.DATABASE_URL)
Base = declarative_base()

Session = sessionmaker(db)
session = Session()


class Database(Base):
    __tablename__ = 'goods'
    goods_id = Column(INTEGER, Sequence('tariff_id_seq', start=1, increment=1), primary_key=True)
    user_id = Column(BigInteger, nullable=True)
    name = Column(String, nullable=True)
    quantity = Column(BigInteger, nullable=True)
    price = Column(String, nullable=True)
    photo = Column(LargeBinary)

# class SelfTariff(Base):
#     __tablename__ = 'self_tariffs'
#     tariff_id = Column(INTEGER, Sequence('tariff_id_seq', start=1, increment=1), primary_key=True)
#     admin_id = Column(BigInteger, nullable=True)
#     name = Column(String, nullable=True)
#     monthly_fee = Column(INTEGER, nullable=True)
#     minutes_limits = Column(INTEGER, nullable=True)
#     messages_limit = Column(INTEGER, nullable=True)
#     data_limit = Column(INTEGER, nullable=True)
#     social_pass = Column(Boolean, nullable=True)
#     social_platform = Column(Boolean, nullable=True)
#     photo = Column(LargeBinary, nullable=True)
#     url = Column(String, nullable=True)
#     delete_index = Column(INTEGER, nullable=True)
#
#
# class FamilyTariff(Base):
#     __tablename__ = 'family_tariffs'
#     tariff_id = Column(INTEGER, Sequence('tariff_id_seq', start=1, increment=1), primary_key=True)
#     admin_id = Column(BigInteger, nullable=True)
#     name = Column(String, nullable=True)
#     monthly_fee = Column(INTEGER, nullable=True)
#     minutes_limits = Column(INTEGER, nullable=True)
#     messages_limit = Column(INTEGER, nullable=True)
#     data_limit = Column(INTEGER, nullable=True)
#     social_pass = Column(Boolean, nullable=True)
#     social_platform = Column(Boolean, nullable=True)
#     photo = Column(LargeBinary, nullable=True)
#     url = Column(String, nullable=True)
#     delete_index = Column(INTEGER, nullable=True)
#
#
# class GadgetTariff(Base):
#     __tablename__ = 'gadget_tariffs'
#     tariff_id = Column(INTEGER, Sequence('tariff_id_seq', start=1, increment=1), primary_key=True)
#     admin_id = Column(BigInteger, nullable=True)
#     name = Column(String, nullable=True)
#     monthly_fee = Column(INTEGER, nullable=True)
#     minutes_limits = Column(INTEGER, nullable=True)
#     messages_limit = Column(INTEGER, nullable=True)
#     data_limit = Column(INTEGER, nullable=True)
#     social_pass = Column(Boolean, nullable=True)
#     social_platform = Column(Boolean, nullable=True)
#     photo = Column(LargeBinary, nullable=True)
#     url = Column(String, nullable=True)
#     delete_index = Column(INTEGER, nullable=True)


if __name__ == '__main__':
    print('start')
    Base.metadata.create_all(db)
    select = select(Database)
    users = session.query(Database).all()
    print('finish')
