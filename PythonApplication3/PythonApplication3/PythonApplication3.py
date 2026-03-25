from turtle import speed

G3 = ["G3", "Mitsubishi Pajero", 185, ("153, 203"), 7000, 9, 6, 3497, 6]
H1 = ["H1", "Bob Miller Special", 195, ("191, 260"), 5600, 6, 2, 2900, 4]
E4 = ["E4", "Austin metro 6 ", 240, ("265,360"), 9800, 3, 4, 3600, 6]
F1 = ["F1", "VW Off-Road-Bug ", 185, ("104,142"), 6000, 9, 6, 1880, 4]  # Fixed
H3 = ["H3", "Honda Integra Type R", 235, ("145, 198"), 6500, 5, 5, 1800, 4]

cars = [G3, H1, E4, F1, H3]

def print_car(c):
    print(f"Model: {c[1]}")
    print(f"Top Speed: {c[2]} km/h", f"Power: {c[3][0]} hp, {c[3][1]} Nm")
    print(f"Price: ${c[4]}", f"Seats: {c[5]}")
    print(f"Weight: {c[7]} kg", f"Cylinders: {c[8]}")

i = 1
for c in cars: 
    print(i, c[1])
    i = i+1
    print(" ")

print ("enter a car number")
choice = int(input()) - 1
print_car(cars[choice])

