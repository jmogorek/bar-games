import random
from collections import Counter

def roll_dice(n=5):
    return [random.randint(1, 6) for _ in range(n)]

def simulate_one_play(max_rolls=3, farm=True, fixed_number=None):
    if farm:
        if fixed_number is not None:
            target = fixed_number
            kept = 0
            for _ in range(max_rolls):
                needed = 5 - kept
                roll = roll_dice(needed)
                kept += sum(1 for d in roll if d == target)
                if kept == 5:
                    return True
            return False
        else:
            roll = roll_dice(5)
            counts = Counter(roll)
            target, kept = counts.most_common(1)[0]
            if kept == 5:
                return True
            for _ in range(1, max_rolls):
                needed = 5 - kept
                roll = roll_dice(needed)
                kept += sum(1 for d in roll if d == target)
                if kept == 5:
                    return True
            return False
    else:
        for _ in range(max_rolls):
            roll = roll_dice(5)
            counts = Counter(roll)
            number, count = counts.most_common(1)[0]
            if count == 5:
                if fixed_number is None or number == fixed_number:
                    return True
        return False

def simulate_until_win(max_rolls=3, farm=True, fixed_number=None):
    plays = 0
    while True:
        plays += 1
        if simulate_one_play(max_rolls=max_rolls, farm=farm, fixed_number=fixed_number):
            return plays

def run_experiments(num_experiments=10, max_rolls=3, farm=True, fixed_number=None, cost_per_play=1.0):
    lengths = []
    for _ in range(num_experiments):
        plays_needed = simulate_until_win(max_rolls=max_rolls, farm=farm, fixed_number=fixed_number)
        lengths.append(plays_needed)
    
    avg_plays = sum(lengths) / len(lengths)
    avg_cost = avg_plays * cost_per_play
    
    return {
        "num_experiments": num_experiments,
        "avg_plays_until_win": avg_plays,
        "avg_cost_until_win": avg_cost,
        "min_plays": min(lengths),
        "max_plays": max(lengths),
        "sample_runs": lengths[:20]  # peek at first 20 runs
    }

if __name__ == "__main__":
    # --- Interactive inputs ---
    max_rolls = int(input("How many rolls are allowed per game (e.g., 2 or 3)? "))
    farm_input = input("Can you farm (keep dice between rolls)? (y/n): ").strip().lower()
    farm = farm_input.startswith("y")
    
    fixed_number_input = input("Do you need a specific number (1–6)? Enter number or press Enter for 'any': ").strip()
    fixed_number = int(fixed_number_input) if fixed_number_input else None
    
    cost_per_play = float(input("How much does it cost per play ($)? "))
    pot_size = float(input("What is the pot size ($)? "))
    num_experiments = int(input("How many full 'play until win' experiments should we run? "))
    
    # --- Run simulation ---
    results = run_experiments(num_experiments=num_experiments,
                              max_rolls=max_rolls,
                              farm=farm,
                              fixed_number=fixed_number,
                              cost_per_play=cost_per_play)
    
    # --- Show results ---
    print("\n--- Simulation Results ---")
    print(f"Number of experiments: {results['num_experiments']}")
    print(f"Average plays until win: {results['avg_plays_until_win']:.2f}")
    print(f"Average cost until win: ${results['avg_cost_until_win']:.2f}")
    print(f"Minimum plays observed: {results['min_plays']}")
    print(f"Maximum plays observed: {results['max_plays']}")
    print(f"First few runs: {results['sample_runs']}")
    print(f"Pot size: ${pot_size:.2f}")
    print(f"Expected net gain per win: ${pot_size - results['avg_cost_until_win']:.2f}")
