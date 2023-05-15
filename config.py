TOKEN = '6025564381:AAE0nNtkoOrNBNstPQFexvEVdyh_U9kNlsA'
import parsing
from keyboards import *
from auxiliary_functions import *

import duckdb
import random

from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Bot, Dispatcher, executor, types, filters
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
