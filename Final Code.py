import networkx as nx
import matplotlib.pyplot as plt

def is_deadlock_with_recovery(processes, avail, max_need, allot):
    n = len(processes)

    while True:
        work = avail[:]
        finish = [False] * n
        safe_sequence = []

        progress_made = True
        while progress_made:
            progress_made = False
            for p in range(n):
                if not finish[p] and all(max_need[p][j] - allot[p][j] <= work[j] for j in range(len(avail))):
                    for j in range(len(avail)):
                        work[j] += allot[p][j]
                    finish[p] = True
                    safe_sequence.append(processes[p])
                    progress_made = True
                    print(f"Process {processes[p]} can finish; Work = {work}")

        if all(finish):
            print("No deadlock detected. Safe sequence is:", safe_sequence)
            return False, safe_sequence

        # Deadlock detected
        print("Deadlock detected. Initiating recovery...")

        recovered = False
        for p in range(n):
            if not finish[p]:
                print(f"Terminating process {processes[p]} to recover resources.")
                for j in range(len(avail)):
                    avail[j] += allot[p][j]
                    allot[p][j] = 0
                finish[p] = True
                recovered = True
                print(f"Resources released. New available resources: {avail}")
                break  # Terminate one process per round

        if not recovered:
            print("Recovery failed. Unable to resolve deadlock.")
            return True, []

def draw_rag(processes, avail, max_need, allot):
    num_resources = len(avail)
    G = nx.DiGraph()

    for p in processes:
        G.add_node(p, color='blue', shape='o')

    for r in range(num_resources):
        G.add_node(f'R{r}', color='red', shape='s')

    for i, p in enumerate(processes):
        for j in range(num_resources):
            if allot[i][j] > 0:
                G.add_edge(f'R{j}', p, label=f'Alloc {allot[i][j]}')

    for i, p in enumerate(processes):
        for j in range(num_resources):
            if max_need[i][j] - allot[i][j] > 0:
                G.add_edge(p, f'R{j}', label=f'Req {max_need[i][j] - allot[i][j]}')

    pos = nx.spring_layout(G)
    node_colors = ['blue' if n in processes else 'red' for n in G.nodes]

    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=3000, font_size=10, edge_color='black')
    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

    plt.title("Resource Allocation Graph (RAG)")
    plt.show()

def main():
    try:
        num_processes = int(input("Enter the number of processes: "))
        num_resources = int(input("Enter the number of resources: "))

        avail = list(map(int, input("Enter available resources (space-separated): ").split()))

        print("\nEnter the maximum need matrix (one row per process, space-separated):")
        max_need = []
        for i in range(num_processes):
            print(f"For process P{i}:")
            max_need.append(list(map(int, input().split())))

        print("\nEnter the allocation matrix (one row per process, space-separated):")
        allot = []
        for i in range(num_processes):
            print(f"For process P{i}:")
            allot.append(list(map(int, input().split())))

        processes = [f"P{i}" for i in range(num_processes)]

        draw_rag(processes, avail[:], max_need, [row[:] for row in allot])

        deadlock, sequence = is_deadlock_with_recovery(processes, avail, max_need, allot)

        if not deadlock:
            print("System is in a safe state.")
            print("Safe sequence:", " → ".join(sequence))
        else:
            print("System was in deadlock and could not be recovered.")

    except ValueError:
        print("Error: Please enter valid numeric values.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
