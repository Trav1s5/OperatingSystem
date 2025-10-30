# for this file am suppose to simulate simple paging
# by mapping logical address to physical address
# using a page map table where the page offset is 7

pageOffset = 7
pageSize = 1 << pageOffset  # 2^7 = 128 bytes

#example page map table : page number to frame number
pageMapTable = {
    0: 3,
    1: 0, #page 1 is stored in frame 0
    2: 4,
    3: 1,
    4: 2
}

def logicalToPhysical(logicalAddress):
    pageNumber = logicalAddress >> pageOffset  # logicalAddress // pageSize
    offset = logicalAddress & (pageSize - 1)   # logicalAddress % pageSize
    if pageNumber >= len(pageMapTable):
        raise ValueError("Invalid logical address: page number out of range")
    frameNumber = pageMapTable[pageNumber]
    physicalAddress = (frameNumber * pageSize) + offset
    return physicalAddress

# Example
logicalAddress = 300
physicalAddress = logicalToPhysical(logicalAddress)
print(f"Logical Address: {logicalAddress} maps to Physical Address: {physicalAddress}")