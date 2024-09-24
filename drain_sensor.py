# Function to check if the drain is intentionally stopped (e.g., for a bath)
def is_drain_stopped(stopped=False):
    return stopped

# Function to check if the drain is unplugged and ready to drain (e.g., for draining after a bath)
def is_drain_unplugged(stopped=False):
    return not stopped 