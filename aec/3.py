import numpy as np

print('===TRAFFIC FLOW SIMULATION===')

#Initial matrix
#Rows:From(Road A to Road B)
#Column:From(Road A to Road B)

T=np.array([[120,30],[40,100]])
print("Initial Traffic matrix:")
print('Rows:From Road A to Road B')
print('Colums:Frome Road A to Road B')
print(T)

initial_total=np.sum(T)
print('Total initial traffic:')
print(initial_total)

#signal optimization transformation
#10% decrease for road A
#20% decrease for road B

S=np.array([[0.9,0.0],[0.0,0.8]])
T_optimized=np.dot(S,T)
print("After signal optimization:")
print(np.round(T_optimized,2))

optimized_total=np.sum(T_optimized)
print('Total after optimization:')
print(np.round(optimized_total,2))

#Redistribution matrix(Traffic shift)
#15% of road A traffic shifts to road B
#20% of road B traffic shifts to road A

M=np.array([[0.85,0.15],[0.20,0.80]])
T_redistributed=np.dot(M,T_optimized)
print('After redistribution:')
print(np.round(T_redistributed,2))

redistributed_total=np.sum(T_redistributed)
print("Total after redistribution:")
print(redistributed_total)

#Multi-cycle simulation
T_sim=T_redistributed.copy()
for cycle in range(5):
    T_sim=np.dot(M,T_sim)

print('After 5 signal cycles:')
print(np.round(T_sim,2))
final_total=np.sum(T_sim)
print("Final total traffic:\n",round(final_total,2))

#Performance analysis

percentage_change=((T_sim-T)/T)*100
print('Percentage change compared to initial:')
print(np.round(percentage_change,2))

print('===ANALYSIS SUMMARY===')
if final_total>initial_total:
    print('Overall traffic throughout increased')
elif final_total<initial_total:
    print('Overall traffic throughout decreased')
else:
    print("Total traffic remained same")