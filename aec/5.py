import pandas as pd

data = pd.read_csv("covid_data.csv")

while True:
    print("\n--- COVID DATA ANALYSIS MENU ---")
    print("1. Show first few records")
    print("2. Patients per district")
    print("3. Total male and female cases")
    print("4. Total recoveries and deaths")
    print("5. Exit")

    ch = int(input("Enter choice: "))

    if ch == 1:
        print(data.head())

    elif ch == 2:
        print(data[['District','TotalCases']])

    elif ch == 3:
        print("Total Male Cases:", data['Male'].sum())
        print("Total Female Cases:", data['Female'].sum())

    elif ch == 4:
        print("Total Recoveries:", data['Recoveries'].sum())
        print("Total Deaths:", data['Deaths'].sum())

    elif ch == 5:
        print("Program ended")
        break

    else:
        print("Invalid choice")