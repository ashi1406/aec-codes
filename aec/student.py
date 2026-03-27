import numpy as np

# Step 1: Create 3×3 matrix (Subjects × Students)
marks = np.array([
    [78, 85, 90],   # Subject 1
    [88, 79, 92],   # Subject 2
    [84, 91, 87]    # Subject 3
])

print("Original Marks Matrix (Subjects × Students):\n", marks)

# Step 2: Convert to Student-wise format (Students × Subjects)
student_wise = marks.T
print("\nStudent-wise Marks (Students × Subjects):\n", student_wise)

# Step 3: Calculate total marks per student
total_marks = np.sum(student_wise, axis=1)
print("\nTotal Marks per Student:\n", total_marks)

# Step 4: Allocate bonus
# Condition: If marks in Subject 2 >= 85 → give +5 bonus
bonus = np.where(student_wise[:, 1] >= 85, 5, 0)
print("\nBonus Marks:\n", bonus)

# Step 5: Final marks after adding bonus
final_marks = total_marks + bonus
print("\nFinal Marks After Bonus:\n", final_marks)

# Step 6: Display final report
print("\n----- FINAL REPORT -----")
for i in range(len(student_wise)):
    print(f"Student {i+1}: Total = {total_marks[i]}, Bonus = {bonus[i]}, Final = {final_marks[i]}")