from datetime import datetime
import time, os, re
import csv, asyncio
import a2s
import config

pdeath = r'.*?Got character ZDOID from (\w+) : 0:0'
log = config.file

async def timenow():
    now = datetime.now()
    gettime = now.strftime("%d/%m/%Y %H:%M:%S")
    return gettime

async def writecsv():
    while True:
        try:
            info = a2s.info(config.SERVER_ADDRESS)
            with open('csv/playerstats.csv', 'a', newline='') as f:
                csvup = csv.writer(f, delimiter=',')
                curtime, players = await timenow(), info.player_count
                csvup.writerow([curtime, players])
                print(curtime, players)
        except Exception as e:
            with open('csv/playerstats.csv', 'a', newline='') as f:
                csvup = csv.writer(f, delimiter=',')
                curtime, players = await timenow(), '0'
                csvup.writerow([curtime, players])
                print(curtime, e)
        await asyncio.sleep(60)

async def deathcount():
    while True:
        with open(log, encoding='utf-8', mode='r') as f:
            f.seek(0,2)
            while True:
                line = f.readline()
                if(re.search(pdeath, line)):
                    pname = re.search(pdeath, line).group(1)
                    with open('csv/deathlog.csv', 'a', newline='', encoding='utf-8') as dl:
                        curtime = await timenow()
                        deathup = csv.writer(dl, delimiter=',')
                        deathup.writerow([curtime, pname])
                        print(curtime, pname, ' has died!')
                await asyncio.sleep(0.2)

async def main():
    await asyncio.gather(deathcount(), writecsv())

asyncio.run(main())
