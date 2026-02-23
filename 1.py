import numpy as np

revenue = np.array([
    [4, 2, 1],
    [3, 5, 7],
    [8, 6, 9]
])

# Find determinant
det_value = np.linalg.det(revenue)

# Convert to single row
report = revenue.flatten()

print("Revenue Matrix:\n", revenue)
print("\nDeterminant:", det_value)
print("\nSingle Row Format:\n", report)