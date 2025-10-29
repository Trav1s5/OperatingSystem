import random
import json
import matplotlib.pyplot as plt # <-- UNCOMMENTED FOR PLOTTING
from typing import List, Dict

# *** THIS IS THE NEW IMPORT PATH ***
# Ensure this works based on your directory structure (e.g., from Algorithms.Scheduling import ...)
from Scheduling import fcfs, sjf, srtf, priority_scheduling

# Helper function (Assuming calculate_metrics is available in the imported Scheduling module)
# If calculate_metrics is NOT imported, you must add it to the import list above.

# Pretty print function (Kept for CLI output)
def format_results(name, results, metrics, gantt):
    """Prints the results in a formatted table."""
    print(f"\n--- {name} Scheduling Results ---")
    print("PID Arrival Burst Priority Start Completion Turnaround Waiting")
    print("-" * 75)

    results.sort(key=lambda x: x['PID'])

    for p in results:
        start_time = p.get('StartTime', '-')
        completion_time = p.get('CompletionTime', '-')
        turnaround_time = p.get('TurnaroundTime', '-')
        waiting_time = p.get('WaitingTime', '-')

        print("{:<3} {:<7} {:<5} {:<8} {:<5} {:<11} {:<10} {:<7}".format(
            p['PID'], p['ArrivalTime'], p['BurstTime'], p.get('Priority', '-'), start_time, completion_time,
            turnaround_time, waiting_time))

    print("-" * 75)
    print("Metrics:")
    print("Avg Waiting Time={:.2f} Avg Turnaround Time={:.2f} Throughput={:.2f}".format(
        metrics['average_waiting_time'], metrics['average_turnaround_time'], metrics['throughput']))
    print("Gantt Chart (PID:Start->End):", " ".join([f"P{pid}:{s}->{e}" for pid, s, e in gantt]))


# Process generation and loading (from data.py)
def generate_processes(n=5, max_arrival=10, max_burst=10, max_priority=5):
    """Generate random processes"""
    processes = []
    for i in range(1, n + 1):
        processes.append({
            "PID": i,
            "ArrivalTime": random.randint(0, max_arrival),
            "BurstTime": random.randint(1, max_burst),
            "Priority": random.randint(1, max_priority)
        })
    processes.sort(key=lambda x: x['ArrivalTime'])
    return processes


def load_processes_from_file(filename):
    """Load processes from a JSON file"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: Could not load/decode file '{filename}'. Generating random processes instead.")
        return generate_processes(n=4)


def input_processes():
    """Manually input processes from keyboard"""
    processes = []
    try:
        n = int(input("Enter number of processes: "))
    except ValueError:
        print("Invalid number, defaulting to 1 process.")
        n = 1

    for i in range(1, n + 1):
        print(f"--- Input for P{i} ---")
        try:
            at = int(input(f"Arrival time of P{i}: "))
            bt = int(input(f"Burst time of P{i}: "))
            pr = int(input(f"Priority of P{i}: "))
        except ValueError:
            print("Invalid input for time/priority, defaulting to (0, 5, 2).")
            at, bt, pr = 0, 5, 2

        processes.append({"PID": i, "ArrivalTime": at, "BurstTime": bt, "Priority": pr})
    return processes


# -------------------------
# PLOTTING FUNCTIONS GO HERE
# -------------------------

def plot_gantt(gantt, title):
    """Generates and displays the Gantt chart for a single scheduling run."""
    import matplotlib.pyplot as plt # Import locally for safety

    fig, ax = plt.subplots(figsize=(10, 3))

    max_time = max(end for pid, start, end in gantt) if gantt else 0

    pids = sorted(list(set(p[0] for p in gantt)))
    pid_to_color = {pid: plt.cm.get_cmap('viridis')(i / (len(pids) + 1)) for i, pid in enumerate(pids)}

    for pid, start, end in gantt:
        color = pid_to_color[pid]
        ax.barh(y=0, width=end - start, left=start, height=0.5, color=color)
        ax.text((start + end) / 2, 0, f"P{pid}", ha="center", va="center", color="white", fontweight='bold')

    ax.set_title(title, pad=15)
    ax.set_xlabel("Time")
    ax.set_xticks(range(int(max_time) + 1))
    ax.set_yticks([])
    ax.grid(axis='x', linestyle='--')
    plt.tight_layout()
    plt.show()


def compare_algorithms(processes): # <-- REPLACING THE OLD CLI-ONLY FUNCTION
    """Compares all algorithms, prints results, and plots Gantt/Comparison charts."""
    # Note: If matplotlib fails, this function will crash.
    # For robustness, a try/except or separating CLI logic is best.

    algos = {
        "FCFS": fcfs,
        "SJF": sjf,
        "SRTF": srtf,
        "Priority": priority_scheduling
    }

    avg_waiting, avg_turnaround = {}, {}

    print("\n" + "=" * 80)
    print("Running Scheduling Algorithms and Generating Plots...")
    print("=" * 80)

    # 1. Run algorithms, print results, and plot individual Gantt charts
    for name, fn in algos.items():
        results, metrics, gantt = fn(processes)

        # Print detailed results to CLI
        format_results(name, results, metrics, gantt)

        # Store metrics for comparison plot
        avg_waiting[name] = metrics["average_waiting_time"]
        avg_turnaround[name] = metrics["average_turnaround_time"]

        # Show Gantt chart
        plot_gantt(gantt, f"{name} Scheduling Gantt Chart")

    # 2. Plot comparison bar charts
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(12, 5))

    names = list(avg_waiting.keys())
    x = range(len(names))

    # Average Waiting Time
    bars1 = ax[0].bar(x, avg_waiting.values(), color="skyblue")
    ax[0].set_title("Average Waiting Time (Lower is Better)")
    ax[0].set_xticks(x)
    ax[0].set_xticklabels(names)
    ax[0].set_ylabel("Time Units")
    ax[0].bar_label(bars1, fmt='%.2f')

    # Average Turnaround Time
    bars2 = ax[1].bar(x, avg_turnaround.values(), color="lightgreen")
    ax[1].set_title("Average Turnaround Time (Lower is Better)")
    ax[1].set_xticks(x)
    ax[1].set_xticklabels(names)
    ax[1].set_ylabel("Time Units")
    ax[1].bar_label(bars2, fmt='%.2f')

    plt.suptitle("Scheduling Algorithm Comparison", fontweight='bold')
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()


# Main function to handle input choice
def main():
    print("Choose input method:")
    print("1. Random processes (5 processes)")
    print("2. Manual input")
    print("3. Load from file (defaulting to 'json')")
    choice = input("Enter choice (1/2/3): ")

    processes = []

    if choice == "1":
        processes = generate_processes(n=5)
    elif choice == "2":
        processes = input_processes()
    elif choice == "3":
        filename = "json"
        processes = load_processes_from_file(filename)
    else:
        print("Invalid choice, defaulting to random processes.")
        processes = generate_processes(n=5)

    if not processes:
        print("No processes were loaded or generated. Exiting.")
        return

    print("\n--- Processes to be Scheduled ---")
    print("PID | AT | BT | PR")
    print("----|----|----|----")
    for p in sorted(processes, key=lambda x: x['ArrivalTime']):
        print(f"{p['PID']:<3} | {p['ArrivalTime']:<2} | {p['BurstTime']:<2} | {p['Priority']:<2}")

    # This will now call the plotting version
    compare_algorithms(processes)


if __name__ == "__main__":
    main()