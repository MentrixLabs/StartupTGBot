from aiogram.fsm.state import State, StatesGroup

class RegisterStates(StatesGroup):
    waiting_username = State()
    waiting_email = State()
    waiting_password = State()
    confirm = State()          # опционально, для подтверждения

class LoginStates(StatesGroup):
    waiting_username = State()
    waiting_password = State()