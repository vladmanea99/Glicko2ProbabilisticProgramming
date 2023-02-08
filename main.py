import numpy as np


def g(RD):
    return 1 / np.sqrt(1 + 3*(RD**2) / (np.pi**2))

def E(rating, rating_j, RD_j):
    return 1 / (1 + np.exp(-g(RD_j)*(rating-rating_j)))

def map_to_real_ratings(hema_showed_rating, real_enemy_RDs):
    return hema_showed_rating + real_enemy_RDs*2

#Algorithm constants
'''
The system constant, which constrains the change in volatility over time, needs to be
set prior to application of the system. Reasonable choices are between 0.3 and 1.2,
though the system should be tested to decide which value results in greatest predictive
accuracy
'''
system_constant = 0.7
#Constant used in mapping of rating and RD to values used in the algorithm
constant = 173.7178


'''Values taken from hema rating site
Both enemy rating and rd's should be taken from the month prior the month where the games took hold
because the site updates the variables at the end of every month so choosing May would mean that the values are fresh 
for the fights used in June
'''
'''
#Fights that Vlad Manea had in June
hema_showed_enemy_ratings = np.array([1441, 1036.6, 1263.7])
real_enemy_RDs = np.array([134.7686, 143.2615, 122.2674])
#win = 1, lose = 0, draw = 0.5
scores = [0.5, 0, 0]
#Starting values for a fencer that has never played before
real_rating = 1500
real_RD = 350
volatility = 0.06


#Fights that Vlad Dobre had in June
hema_showed_enemy_ratings = np.array([1250.2, 1349.7, 800])
real_enemy_RDs = np.array([150.0634, 123.6534, 350])
#win = 1, lose = 0, draw = 0.5
scores = [0, 0, 1]
#Starting values for a fencer that has never played before
real_rating = 1500
real_RD = 350
volatility = 0.06
'''

#Fights that Andrei Chirlesan had in June

hema_calculated_rating = 1393.3
hema_calculated_RD = 90.12713

hema_showed_enemy_ratings = np.array([1425.3, 1242.2, 1355.1, 1500, 1048.7, 1263.7, 1935])
real_enemy_RDs = np.array([155.282, 114.5564, 137.8928, 350, 164.419, 122.2674, 78.03616])
#win = 1, lose = 0, draw = 0.5
scores = [0, 1, 1, 1, 1, 1, 0]

#Starting values for the fencer
hema_showed_rating_prior_month= 1264.2
real_RD = 106.3504
real_rating = hema_showed_rating_prior_month + 2*real_RD
volatility = 0.06



'''The rating displayed on hema ratings is not the actual one. The guys use the following formula: 
hema_showed_rating = real_rating - 2 * RD
this is because the hema_showed_rating has a 97.5% chance to be the exact rating according to the guys that created the website
'''
real_enemy_ratings = map_to_real_ratings(hema_showed_enemy_ratings, real_enemy_RDs)

#Mapping real values to the ones used in the algorithm
rating = (real_rating - 1500) / constant
RD = real_RD / constant

ratings = (real_enemy_ratings - 1500)/constant
enemy_RDs = real_enemy_RDs/constant

#The Algorithm starts here, for more check their documentation: http://www.glicko.net/glicko/glicko2.pdf
#***********************************************************************************************************************
v = 0
for i in range(len(ratings)):
    v += (g(enemy_RDs[i])**2)*E(rating, ratings[i], enemy_RDs[i])*(1 - E(rating, ratings[i], enemy_RDs[i]))

v = 1/v

delta = 0
for i in range(len(ratings)):
    delta += g(enemy_RDs[i])*(scores[i] - E(rating, ratings[i], enemy_RDs[i]))
delta *= v

a = np.log(volatility**2)

def f(x):
    return (np.exp(x)*(delta**2 - RD**2 - v - np.exp(x)))/(2*((RD**2 + v + np.exp(x))**2)) - ((x - a)/(system_constant**2))


epsilon = 0.000001

A = a
B = 0

if delta**2 > (RD**2 + v):
    B = np.log(delta**2 - RD**2 - v)
else:
    k = 1
    while (f(a - k*system_constant)) < 0:

        k += 1
    B = a - k*system_constant
fA = f(A)
fB = f(B)
while np.abs(B - A) > epsilon:
    C = A + (A - B)*fA/(fB - fA)
    fC = f(C)
    if fC*fB <= 0:
        A = B
        fA = fB
    else:
        fA /= 2
    B = C
    fB = fC

volatility2 = np.exp(A/2)
RD_star = np.sqrt(RD**2 + volatility2**2)

RD = 1/np.sqrt((1/(RD_star**2) + 1/v))

sum = 0
for i in range(len(ratings)):
    sum += g(enemy_RDs[i])*(scores[i] - E(rating, ratings[i], enemy_RDs[i]))
rating += (RD**2)*sum
#***********************************************************************************************

#Mapping back to real rating and RD
real_rating = constant*rating + 1500
real_RD = RD*constant

#Showed_rating calculated as it was described in the beginning of the algorithm
showed_rating = real_rating - real_RD*2
print(f"Real rating: {real_rating}")
print(f"Real RD: {real_RD}")
print(f"Showed rating: {showed_rating}")

print(f"Hema site calculated rating: {hema_calculated_rating}")
print(f"Hema site calculated RD: {hema_calculated_RD}")

print(showed_rating - hema_calculated_rating)