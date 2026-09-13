import math

cur_x = 0.01 # The algorithm starts here
gamma = 0.01 # step size multiplier
precision = 0.00001
previous_step_size = 1 
max_iters = 10000 # maximum number of iterations
iters = 0 #iteration counter

df = lambda x: -math.cos(x)

while previous_step_size > precision and iters < max_iters:
    prev_x = cur_x
    cur_x -= gamma * df(prev_x)
    previous_step_size = abs(cur_x - prev_x)
    iters+=1

print("The local minimum occurs at", cur_x)
print("The true value should be:", math.pi/2)
#The output for the above will be: ('The local minimum occurs at 1.5698099848414262)
