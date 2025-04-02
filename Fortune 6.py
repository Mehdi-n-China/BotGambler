import asyncio
import websockets
import json
import re
import requests
import time
import configparser
from functools import lru_cache
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@lru_cache(maxsize=100000)
def FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, third_turn, selected):
    if player > 9:
        player -= 10
    if banker > 9:
        banker -= 10
    if player_card == 0:
        player_card += 1
        return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player + 1, banker, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player + 2, banker, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player + 3, banker, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player + 4, banker, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player + 5, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player + 6, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player + 7, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player + 8, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player + 9, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
    elif banker_card == 0:
        banker_card += 1
        return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player, banker + 1, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 2, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 3, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 4, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 5, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 6, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 7, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 8, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 9, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
    elif player_card == 1:
        player_card += 1
        return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player + 1, banker, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player + 2, banker, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player + 3, banker, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player + 4, banker, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player + 5, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player + 6, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player + 7, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player + 8, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player + 9, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
    elif banker_card == 1:
        banker_card += 1
        return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player, banker + 1, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 2, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 3, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 4, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 5, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 6, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 7, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 8, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 9, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
    elif player_card == 2 and third_turn == -1:
        third_turn = 0
        if banker in (8, 9) or player in (8, 9):
            third_turn = -2
            return FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, third_turn, selected)
        elif player in (6, 7):
            return FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, third_turn, selected)
        else:
            player_card += 1
            return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player + 1, banker, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn + 1, selected) +
                    (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player + 2, banker, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn + 2, selected) +
                    (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player + 3, banker, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn + 3, selected) +
                    (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player + 4, banker, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn + 4, selected) +
                    (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player + 5, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn + 5, selected) +
                    (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player + 6, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn + 6, selected) +
                    (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player + 7, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn + 7, selected) +
                    (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player + 8, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn + 8, selected) +
                    (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player + 9, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn + 9, selected) +
                    (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn + 10, selected))
    elif banker_card == 2 and third_turn >= 0:
        if banker == 6 and third_turn in (6, 7):
            third_turn = -2
            return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player, banker + 1, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 2, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 3, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 4, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 5, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 6, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 7, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 8, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 9, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
        elif banker == 5 and third_turn in (0, 4, 5, 6, 7):
            third_turn = -2
            return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player, banker + 1, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 2, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 3, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 4, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 5, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 6, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 7, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 8, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 9, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
        elif banker == 4 and third_turn in (0, 2, 3, 4, 5, 6, 7):
            third_turn = -2
            return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player, banker + 1, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 2, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 3, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 4, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 5, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 6, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 7, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 8, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 9, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
        elif banker == 3 and third_turn in (0, 1, 2, 3, 4, 5, 6, 7, 9, 10):
            third_turn = -2
            return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player, banker + 1, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 2, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 3, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 4, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 5, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 6, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 7, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 8, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 9, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
        elif banker in (0, 1, 2):
            third_turn = -2
            return ((Total_Ace / Total_All) * FortuneHand(player_card, banker_card, player, banker + 1, Total_Ace - 1, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_2 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 2, Total_Ace, Total_2 - 1, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_3 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 3, Total_Ace, Total_2, Total_3 - 1, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_4 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 4, Total_Ace, Total_2, Total_3, Total_4 - 1, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_5 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 5, Total_Ace, Total_2, Total_3, Total_4, Total_5 - 1, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_6 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 6, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6 - 1, Total_7, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_7 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 7, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7 - 1, Total_8, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_8 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 8, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8 - 1, Total_9, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_9 / Total_All) * FortuneHand(player_card, banker_card, player, banker + 9, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9 - 1, Total_10, Total_All - 1, third_turn, selected) +
                    (Total_10 / Total_All) * FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10 - 1, Total_All - 1, third_turn, selected))
        else:
            third_turn = -2
            return FortuneHand(player_card, banker_card, player, banker, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, third_turn, selected)
    elif third_turn == -2:
        if selected == "player":
            if player == 6 and banker in (8,9) and player_card == 2 and banker_card == 2:
                return 1
            elif player == 6 and player > banker:
                return 15
            return 0
        elif selected == "banker":
            if banker == 6 and player in (8,9) and player_card == 2 and banker_card == 2:
                return 1
            elif banker == 6 and player < banker:
                return 17
            return 0

def decrement_card_count(Card):
    global Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, Card_Out
    if Card == "1" and Total_Ace > 0:
        Total_Ace -= 1
        Total_All -= 1
        Card_Out = "Ace"
        print("\nCard : Ace")
    elif Card == "2" and Total_2 > 0:
        Total_2 -= 1
        Total_All -= 1
        Card_Out = "2"
        print("\nCard : 2")
    elif Card == "3" and Total_3 > 0:
        Total_3 -= 1
        Total_All -= 1
        Card_Out = "3"
        print("\nCard : 3")
    elif Card == "4" and Total_4 > 0:
        Total_4 -= 1
        Total_All -= 1
        Card_Out = "4"
        print("\nCard : 4")
    elif Card == "5" and Total_5 > 0:
        Total_5 -= 1
        Total_All -= 1
        Card_Out = "5"
        print("\nCard : 5")
    elif Card == "6" and Total_6 > 0:
        Total_6 -= 1
        Total_All -= 1
        Card_Out = "6"
        print("\nCard : 6")
    elif Card == "7" and Total_7 > 0:
        Total_7 -= 1
        Total_All -= 1
        Card_Out = "7"
        print("\nCard : 7")
    elif Card == "8" and Total_8 > 0:
        Total_8 -= 1
        Total_All -= 1
        Card_Out = "8"
        print("\nCard : 8")
    elif Card == "9" and Total_9 > 0:
        Total_9 -= 1
        Total_All -= 1
        Card_Out = "9"
        print("\nCard : 9")
    elif Card in ("0", "J", "Q", "K") and Total_10 > 0:
        Total_10 -= 1
        Total_All -= 1
        Card_Out = "T"
        print("\nCard : T")

def reset_deck():
    global Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, bet_amt, Edge_Player, Edge_Banker
    Total_Ace = Deck_Count * 4
    Total_2 = Deck_Count * 4
    Total_3 = Deck_Count * 4
    Total_4 = Deck_Count * 4
    Total_5 = Deck_Count * 4
    Total_6 = Deck_Count * 4
    Total_7 = Deck_Count * 4
    Total_8 = Deck_Count * 4
    Total_9 = Deck_Count * 4
    Total_10 = Deck_Count * 4 * 4
    Total_All = Deck_Count * 52
    print("\nDeck has been reset")
    Edge_Player = 0
    Edge_Banker = 0
    bet_amt = 100


def get_new_seed():
    global uri
    url = "https://roobet.com/_api/pragmatic/internal/getGameConfig"

    params = {
        "isMobile": "false",
        "currency": "USD",
        "lang": "en",
        "gameId": "434"
    }

    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    connect_sid = config.get('Cookies', 'connect_sid')
    print(connect_sid)
    cookies = {
        "connect.sid": connect_sid
    }

    response = requests.get(url, params=params, cookies=cookies)
    response_data = response.json()
    print("\nFetched Game Url")
    if response.status_code == 200:
        game_url = response_data['gameURL']
    else:
        exit()

    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    print("Selenium Running")

    driver = webdriver.Chrome(options=chrome_options)

    driver.get(game_url)

    WebDriverWait(driver, 1000).until(
        lambda d: d.execute_script("return sessionStorage.getItem('PPG')") is not None
    )

    game_session_json = driver.execute_script("return sessionStorage.getItem('PPG');")

    if game_session_json:
        game_session = json.loads(game_session_json)
        jsessionid = game_session.get("JSESSIONID", "Not Found")

    uri = f"wss://gs8.pragmaticplaylive.net/game?JSESSIONID={jsessionid}&tableId=bcpirpmfpobc1910"
    print("Standby for Connect")

def ping():
    global Ping
    Ping = f"""<ping time='{time.time()}'></ping>"""

def Bets(game_id):
    global bets
    ck = time.time()
    Bet_Player = f"""<command channel="table-bcpirpmfpobc1910"> <lpbet gm="baccarat_desktop" gId="{game_id}" uId="ppc1735006715548" ck="{ck}"><bet amt="{bet_amt}" bc="22" ck="{ck}"/></lpbet></command>"""
    Bet_Banker = f'''<command channel="table-bcpirpmfpobc1910"> <lpbet gm="baccarat_desktop" gId="{game_id}" uId="ppc1735006715548" ck="{ck}"><bet amt="{bet_amt}" bc="24" ck="{ck}"/></lpbet></command>'''
    bets = {
        "Player": Bet_Player,
        "Banker": Bet_Banker,
    }


async def send_request(websocket, request_data):
    try:
        await websocket.send(request_data)
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

async def listen_for_messages():
    while True:
        async with (websockets.connect(uri) as websocket):
            print('\nWebSocket connection opened')
            global global_timer_start, percentoftotal, Edge_Player, Edge_Banker, game_in_shoe, ev
            global_timer_start = time.time()
            try:
                async for message in websocket:
                    #print(message)
                    if r'<card sc=' in message:
                        match = re.search(r'<card sc="(\S)', message)
                        if match:
                            cards = match.group(1)
                            ranks = re.findall(r'([0-9]|J|[QK])', cards)
                            for rank in ranks:
                                decrement_card_count(rank)
                            Edge_Player = FortuneHand(0, 0, 0, 0, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, -1, "player") * 100
                            Edge_Banker = FortuneHand(0, 0, 0, 0, Total_Ace, Total_2, Total_3, Total_4, Total_5, Total_6, Total_7, Total_8, Total_9, Total_10, Total_All, -1, "banker") * 100
                            percentoftotal = (Total_All / (Deck_Count * 52)) * 100
                            print(f"Odds ({percentoftotal:.2f}%)\nPlayer: {Edge_Player:.2f}\nBanker: {Edge_Banker:.2f}")
                            ping()
                            await send_request(websocket, Ping)
                    if r'<betsclosingsoon game=' in message:
                        print(f"\nRound : {game_in_shoe} EV Generated : {ev:.2f}")
                        game_id = re.search(r'game="([^"]+)"', message)
                        if game_id:
                            game_id = game_id.group(1)
                        Bets(game_id)
                        if Edge_Player > 100 and game_in_shoe <= 40:
                            global_timer_start = time.time()
                            await send_request(websocket, bets["Player"])
                            print(f"Bet Out for Player ({bet_amt})")
                            if bet_amt >= 100:
                                ev += (bet_amt*(Edge_Player-100))/100
                        if Edge_Banker > 100 and game_in_shoe <= 40:
                            global_timer_start = time.time()
                            await send_request(websocket, bets["Banker"])
                            print(f"Bet Out for Banker ({bet_amt})")
                            if bet_amt > 0:
                                ev += (bet_amt*(Edge_Banker-100))/100
                    if r'<endshuffling game=' in message:
                        game_in_shoe = 1
                        reset_deck()
                    if r'<gameresult' in message:
                        game_in_shoe += 1
                        global_timer_stop = time.time() - global_timer_start
                        if global_timer_stop >= 540:
                            get_new_seed()
                            global_timer_start = time.time()
                            break
            except websockets.ConnectionClosed as e:
                print(f"\nWebSocket connection closed: {e}")
                listen_for_messages()


if __name__ == "__main__":
    percentoftotal = 100
    Edge_Player = 0
    Edge_Banker = 0
    bet_amt = 1
    game_in_shoe = 1
    ev = 0

    Deck_Count = 8
    Total_Ace = Deck_Count * 4
    Total_2 = Deck_Count * 4
    Total_3 = Deck_Count * 4
    Total_4 = Deck_Count * 4
    Total_5 = Deck_Count * 4
    Total_6 = Deck_Count * 4
    Total_7 = Deck_Count * 4
    Total_8 = Deck_Count * 4
    Total_9 = Deck_Count * 4
    Total_10 = Deck_Count * 4 * 4
    Total_All = Deck_Count * 52

    get_new_seed()

    asyncio.get_event_loop().run_until_complete(listen_for_messages())
