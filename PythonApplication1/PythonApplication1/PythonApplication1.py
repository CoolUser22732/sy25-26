runner_info=("Chris", 540, 54)
mile_splits = [8.5, 8.2, 8.4]

print(mile_splits)
mile_splits.append(8.3)
print(mile_splits)

print(runner_info[0], sum (mile_splits))


total_time = 0
total_miles = 0
for split in mile_splits:
    print(split)
    total_time = total_time + split
    total_miles = total_miles + 1
print(runner_info[0], total_time, total_miles)

