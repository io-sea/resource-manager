from RM_ResourceStruct import RM_ResourceStruct


print("Start Run")

struct = RM_ResourceStruct(100, 10, 1)
struct.addItemToStruct(10, 99001)
struct.addItemToStruct(10, 99002)
struct.addItemToStruct(10, 99003)
struct.addItemToStruct(10, 99004)

struct.deleteItemFromStruct(99001)
struct.deleteItemFromStruct(99003)
struct.deleteItemFromStruct(99002)
struct.printListOfItems()
print("MaxChunk: " + str(struct.getMaxChunkOfFreeSpace()))
print("Total freespace: " + str(struct.getTotalFreeSpace()))