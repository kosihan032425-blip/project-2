import time
import sys
import random
import matplotlib.pyplot as plt


def generate_uniform_array(n, range_max=None):
    if range_max is None:
        range_max = n * 10
    step = range_max / n
    arr = set()
    i = 0
    while len(arr) < n:
        val = round(step * (i + 1) + random.uniform(-step * 0.4, step * 0.4))
        val = max(1, min(range_max * 2, val))
        arr.add(val)
        i += 1
    return sorted(arr)


def interpolation_search(arr, key):
    lo, hi = 0, len(arr) - 1
    comparisons = 0
    steps = []

    while lo <= hi and key >= arr[lo] and key <= arr[hi]:
        if lo == hi:
            comparisons += 1
            steps.append((lo, arr[lo]))
            if arr[lo] == key:
                return lo, comparisons, steps
            break

        # Interpolation formula
        pos = lo + int(((key - arr[lo]) / (arr[hi] - arr[lo])) * (hi - lo))
        comparisons += 1
        steps.append((pos, arr[pos]))

        if arr[pos] == key:
            return pos, comparisons, steps
        elif arr[pos] < key:
            lo = pos + 1
        else:
            hi = pos - 1

    comparisons += 1
    return -1, comparisons, steps


def plot_performance():
    sizes = [100, 500, 1000, 5000, 10000, 50000, 100000, 200000, 500000]
    times = []
    RUNS = 300

    print("\nRunning benchmark across different input sizes...")
    for n in sizes:
        arr = list(range(1, n * 2, 2))   # perfectly uniform
        key = arr[n // 2]
        start = time.perf_counter()
        for _ in range(RUNS):
            interpolation_search(arr, key)
        elapsed = (time.perf_counter() - start) / RUNS * 1e6
        times.append(elapsed)
        label = f"{n//1000}K" if n >= 1000 else str(n)
        print(f"  n = {n:>7,}  →  {elapsed:.3f} μs (avg over {RUNS} runs)")

    labels = [f"{n//1000}K" if n >= 1000 else str(n) for n in sizes]

    plt.figure(figsize=(10, 5))
    plt.plot(labels, times, marker='o', color='#1d9e75', linewidth=2,
             markersize=7, markerfacecolor='white', markeredgewidth=2)
    plt.fill_between(range(len(sizes)), times, alpha=0.12, color='#1d9e75')
    plt.title("Interpolation Search — Execution Time vs Input Size", fontsize=14, pad=14)
    plt.xlabel("Array size (n)", fontsize=12)
    plt.ylabel("Execution time (μs)", fontsize=12)
    plt.xticks(range(len(sizes)), labels, rotation=20)
    plt.grid(True, linestyle='--', alpha=0.4)
    plt.tight_layout()
    plt.savefig("/mnt/user-data/outputs/interpolation_search_performance.png", dpi=150)
    print("\nPerformance plot saved as 'interpolation_search_performance.png'")
    plt.show()


def main():
    print("=" * 55)
    print("   Interpolation Search — Uniformly Distributed Data")
    print("=" * 55)

    # --- Input ---
    while True:
        try:
            n = int(input("\nEnter number of elements (n): "))
            if n < 2:
                print("  Please enter n >= 2.")
                continue
            break
        except ValueError:
            print("  Invalid input. Enter an integer.")

    range_max = n * 10
    arr = generate_uniform_array(n, range_max)

    print(f"\nGenerated sorted uniform array of {n} elements:")
    if n <= 30:
        print(" ", arr)
    else:
        print(f"  [{arr[0]}, {arr[1]}, {arr[2]}, ... {arr[-3]}, {arr[-2]}, {arr[-1]}]")
    print(f"  Min: {arr[0]}   Max: {arr[-1]}")

    # --- Search ---
    while True:
        try:
            key = int(input("\nEnter the search key: "))
            break
        except ValueError:
            print("  Invalid input. Enter an integer.")

    start = time.perf_counter()
    pos, comparisons, steps = interpolation_search(arr, key)
    elapsed_us = (time.perf_counter() - start) * 1e6

    print("\n" + "-" * 45)
    print("  SEARCH RESULT")
    print("-" * 45)

    if pos != -1:
        print(f"  ✓ Key {key} found at index {pos} (value: {arr[pos]})")
    else:
        print(f"  ✗ Key {key} not found in the array")

    print(f"  Comparisons made  : {comparisons}")
    print(f"  Execution time    : {elapsed_us:.4f} μs")
    print(f"  Space complexity  : O(1)  [iterative, no extra space]")
    print(f"  Time complexity   : O(log log n) avg  |  O(n) worst case")

    print("\n  Probe sequence:")
    for i, (idx, val) in enumerate(steps, 1):
        marker = "→ FOUND" if val == key and pos != -1 else ""
        print(f"    Step {i}: index {idx}  →  value {val}  {marker}")

    # --- Performance plot ---
    plot_choice = input("\nPlot performance graph? (y/n): ").strip().lower()
    if plot_choice == 'y':
        plot_performance()

    print("\nDone.")


if __name__ == "__main__":
    main()