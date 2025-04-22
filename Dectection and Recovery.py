def is_deadlock_with_recovery(processes, avail, max_need, allot):
    n = len(processes)
    work = avail[:]
    finish = [False] * n
    safe_sequence = []

    while len(safe_sequence) < n:
        progress_made = False
        for p in range(n):
            if not finish[p]:
                if all(max_need[p][j] - allot[p][j] <= work[j] for j in range(len(avail))):
                    for j in range(len(avail)):
                        work[j] += allot[p][j]
                    finish[p] = True
                    safe_sequence.append(processes[p])
                    progress_made = True
                    print(f"Process {processes[p]} can finish; Work = {work}")

        if not progress_made:
            print("Deadlock detected. Initiating recovery...")
            return recover_from_deadlock(processes, avail, max_need, allot, finish)

    print("No deadlock detected. Safe sequence is:", safe_sequence)
    return False, safe_sequence


def recover_from_deadlock(processes, avail, max_need, allot, finish):
    print("Attempting to recover from deadlock...")
    n = len(processes)

    for p in range(n):
        if not finish[p]:
            print(f"Terminating process {processes[p]} to recover resources.")
            for j in range(len(avail)):
                avail[j] += allot[p][j]
            finish[p] = True
            print(f"Resources released. New available resources: {avail}")
            return is_deadlock_with_recovery(processes, avail, max_need, allot)

    print("Recovery failed. Unable to resolve deadlock.")
    return True, []


def main():
    processes = []
    num_processes = int(input("Enter number of processes: "))
    num_resources = int(input("Enter number of resources: "))
    avail = list(map(int, input("Enter available resources: ").split()))
    max_need = []
    allot = []
    for i in range(num_processes):
        processes.append(f"P{i}")
        print(f"Process {i}:")
        max_need.append(list(map(int, input("Enter maximum resources needed: ").split())))
        allot.append(list(map(int, input("Enter allocated resources: ").split())))

    is_deadlock_with_recovery(processes, avail, max_need, allot)


if __name__ == "__main__":
    main()
