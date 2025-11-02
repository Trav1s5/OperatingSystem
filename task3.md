
=>USING THE OUTCOME OF TASK 1  COMPARE THE PERFORMANCE OF THE THREE ALLOCATION ALGORITHMS IN TERMS OF MEMORY UTILISATION, NO OF PROCESSES ALLOCATED AND FRAGMENTATION.
1]best fit achieved the highest memory allocation by successfully allocating all 4 processes, resulting in a 100% allocation rate. 
This indicates that Best Fit is highly effective in utilizing available memory blocks by minimizing wasted space.
In contrast, both First Fit and Worst Fit algorithms allocated only 3 out of 4 processes. Indicating the primary draw back of contiguous allocation:External Fragmentation.


2]Algorithm,Processes Successfully Allocated
Best Fit Allocation,"4 (Process 1, 2, 3, 4)"
First Fit Allocation,"3 (Process 1, 2, 3)"
Worst Fit Allocation,"3 (Process 1, 2, 3)"
based on this output best fit is the most efficient algorithm as it allocated all 4 processes successfully while first fit and worst fit only allocated 3 processes each.

3]best fit - tends to create many small fragmented holes over time as it allocates the smallest suitable block for each process, leaving behind smaller unusable fragments.
first fit - can lead to mixed-size fragmented holes since it allocates the first available block that fits
worst fit - Creates large fragmented holes as it allocates the largest available block, potentially leaving behind sizable unusable fragments.

=>WHICH ALLOCATION ALGORITHM PERFORMS THE BEST AND WHY?
4]Best fit performs the best because its allocation strategy minimizes wasted space by fitting processes into the smallest available blocks. 
Fast fit -had a faster execution
worst fit - had the most fragmented memory

=>CHANGES I WOULD MAKE:
1.I would add a compaction mechanism to reduce fragmentation.
2.Maybe by implementing a hybrid allocation that combines the strength of all algorithms.

=>HOW DO MODERN OPERATING SYSTEM DIFFER FROM CLASSIC ALLOCATION ALGORITHMS?
-Modern OS do not use best fit, first fit, or worst fit algorithms for memory allocation whereas classical algorithms rely on these methods for contiguous memory allocation thus they reduce fragmentation.
-Modern OS use advanced techniques like paging and segmentation to manage memory more efficiently.
-Modern OS use virtual memory to allow processes to use more memory than physically available, which classical algorithms do not support.