# Function to calculate the capacity of a bathtub in liters
def calculate_bathtub_capacity(length_cm, width_cm, depth_cm):
   
    # Calculate the volume of the bathtub in cubic centimeters
    volume_cc = length_cm * width_cm * depth_cm
    capacity_liters = volume_cc / 1000
    return round(capacity_liters, 2)

