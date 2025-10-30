# A program that simulates best fit ,worst fit and first fit memory allocation techniques.
#input are memory blocks and process sizes :
                     # Memory Blocks: [100, 500, 200, 300, 600]
                        # Process Sizes: [212, 417, 112, 426]


#BEST FIT ALGORITHM
def best_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i, processes_size in enumerate(processes):
        best_index = -1
        for j, block_size in enumerate(blocks):
            if block_size >= processes_size:
                if best_index == -1 or blocks[j] < blocks[best_index]:
                    best_index = j
        if best_index != -1:
            allocation[i] = best_index
            blocks[best_index] -= processes_size
    return allocation

#FIRST FIT ALGORITHM
def first_fit(blocks ,processes):
    allocation =[-1] * len(processes)
    for i , processes_size in enumerate(processes):
        for j , block_size in enumerate(blocks):
            if block_size >= processes_size:
                allocation[i] = j
                blocks[j] -= processes_size
                break
    return allocation

#WORST FIT ALGORITHM
def worst_fit(blocks, processes):
    allocation = [-1] * len(processes)
    for i, processes_size in enumerate(processes):
        worst_index = -1
        for j, block_size in enumerate(blocks):
            if block_size >= processes_size:
                if worst_index == -1 or blocks[j] > blocks[worst_index]:
                    worst_index = j
        if worst_index != -1:
            allocation[i] = worst_index
            blocks[worst_index] -= processes_size
    return allocation

def print_allocation(processes , allocation,blocks):
    for i, allocation in enumerate(allocation):
        if allocation != -1:
            print(f"Process {i+1} of size {processes[i]}KB allocated to block {allocation + 1}")
        else:
            print(f"Process {i+1} of size {processes[i]}KB not allocated")

memory_blocks = [100, 500, 200, 300, 600]
process_sizes = [212, 417, 112, 426]

# Best Fit Allocation
print("Best Fit Allocation:")
print_allocation(process_sizes , best_fit(memory_blocks.copy(), process_sizes),memory_blocks)

# First Fit Allocation
print("\nFirst Fit Allocation:")
print_allocation(process_sizes , first_fit(memory_blocks.copy(), process_sizes),memory_blocks)

# Worst Fit Allocation
print("\nWorst Fit Allocation:")
print_allocation(process_sizes , worst_fit(memory_blocks.copy(), process_sizes),memory_blocks)
