import copy


# --- 1. HELPER FUNCTIONS ---

def get_matrix_input(name, n, m):
    #Reads n x m matrix based on users input.
    matrix = []
    print(f"\nEnter the {name} matrix ({n} processes, {m} resources):")
    for i in range(n):
        while True:
            try:
                # Read resource values as a single line, split by space, convert to int
                row = list(map(int, input(f"P{i} for {name}: ").split()))
                if len(row) == m:
                    matrix.append(row)
                    break
                else:
                    print(f"Error: Expected {m} values, got {len(row)}. Try again.")
            except ValueError:
                print("Error: Please enter only integers separated by spaces.")
    return matrix


def is_need_met(process_index, Need , Work):
    m = len(Work) #number of resources

    #check every resource
    for j in range(m):
        #process need more than available
        if Need[process_index][j] > Work[j]:
            return False
    return True

def run_bankers_algorithm():
    print("\n--- Banker's Algorithm ---")

    try:
        num_processes = int(input("Enter number of processes (n): "))
        num_resources = int(input("Enter number of resources (m): "))
    except ValueError:
        print("Invalid input.Please enter integers only.")
        return

    Max = get_matrix_input("Max", num_processes, num_resources)
    Allocation = get_matrix_input("Allocation", num_processes, num_resources)

    while True:
        try:
            Available = list(map(int , input("Enter Available resources (m values): ").split()))
            if len(Available) == num_resources:
                break
            else:
                print(f"Error: Expected {num_resources} values, got {len(Available)}. Try again.")
        except ValueError:
            print("Error: Please enter only integers separated by spaces.")

        # NEED MATRIX CALCULATION
    Need = []
    for i in range(num_processes):
        process_need = []
        for j in range(num_resources):
            # Need = Max - Allocation
            process_need.append(Max[i][j] - Allocation[i][j])
        Need.append(process_need)

    print("1.Calculate Need Matrix")
    for row in Need:
        print(row)

    #Calculate total resources
    total_resources = [0] * num_resources
    for j in range(num_resources):
        allocated_sum = 0
        for i in range (num_processes):
            allocated_sum += Allocation[i][j]
        #total resources = allocated + available
        total_resources[j] = allocated_sum + Available[j]


    print("2.Calculate Total Resources")
    print(total_resources)

    #SAFETY ALGORITHM

    # Initialization
    Work = list(Available)  # Work starts as a copy of Available
    Finish = [False] * num_processes  # All processes start as unfinished
    safe_sequence = []
    count = 0

    # Loop until all processes have finished or no safe process can be found
    while count < num_processes:
        found = False  # Flag to track if we found ANY process in this pass

        # Search for a process i that can run
        for i in range(num_processes):
            # Check two conditions: 1. Not finished AND 2. Need can be met by Work
            if (Finish[i] == False) and is_need_met(i, Need, Work):
                # Process P_i is safe to run!
                found = True

                # Update Work: Add back resources P_i was holding (Allocation)
                for j in range(num_resources):
                    Work[j] += Allocation[i][j]

                # Mark -> finished and record the sequence
                Finish[i] = True
                safe_sequence.append(f"P{i}")
                count += 1
                # We restart the search (break the inner loop) since Work has changed
                break

                # If we made a full pass and didn't find a single process to run, it's unsafe.
        if found == False:
            break

            # --- Results ---
    print("3. System state determination")

    if count == num_processes:
        print("The system is in a SAFE STATE.")
        print(f"A Safe Sequence is: {safe_sequence}")
    else:
        print("The system is in an UNSAFE STATE.")
        print("No safe sequence could be found.")



# Execute the main function
run_bankers_algorithm()





