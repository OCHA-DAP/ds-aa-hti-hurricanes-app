import pandas as pd


def speed2cat(speed):
    if pd.isnull(speed):
        return None
    elif speed <= 33:
        return "TD"
    elif speed <= 63:
        return "TS"
    elif speed <= 82:
        return "1"
    elif speed <= 95:
        return "2"
    elif speed <= 112:
        return "3"
    elif speed <= 136:
        return "4"
    else:
        return "5"
