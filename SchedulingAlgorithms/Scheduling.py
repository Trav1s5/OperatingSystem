# Algorithms/Scheduling.py

from typing import List, Dict


# Helper: calculate averages + throughput
def calculate_metrics(processes):
    n = len(processes)
    completed_processes = [p for p in processes if 'CompletionTime' in p]
    if len(completed_processes) == 0:
        return {
            "average_waiting_time": 0.0,
            "average_turnaround_time": 0.0,
            "throughput": 0.0
        }

    total_waiting_time = sum(p['WaitingTime'] for p in completed_processes)
    total_turnaround_time = sum(p['TurnaroundTime'] for p in completed_processes)
    first_arrival = min(p['ArrivalTime'] for p in completed_processes)
    last_completion_time = max(p['CompletionTime'] for p in completed_processes)
    makespan = last_completion_time - first_arrival

    return {
        "average_waiting_time": total_waiting_time / n,
        "average_turnaround_time": total_turnaround_time / n,
        "throughput": n / makespan if makespan > 0 else float('inf')
    }


# FCFS
def fcfs(processes: List[Dict]):
    procs = [p.copy() for p in processes]
    procs.sort(key=lambda x: (x['ArrivalTime'], x['PID']))
    time, gantt = 0, []
    for p in procs:
        if time < p['ArrivalTime']:
            time = p['ArrivalTime']
        p['StartTime'], p['CompletionTime'] = time, time + p['BurstTime']
        p['TurnaroundTime'] = p['CompletionTime'] - p['ArrivalTime']
        p['WaitingTime'] = p['TurnaroundTime'] - p['BurstTime']
        gantt.append((p['PID'], p['StartTime'], p['CompletionTime']))
        time = p['CompletionTime']
    return procs, calculate_metrics(procs), gantt


# SJF (non-preemptive)
def sjf(processes: List[Dict]):
    procs = [p.copy() for p in processes]
    time, done, gantt = 0, 0, []
    procs_dict = {p['PID']: p for p in procs}

    while done < len(procs):
        available = [p for p in procs if p.get('StartTime') is None and p['ArrivalTime'] <= time]

        if not available:
            unstarted = [p for p in procs if p.get('StartTime') is None]
            if not unstarted:
                break
            time = min(p['ArrivalTime'] for p in unstarted)
            continue

        p = min(available, key=lambda x: x['BurstTime'])

        p['StartTime'], p['CompletionTime'] = time, time + p['BurstTime']
        p['TurnaroundTime'] = p['CompletionTime'] - p['ArrivalTime']
        p['WaitingTime'] = p['TurnaroundTime'] - p['BurstTime']
        gantt.append((p['PID'], p['StartTime'], p['CompletionTime']))
        time, done = p['CompletionTime'], done + 1

    return list(procs_dict.values()), calculate_metrics(list(procs_dict.values())), gantt


# SRTF (preemptive SJF)
def srtf(processes: List[Dict]):
    procs = [p.copy() for p in processes]
    for p in procs:
        p['RemainingTime'] = p['BurstTime']

    time, done, gantt = 0, 0, []

    while done < len(procs):
        available = [p for p in procs if p['ArrivalTime'] <= time and p['RemainingTime'] > 0]

        if not available:
            remaining = [p for p in procs if p['RemainingTime'] > 0]
            if not remaining:
                break
            time = min(p['ArrivalTime'] for p in remaining)
            continue

        p = min(available, key=lambda x: x['RemainingTime'])

        if p.get('StartTime') is None:
            p['StartTime'] = time

        p['RemainingTime'] -= 1
        time += 1

        if not gantt or gantt[-1][0] != p['PID']:
            gantt.append([p['PID'], time - 1, time])
        else:
            gantt[-1][2] = time

        if p['RemainingTime'] == 0:
            p['CompletionTime'] = time
            p['TurnaroundTime'] = time - p['ArrivalTime']
            p['WaitingTime'] = p['TurnaroundTime'] - p['BurstTime']
            done += 1

    gantt_tuples = [(pid, start, end) for pid, start, end in gantt]
    return procs, calculate_metrics(procs), gantt_tuples


# Priority Scheduling (non-preemptive)
def priority_scheduling(processes: List[Dict]):
    procs = [p.copy() for p in processes]
    time, done, gantt = 0, 0, []
    procs_dict = {p['PID']: p for p in procs}

    while done < len(procs):
        available = [p for p in procs if p.get('StartTime') is None and p['ArrivalTime'] <= time]

        if not available:
            unstarted = [p for p in procs if p.get('StartTime') is None]
            if not unstarted:
                break
            time = min(p['ArrivalTime'] for p in unstarted)
            continue

        p = min(available, key=lambda x: (x['Priority'], x['ArrivalTime']))

        p['StartTime'], p['CompletionTime'] = time, time + p['BurstTime']
        p['TurnaroundTime'] = p['CompletionTime'] - p['ArrivalTime']
        p['WaitingTime'] = p['TurnaroundTime'] - p['BurstTime']
        gantt.append((p['PID'], p['StartTime'], p['CompletionTime']))
        time, done = p['CompletionTime'], done + 1

    return list(procs_dict.values()), calculate_metrics(list(procs_dict.values())), gantt