import datetime
import json
import asyncio
import logging
import time
import threading
import logging
from calendar import firstweekday
import pandas as pd
import numpy as np
import aiogram
from aiogram import Bot, Dispatcher, executor, types
import requests
from aiogram.types import ParseMode
from flask import Flask, request, render_template, redirect, url_for

from config import API_TOKEN

from aiogram.contrib.fsm_storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

isStart=True
app = Flask(__name__)
app.config['ENV'] = 'development'

timenow=datetime.datetime.now()
lastTime = datetime.datetime.timestamp(timenow)



# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

Dispatcher.set_current(dp)

channel_id="-1001605272630"
messageSended=False
messageOFF=None
messageON=None
ligthDisabled=False
timeEnabled=datetime.datetime.now()
lastTimeFrom=None
strNoLight=""
editedPrev=""
stop=True
currZone=0
curr=datetime.datetime.now()
stopGetReq=True

timeKnow=datetime.datetime.now()
timeOfPost=datetime.datetime.timestamp(timeKnow)

isBotStart=True

timeToNext=None
timeToNextNext=None
timeToNextNextNext=None
timeToNextNextNextNext=None
codeExecutetime=None

dick={
    1:"Сіра",
    2:"Чорна",
    0:"Біла"
}

dick2=[
    "00:00:00",
    "03:00:00",
    "06:00:00",
    "09:00:00",
    "12:00:00",
    "15:00:00",
    "18:00:00",
    "21:00:00"
]

times=[]

df = pd.read_excel("zones.xlsx", sheet_name=0)
matrix = np.delete(df.to_numpy(),0,1)

flattenMatrix=matrix.flatten()


@app.route("/")
def login():
    return "Hello World!"

@app.post("/beba")
def success():
    global timeOfPost
    global timeKnow
    global stopGetReq
    timeKnow = datetime.datetime.now()
    if stopGetReq==False:
        timeOfPost = datetime.datetime.timestamp(timeKnow)

    print("boba")
    boba = request.json.get("penis")
    print(boba)

    return "this is success"


# @dp.message_handler()
# async def echo(message: types.Message):
#     # old style:
#     # await bot.send_message(message.chat.id, message.text)
#
#     await bot.send_message(text="Beba",chat_id=channel_id)
#
#     await message.answer(message.text)




def flaskThread():
    app.run(host="0.0.0.0",port=1242)


def chop_microseconds(delta):
    return delta - datetime.timedelta(microseconds=delta.microseconds)



def formatTime(timePart):
    if int(timePart)<10:
        return f"0{timePart}"
    else:
        return timePart

# def getNextItemInDict(fMatrix,curPos,shag):
#     matrixLen=len(fMatrix)
#     if curPos+shag>matrixLen-1:
#         return fMatrix[shag-matrixLen+curPos]


def getNextItem(fMatrix,currRowCell,shag):
    matrixLen = len(fMatrix)

    if currRowCell+shag>matrixLen-1:
        #print(f"curr In Matrix with shag:{shag}",fMatrix[shag-matrixLen+currRowCell])
        return fMatrix[shag-matrixLen+currRowCell]

    #print(f"curr In Matrix with shag:{shag}", fMatrix[currRowCell+shag])
    return fMatrix[currRowCell+shag]

async def zoneTimer():
    global timeToNextNext
    global timeToNext
    global timeToNextNextNext
    global timeToNextNextNextNext
    start_time = datetime.datetime.now().strftime("%H:%M:%S")
    currDayOfWeek = datetime.datetime.now().weekday()
    currCell = int(start_time.split(":")[0]) // 3
    shag = 1
    shag2 = 2

    if currCell + shag > 7:
        shag = 7 - currCell + shag

    end_time = getNextItem(dick2, currCell, 1)
    times.append(end_time)
    # print(end_time)

    # getNextItem(flattenMatrix, (currDayOfWeek + 1) * currCell,shag)

    t1 = datetime.datetime.strptime(start_time, "%H:%M:%S")
    t2 = datetime.datetime.strptime(end_time, "%H:%M:%S")
    timeSec = round((t2 - t1).total_seconds())

    timeSec = timeSec % (24 * 3600)
    hour = timeSec // 3600
    timeSec %= 3600
    minutes = timeSec // 60
    timeSec %= 60
    seconds = timeSec



    timeToNext=f"{formatTime(hour)}:{formatTime(minutes)}:{formatTime(seconds)}"
    print(timeToNext)

    end_time = getNextItem(dick2, currCell, 2)
    times.append(end_time)

    t1 = datetime.datetime.strptime(start_time, "%H:%M:%S")
    t2 = datetime.datetime.strptime(end_time, "%H:%M:%S")
    timeSec = round((t2 - t1).total_seconds())

    timeSec = timeSec % (24 * 3600)
    hour = timeSec // 3600
    timeSec %= 3600
    minutes = timeSec // 60
    timeSec %= 60
    seconds = timeSec

    #print(f"{hour}:{minutes}:{seconds}")
    # print(getNextItem(flattenMatrix,(currDayOfWeek+1)*currCell,1))
    timeToNextNext=f"{formatTime(hour)}:{formatTime(minutes)}:{formatTime(seconds)}"
    print(timeToNextNext)

    end_time = getNextItem(dick2, currCell, 3)
    times.append(end_time)
    t1 = datetime.datetime.strptime(start_time, "%H:%M:%S")
    t2 = datetime.datetime.strptime(end_time, "%H:%M:%S")
    timeSec = round((t2 - t1).total_seconds())

    timeSec = timeSec % (24 * 3600)
    hour = timeSec // 3600
    timeSec %= 3600
    minutes = timeSec // 60
    timeSec %= 60
    seconds = timeSec

    timeToNextNextNext = f"{formatTime(hour)}:{formatTime(minutes)}:{formatTime(seconds)}"

    end_time = getNextItem(dick2, currCell, 4)
    times.append(end_time)
    t1 = datetime.datetime.strptime(start_time, "%H:%M:%S")
    t2 = datetime.datetime.strptime(end_time, "%H:%M:%S")
    timeSec = round((t2 - t1).total_seconds())

    timeSec = timeSec % (24 * 3600)
    hour = timeSec // 3600
    timeSec %= 3600
    minutes = timeSec // 60
    timeSec %= 60
    seconds = timeSec

    timeToNextNextNextNext = f"{formatTime(hour)}:{formatTime(minutes)}:{formatTime(seconds)}"

    await asyncio.sleep(1)

# async def getTimeLeft(timeStartEvent):
#     global curr
#     match curr:
#         case 0:
async def detectCurrentEventReturnString(zoneNum):

    match zoneNum:
        case 0: zoneNum = "БІЛА ЗОНА"
        case 1: zoneNum = "СІРА ЗОНА"
        case 2: zoneNum = "ЧОРНА ЗОНА"
    return zoneNum


async def timeCheck():
    global lastTime
    global messageOFF
    global messageSended
    global timenow
    global ligthDisabled
    global timeEnabled
    global messageON
    global strNoLight
    global lastTimeFrom
    global stop
    global bot
    global isBotStart
    global channel_id
    codeExecutetime=datetime.datetime.now()
    print("NOW: ", timeOfPost)

    # await bot.send_message(chat_id=channel_id, text="test bot")

    if stop == False:

        now = datetime.datetime.now().strftime("%H:%M:%S")
        currDayOfWeek = datetime.datetime.now().weekday()
        currCell = int(now.split(":")[0]) // 3

        currRowCell = currCell + currDayOfWeek * 8
        currEvent=""


        print("Today",currDayOfWeek,currCell)


        currentZone=await detectCurrentEventReturnString(flattenMatrix[currRowCell])
        currEvent=await detectCurrentEventReturnString(getNextItem(flattenMatrix,currRowCell,1))
        nextEvent=await detectCurrentEventReturnString(getNextItem(flattenMatrix,currRowCell,2))
        nextnextEvent=await detectCurrentEventReturnString(getNextItem(flattenMatrix,currRowCell,3))
        nextnextnextEventEvent=await detectCurrentEventReturnString(getNextItem(flattenMatrix,currRowCell,4))

        print("bebaaaaaaaaaaas:",timeToNextNext)
        # print(currEvent,nextEvent)
        #
        # print("Huy: ",datetime.datetime.fromtimestamp(lastTime).time())
        # timediff=None

        biba=datetime.datetime.now()
        now=datetime.datetime.timestamp(biba)



        # print("перед проверкой")
        if (isBotStart) and (bot != None):
            isBotStart = False
            await bot.send_message(chat_id=channel_id, text="test bot")


        if (now - timeOfPost > 10) and not (messageSended):
            # if bot != None:
            #     await bot.send_message(chat_id=channel_id, text="test bot begin")
            messageOFF=await bot.send_message(chat_id=channel_id,text="💔Світло вимкненно💔")

            print("penis pered nach 228")
            timediff = datetime.datetime.fromtimestamp(lastTime)-timeEnabled

            timeSec = round(timediff.total_seconds())

            day = timeSec // (24 * 3600)
            timeSec = timeSec % (24 * 3600)
            hour = timeSec // 3600
            timeSec %= 3600
            minutes = timeSec // 60
            timeSec %= 60
            seconds = timeSec

            print("penis pered centr")

            strLight = f"{day} Днів, {hour} годин, {minutes} хвилин, {round(seconds)} секунд"
            if messageON!=None:
                await bot.edit_message_text(chat_id=channel_id,message_id=messageON.message_id,text=f"Світло було з {timeEnabled.strftime('''%H:%M:%S''')} по {datetime.datetime.fromtimestamp(lastTime).strftime('''%H:%M:%S''')}\nУсього було відсутнє:\n{strLight}\n\n<a href='https://send.monobank.ua/jar/79gUJpcGRY'>До чаю</a>",parse_mode=ParseMode.HTML,disable_web_page_preview=True)

            messageSended = True
            ligthDisabled=True
            print("penis pered konec")

        print("перед проверкой 2")
        if (now-timeOfPost>10) and (messageSended):
            print("минус свет")

            timediff=biba-timenow
            timeSec=round(timediff.total_seconds())

            day = timeSec // (24 * 3600)
            timeSec = timeSec % (24 * 3600)
            hour = timeSec // 3600
            timeSec %= 3600
            minutes = timeSec // 60
            timeSec %= 60
            seconds = timeSec

            strNoLight=f"{day} Днів, {hour} годин, {minutes} хвилин, {round(seconds)} секунд"

            if messageOFF != None:
                await bot.edit_message_text(chat_id=channel_id,message_id=messageOFF.message_id,text=f"⬛⬛⬛СВІТЛО ВІДСУТНЄ⬛⬛⬛\n\n💔Останій раз світло було о {datetime.datetime.fromtimestamp(lastTime).strftime('''%H:%M:%S''')}💔 \n({strNoLight} назад) \nДо {currEvent} о {times[0]} залишилося:\n {timeToNext} \nДо {nextEvent} о {times[1]} залишилося:\n {timeToNextNext}\nДо {nextnextEvent} о {times[2]} залишилося:\n {timeToNextNextNext} \nДо {nextnextnextEventEvent} о {times[3]} залишилося:\n {timeToNextNextNextNext} \nЗараз по графіку: \n\n{currentZone}\n\n<a href='https://send.monobank.ua/jar/79gUJpcGRY'>До чаю</a>",parse_mode=ParseMode.HTML,disable_web_page_preview=True)
            print("перед проверкой 3")
        elif not (now-timeOfPost>10) and (ligthDisabled):
            ligthDisabled=False
            timeEnabled = datetime.datetime.now()
            print("Последнее включение света:",lastTime)


            diapSvet=f"з {datetime.datetime.fromtimestamp(lastTime).strftime('''%H:%M:%S''')} по {datetime.datetime.fromtimestamp(datetime.datetime.timestamp(timeEnabled)).strftime('''%H:%M:%S''')}"
            if messageOFF != None:
                await bot.edit_message_text(chat_id=channel_id,message_id=messageOFF.message_id,text=f"Світло було відсутнє {diapSvet}\nУсього не було світла:\n{strNoLight}\n\n<a href='https://send.monobank.ua/jar/79gUJpcGRY'>До чаю</a>",parse_mode=ParseMode.HTML,disable_web_page_preview=True)
            messageON=await bot.send_message(chat_id=channel_id,text="💚Світло УВІМКНУЛИ!💚")



            messageSended=False


            print("Включение света")

        elif ligthDisabled==False and messageON!=None:
            print("Редактирование света есть")

            timediff = datetime.datetime.now()-timeEnabled
            timeSec = round(timediff.total_seconds())

            day = timeSec // (24 * 3600)
            timeSec = timeSec % (24 * 3600)
            hour = timeSec // 3600
            timeSec %= 3600
            minutes = timeSec // 60
            timeSec %= 60
            seconds = timeSec


            timenow=datetime.datetime.now()
            lastTime=datetime.datetime.timestamp(timenow)


            print("Сссссс: ",datetime.datetime.fromtimestamp(lastTime).strftime('''%H:%M:%S'''))
            try:
                await bot.edit_message_text(chat_id=channel_id,message_id=messageON.message_id,text=f"🟩🟩🟩СВІТЛО Є!!!🟩🟩🟩\n\n💚Світло було увімкнено о {timeEnabled.strftime('''%H:%M:%S''')}💚\nУсього світло присутнє:\n{day} Днів, {hour} годин, {minutes} хвилин, {round(seconds)} секунд \n\nДо {currEvent} о {times[0]} залишилося:\n {timeToNext} \nДо {nextEvent} о {times[1]} залишилося:\n {timeToNextNext}\nДо {nextnextEvent} о {times[2]} залишилося:\n {timeToNextNextNext} \nДо {nextnextnextEventEvent} о {times[3]} залишилося:\n {timeToNextNextNextNext}\nЗараз по графіку:\n\n{currentZone}\n\n<a href='https://send.monobank.ua/jar/79gUJpcGRY'>До чаю</a>",parse_mode=ParseMode.HTML,disable_web_page_preview=True)
            except aiogram.utils.exceptions.MessageNotModified:
                print("not edited")

    print("конец ф-ии")
    await asyncio.sleep(10)
    print(stop)
    print("Time:", datetime.datetime.now()-codeExecutetime)

async def recursZoneTimer():
    while True:
        await zoneTimer()

async def recursTimeCheck():
    while True:
        await timeCheck()

    #await timeCheck()

def checkerTime():
    asyncio.run(timeCheck())
    while True:
        asyncio.run(timeCheck())

def funStart():
    asyncio.get_event_loop().create_task(recursZoneTimer())
    # asyncio.get_event_loop().create_task(recursTimeCheck())



if __name__ == "__main__":

    # flaskApp = threading.Thread(target=flaskThread)
    # flaskApp.start()


    # checkerTime=threading.Thread(target=checkerTime)
    # checkerTime.start()

    asyncio.get_event_loop().create_task(timeCheck())
    funStart()
    asyncio.get_event_loop().create_task(bot.send_message(chat_id=channel_id, text="test bot"))
    @dp.message_handler(commands=['req'], state="*")
    async def stopReq(message: types.Message):
        global stopGetReq
        stopGetReq = not stopGetReq
        await message.answer(text="Запросы изменены", reply=True)


    @dp.message_handler(commands=['stop'], state="*")
    async def stopBot(message: types.Message):
        global stop
        stop = True
        await message.answer(text="Бота призупинено", reply=True)


    @dp.message_handler(commands=['resume'], state="*")
    async def resumeBot(message: types.Message):
        global stop
        stop = False
        await message.answer(text="Бота відновлено", reply=True)


    @dp.message_handler(commands=['updateExcel'], state="*")
    async def updateExcel(message: types.Message):
        global stop
        stop = False
        await message.answer(text="Бота відновлено", reply=True)


    @dp.message_handler(commands=['setzone'], state="*")
    async def setZone(message: types.Message):
        global currZone
        currZone = int(message.text.split()[1])
        print(message.text)
        await message.answer(text="Зону встановлено", reply=True)


    executor.start_polling(dp, skip_updates=True)


    print("OKOKOKOKOKOKOKOKOKOKOKOKOKOKOK")

    # loop=asyncio.new_event_loop()
    # loop.create_task(timeCheck())
    # loop.run_forever()
    #loop = asyncio.get_event_loop()



    # #zoneTimer=threading.Thread(target=zoneTimer)
    #
    # timer = asyncio.get_event_loop()
    # timer.call_later(5,stop)
    # task = timer.create_task(zoneTimer())
    #
    # try:
    #     timer.run_until_complete(task)
    # except asyncio.CancelledError:
    #     pass


    #timer.create_task(zoneTimer())
    #timer.run_forever()

    #asyncio.get_event_loop().create_task(zoneTimer())



