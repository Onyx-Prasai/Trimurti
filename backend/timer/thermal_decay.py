def calculate_tar(start_temp, ambient_temp, insulation_r_value=5):
    """
    Calculates the Time-at-Risk (TaR) for a blood packet.

    Args:
        start_temp (float): The initial temperature of the blood packet.
        ambient_temp (float): The current ambient temperature.
        insulation_r_value (int, optional): The R-value of the insulation. Defaults to 5.

    Returns:
        int: The predicted time in minutes for the temperature to cross the critical threshold.
    """
    critical_temp = 8  # Celsius
    
    # If the ambient temperature is cooler than the starting temperature, the blood packet is safe.
    if ambient_temp <= start_temp:
        return 9999  # Effectively infinite if ambient is cooler
    
    # This is a placeholder. A real implementation would be more complex and non-linear.
    # decay_rate is degrees per minute
    # R-value is typically given in ft²·°F·h/BTU. We are simplifying this to a linear factor.
    # A higher R-value means better insulation and a slower decay rate.
    # We'll assume a decay rate that is inversely proportional to the R-value.
    # This is a simplified model for demonstration purposes.
    decay_rate_factor = 60 # minutes in an hour
    decay_rate = (ambient_temp - start_temp) / (insulation_r_value * decay_rate_factor)
    
    if decay_rate <= 0:
        return 9999

    time_to_critical = (critical_temp - start_temp) / decay_rate
    
    return int(time_to_critical)
