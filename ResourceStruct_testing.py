from RM_ResourceStruct import RM_ResourceStruct
from datetime import datetime
from datetime import timedelta
import time

print("Start Run")


now = datetime.now()
#time.sleep(1)
now2 = datetime.now()
final_time = now + timedelta(seconds=15)

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
final_time = final_time.strftime("%H:%M:%S")
print("Current Time =", final_time)
if now > now2:
    print("now")
if now2 > now:
    print("now2")

struct2 = RM_ResourceStruct(100, 10)

err = struct2.addItemToStruct((datetime.now() + timedelta(seconds=1)), (datetime.now() + timedelta(seconds=5)), 20, 95001)
if err == -1: print("Not enougt space")
err = struct2.addItemToStruct((datetime.now() + timedelta(seconds=1)), (datetime.now() + timedelta(seconds=5)), 10, 95002)
if err == -1: print("Not enougt space")
err = struct2.addItemToStruct((datetime.now() + timedelta(seconds=1)), (datetime.now() + timedelta(seconds=20)), 50, 95003)
if err == -1: print("Not enougt space")
struct2.printListOfItems()
print("MaxChunk: " + str(struct2.getMaxChunkOfFreeSpace()))
print("Total freespace: " + str(struct2.getTotalFreeSpace()))
time.sleep(2)
err = struct2.addItemToStruct((datetime.now() + timedelta(seconds=1)), (datetime.now() + timedelta(seconds=10)), 80, 95004)
if err == -1: print("Not enougt space")
time.sleep(5)
print("MaxChunk: " + str(struct2.getMaxChunkOfFreeSpace()))
print("Total freespace: " + str(struct2.getTotalFreeSpace()))
err = struct2.addItemToStruct((datetime.now() + timedelta(seconds=1)), (datetime.now() + timedelta(seconds=10)), 80, 95005)
if err == -1: print("Not enougt space")
struct2.printListOfItems()
print("MaxChunk: " + str(struct2.getMaxChunkOfFreeSpace()))
print("Total freespace: " + str(struct2.getTotalFreeSpace()))