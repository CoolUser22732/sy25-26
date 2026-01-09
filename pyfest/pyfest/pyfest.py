# The initial lineup
lineup = [
    ("Good Charlotte", "punk rock", 30),
    ("All American Rejects", "punk rock", 45),
    ("Jimmy Eat World", "punk rock", 60)
]

# 1. Add the headliner
headliner = ("Yellowcard", "punk rock", 90)
lineup.append(headliner)
print(lineup)
remove_band = lineup.pop(0)
lineup.append(remove_band)
print(lineup)

# Continue the logic below...