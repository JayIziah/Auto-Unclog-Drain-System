import time
from water_sensor import detect_water
from drain_sensor import is_drain_stopped, is_drain_unplugged
from air_pump import push_air, return_to_start
from calc_bathtub_capacity import calculate_bathtub_capacity

# Function to calculate drain rate (baseline test) based on tub capacity and time taken to drain.
def calculate_drain_rate(tub_capacity, drain_duration):
    return float(tub_capacity / drain_duration) # Calculate the rate in liters per second


# Function to preform the baseline test for drain rate
def perform_baseline_test():
    # Ask user for the bathtub dimensions (or use default values)
    length_cm = float(input("Enter bathtub length in cm (default: 152): ") or 152)
    width_cm = float(input("Enter bathtub width in cm (default: 79): ") or 79)
    height_cm = float(input("Enter bathtop height in cm (default: 43): ") or 43)

    # Calculate bathtub capacity using imorted calc_bathtub_capacity function
    tub_capacity = calculate_bathtub_capacity(length_cm, width_cm, height_cm)
    print(f"\nBathtub capacity is approx. {tub_capacity} liters.\n")

    # Simulate drain time based on bathtub capacity (larger capacity takes longer to drain) 
    drain_duration = (tub_capacity / 100) * 10 # Assuming draining 100 liters takes 10 seconds. Adjust time proportianally.
    print(f"Simulated drain time: {drain_duration} seconds.\n")
    
    # Calculate drain rate using drain_duration
    baseline_drain_rate = calculate_drain_rate(tub_capacity, drain_duration)
    print(f"Baseline drain rate established: {baseline_drain_rate:.2f} L/s (liters per second).\n")


    return float(tub_capacity), float(baseline_drain_rate) # Making sure return type is float


# Function to check if the current drain rate is below the baseline by comparing the current drain rate with the baseline drain rate.
def is_drain_rate_below_baseline(current_drain_rate, baseline_drain_rate):  
    return current_drain_rate < (baseline_drain_rate * 0.8)  # Returns True if current rate is below 80% of the baseline rate.


# Function to simulate drain compressions - unclogging process with three compressions.
def drain_compression():
    print("Starting drain compression...\n")
    for push in range(3):  # Perform 3 air pushes
        print(f"Push {push+1}")
        push_air()  # Simulate air pushing
        time.sleep(2)  # Simulate delay between each push
        return_to_start()
        time.sleep(2)  # Simulate neutral return
        print("") 


# Function to simulate three rounds of drain compressions and check if the drain is cleared.
def perform_drain_compressions():
    rounds = 0
    max_rounds = 3  # Set the maximum number of rounds
    while rounds < max_rounds:
        drain_compression()
        # Ask the user if the drain has cleared after each round
        if check_if_drain_cleared():
            print("Drain is cleared! No further action needed.\n")
            return  # Exit function if drain is cleared
        else:
            rounds += 1
            print(f"Round {rounds} completed. Checking if the drain has cleared...\n")
    
    # After 3 rounds, notify the user if the drain is still not draining
    if not check_if_drain_cleared():
        print("Drain is still not draining properly after 3 rounds of compression.\n")
        notify_user_for_manual_maintenance()


# Function to simulate checking if the drain is cleared using user input.
def check_if_drain_cleared():
    # Ask the user if the drain has cleared after each round
    while True:
        user_input = input("Did the drain clear? (y/n): ").lower()
        if user_input in ['y', 'n']:
            return user_input == 'y'
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")


# Function to notify the user that manual maintenance is required.
def notify_user_for_manual_maintenance():
    print("Manual maintenance required. Would you like to schedule a repair? (y/n)")
    user_input = input().lower()
    if user_input == 'y':
        repair_appointment = input("morning or afternoon? ").lower()
        if repair_appointment == 'morning':
            print("Scheduling next available repairman...")
            time.sleep(2)  # Simulate checking availability
            print("Repair scheduled for tomorrow at 10 AM.")
        else:
            print("Scheduling next available repairman...")
            time.sleep(2)  # Simulate checking availability
            print("Repair scheduled for tomorrow at 2 PM.") 
        # Logic for scheduling repair to include repairman availability and time. For now, assume repairman is available.
    else:
        print("You can schedule the repair later. Please monitor the drain status.")


# Main function for auto drain unclog simulation that monitors the drain status and the water level.
def auto_drain_unclog(water_present, drain_stopped, tub_capacity, baseline_drain_rate, current_drain_rate):
    if detect_water(water_present):
        print("Water detected. Monitoring drain status...\n")

        if is_drain_stopped(drain_stopped):
            print("Drain is stopped. Standby mode.\n")
            if not is_drain_unplugged(drain_stopped):
                print("Drain unplugged. Checking if water is draining...\n")

                if is_drain_rate_below_baseline(current_drain_rate, baseline_drain_rate):
                    print("Drain rate below baseline. Starting unclog process.\n")
                    perform_drain_compressions()  # Perform multiple rounds of compressions
                else:
                    print("Water drained successfully.\n")
        else:
            print("Drain is not stopped. Monitoring water levels...\n")

            if is_drain_rate_below_baseline(current_drain_rate, baseline_drain_rate):
                print("Drain rate below baseline. Starting unclog process.\n")
                perform_drain_compressions()  # Perform multiple rounds of compressions
            else:
                print("Water draining properly.\n")
    else:
        print("No water detected. System ready.\n")


# Call the main function to run the auto drain unclog simulation
def run_simulation(water_present=True, drain_stopped=False, drain_rate_factor=1):
    """
    Run the simulation with different scenarios by passing water presence, drain stopped status,
    and a drain_rate_factor to simulate different drain speeds.
    
    Args:
    water_present (bool): Simulate whether water is present in the tub.
    drain_stopped (bool): Simulate whether the drain is intentionally stopped (e.g., for a bath).
    drain_rate_factor (float): Factor to multiply the baseline drain rate to simulate clogs or slow drains.
                               For normal drains, use 1.0; for partial clogs, use 0.5; for full clogs, use 0.
    """
    # Run the baseline test once and store the tub capacity and baseline drain rate
    tub_capacity, baseline_drain_rate = perform_baseline_test()

    # DEBUG: Check the type of baseline_drain_rate before multiplying
    print(f"Type of baseline_drain_rate before multiplication: {type(baseline_drain_rate)}\n")
    print(f"Value of baseline_drain_rate: {baseline_drain_rate}\n")

    # Modify the baseline drain rate according to the drain_rate_factor
    current_drain_rate = baseline_drain_rate * drain_rate_factor

    print(f"Current drain rate: {current_drain_rate}\n")

    # Simulate the auto-unclog process using the established baseline
    auto_drain_unclog(water_present, drain_stopped, tub_capacity, baseline_drain_rate, current_drain_rate)


if __name__ == "__main__":
    run_simulation(water_present=True, drain_stopped=False, drain_rate_factor=0.05)

    # Normal drain scenario
    # run_simulation(water_present=True, drain_stopped=False, drain_rate_factor=1.0)
    
    # Partial clog scenario
    # run_simulation(water_present=True, drain_stopped=False, drain_rate_factor=0.5)

    # Full clog scenario
    # run_simulation(water_present=True, drain_stopped=False, drain_rate_factor=0.0)

    # Drain stopped for bath scenario
    # run_simulation(water_present=True, drain_stopped=True, drain_rate_factor=1.0)