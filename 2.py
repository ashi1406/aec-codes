import numpy as np

matrix = np.array([
    [2, 1, 1],
    [1, 3, 2],
    [1, 0, 0]
])

# Find inverse
inverse_matrix = np.linalg.inv(matrix)

# Convert inverse to single row
report = inverse_matrix.flatten()

print("Original Matrix:\n", matrix)
print("\nInverse Matrix:\n", inverse_matrix)
print("\nSingle Row Format:\n", report)