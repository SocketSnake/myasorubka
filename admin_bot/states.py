from aiogram.fsm.state import State, StatesGroup

class RegRejectedState(StatesGroup):
    waiting_for_reason = State()

class ProjSubmitRejectState(StatesGroup):
    waiting_for_reason = State()