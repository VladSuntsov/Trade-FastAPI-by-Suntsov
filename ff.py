from enum import Enum
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ValidationException
from fastapi.responses import JSONResponse
from typing import List, Optional
from pydantic import *
from datetime import datetime

app = FastAPI(
    title='Trading App'
)


@app.exception_handler(ValidationException)
async def validation_exception_handler(request: Request, exc: ValidationException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()})
    )


fake_users = [
    {'id': 1, 'role': 'admin', 'name': 'Vlad'},
    {'id': 2, 'role': 'trader', 'name': 'Denis'},
    {'id': 3, 'role': 'investor', 'name': 'Alla'},
]

fake_trades = [
    {'id': 1, 'user_id': 1, 'currancy': 'BTC', 'side': 'buy', 'price': 15000, 'ammount': 2.12},
    {'id': 1, 'user_id': 2, 'currancy': 'BTC', 'side': 'sell', 'price': 16000, 'ammount': 2.12},
]


class DegreeType(Enum):
    newbie = 'newbie'
    expert = 'expert'


class Degree(BaseModel):
    id: int
    created_id: datetime
    type_degree: DegreeType


class User(BaseModel):
    id: int
    role: str
    name: str
    degree: Optional[List[Degree]] = []


@app.get('/users/{user_id}', response_model=List[User])
def get_user(user_id: int):
    return [user for user in fake_users if user.get('id') == user_id]


@app.get('/trades')
def get_trades(limit: int = 1, offset: int = 0):
    return fake_trades[offset:][:limit]


fake_users_2 = [
    {'id': 1, 'role': 'admin', 'name': 'Zack'},
    {'id': 2, 'role': 'trader', 'name': 'Lem'},
    {'id': 3, 'role': 'investor', 'name': 'Mia'},
    {'id': 4, 'role': 'investor', 'name': "Homer", 'degree': [
        {'id': 1, 'created_at': '2023-01-01T00:00:00', 'type_degree': 'expert'}
    ]},
]


@app.post('/users/user_id')
def change_user_name(user_id: int, new_name: str):
    current_user = list(filter(lambda user: user.get('id') == user_id, fake_users_2))[0]
    current_user['name'] = new_name
    return {'status': 200, 'data': current_user}


class Trade(BaseModel):
    id: int
    user_id: int
    currency: str = Field(max_length=5)
    side: str
    price: float = Field(ge=0)
    amount: float


@app.post('/trades')
def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {'status': 200, 'data': fake_trades}
