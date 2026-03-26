import numpy as np

# Temperature dataset
temp = np.array([30, 31, 29, 32, 30, 28, 35, 33, 31, 30])

while True:
    print("\n--- Climate Stability Analysis ---")
    print("1. Calculate Mean")
    print("2. Calculate Median")
    print("3. Calculate Variance")
    print("4. Calculate Standard Deviation")
    print("5. Evaluate Climate Stability")
    print("6. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        print("Mean Temperature:", np.mean(temp))

    elif choice == 2:
        print("Median Temperature:", np.median(temp))

    elif choice == 3:
        print("Variance:", np.var(temp))

    elif choice == 4:
        print("Standard Deviation:", np.std(temp))

    elif choice == 5:
        std = np.std(temp)
        if std > 2:
            print("Prediction: Irregular temperature pattern detected.")
        else:
            print("Prediction: Climate is relatively stable.")

    elif choice == 6:
        print("Exiting program...")
        break

    else:
        print("Invalid choice! Try again.")