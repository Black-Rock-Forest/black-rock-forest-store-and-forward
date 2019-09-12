import re
from datetime import datetime

import bcrypt
import jwt
from bcrypt import gensalt
from flask import current_app
from sqlalchemy.orm import validates

from backend.database import Base
from sqlalchemy import Column, String, DateTime, BigInteger, Float, TypeDecorator, Binary

email_regex = re.compile(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\."
                         r"[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$")


class EncryptedPassword(TypeDecorator):
    impl = Binary

    def process_bind_param(self, value, dialect):
        return bcrypt.hashpw(value, bcrypt.gensalt())

    def process_result_value(self, value, dialect):
        return value


class HashedToken(TypeDecorator):
    impl = Binary

    def process_bind_param(self, value, dialect):
        return jwt.encode(value, current_app.config['SECRET_KEY'], algorithm='HS256')

    def process_result_value(self, value, dialect):
        return value

class User(Base):
    __tablename__ = "user"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    email = Column(String(256), unique=True)
    password = Column(EncryptedPassword, nullable=False)
    auth_token = Column(HashedToken, nullable=True)

    def __str__(self):
        return f"User(id={self.id}, email={self.email})"

    @validates('email')
    def validate_email(self, key, address):
        if not email_regex.match(address):
            raise ValueError("not a valid email")
        return address

    def to_dict(self):
        return {'email': self.email}

    def valid_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password)


class Sensor(Base):
    __tablename__ = "sensor"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    device_id = Column(String, primary_key=True)
    mac_addr = Column(String)
    type = Column(String)
    location = Column(String)
    description = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, device_id, type, location, mac_addr='', description=''):
        self.device_id = device_id
        self.mac_addr = mac_addr
        self.type = type
        self.location = location
        self.description = description

    @property
    def serialize(self):
        return dict(device_id=self.device_id,
                    mac_addr=self.mac_addr,
                    type=self.type,
                    location=self.location,
                    description=self.description,
                    created_at=self.created_at)

    def __repr__(self):
        return f'<Sensor id:{self.device_id}, type:{self.net_key}>'


class SensorData(Base):
    __tablename__ = 'sensordata'
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    app_key = Column(String)
    net_key = Column(String)
    device_id = Column(String)
    field_name = Column(String)
    value = Column(Float)
    unit_string = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, app_key, net_key, device_id, field_name, value, unit_string=''):
        self.app_key = app_key
        self.net_key = net_key
        self.device_id = device_id
        self.field_name = field_name
        self.value = value
        self.unit_string = unit_string


    def __repr__(self):
        return f'<SensorData id:{self.id}, device_id:{self.device_id}, net_key:{self.net_key}>'


    @property
    def serialize(self):
        return dict(device_id=self.device_id,
                    app_key=self.app_key,
                    net_key=self.net_key,
                    field_name=self.field_name,
                    value=self.value,
                    unit=self.unit_string,
                    created_at=self.created_at)


class SensorDebug(Base):
    __tablename__ = "debug"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    device_id = Column(String)
    code = Column(String)
    message = Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, device_id, code, message):
        self.device_id = device_id
        self.code = code
        self.message = message

    def __repr__(self):
        return f'<SensorDebug id:{self.id}, device_id:{self.device_id}, code:{self.code}, message:{self.message}, created_at:{self.created_at}>'

    @property
    def serialize(self):
        return dict(device_id=self.device_id,
                    code=self.code,
                    message=self.message,
                    created_at=self.created_at)


class DebugCode(Base):
    __tablename__ = "debugcode"
    id = Column(BigInteger, autoincrement=True, primary_key=True)
    code = Column(String)
    description=Column(String)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, code, description):
        self.code = code
        self.description = description

    @property
    def serialize(self):
        return dict(code=self.code,
                    description=self.description,
                    created_at=self.created_at)

    def __repr__(self):
        return f'<SensorDebug id:{id}, code:{self.code}, description:{self.description}>'