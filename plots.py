import numpy as np
import matplotlib.pyplot as plt
def g(RD):
    return 1 / np.sqrt(1 + 3*(RD**2) / (np.pi**2))

def g_deriv(RD):
    return -3*np.pi*RD/(np.sqrt((3*RD**2 + np.pi**2)**3))

X = np.arange(50, 350, 0.1)
Y = g(X)

Y_deriv = g_deriv(X)
#plt.plot(X, Y)
#plt.plot(X, Y_deriv)
#plt.show()

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


def map_to_real_ratings(hema_showed_rating, real_enemy_RDs):
    return hema_showed_rating + real_enemy_RDs*2



constant = 173.7178

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

'''
def E(rating, rating_j, RD_j):
    return 1 / (1 + np.exp(-g(RD_j)*(rating-rating_j)))

n_sims = 100000

X = np.arange(0, n_sims, 1)
Y = np.zeros((X.shape))

for j in range(len(X)):
    enemy_RDs = np.random.normal(150, 50, 20)
    ratings = np.random.normal(1300, 200, 20)
    rating = np.random.normal(1300, 200, 1)
    for i in range(len(ratings)):
        Y[j] += (g(enemy_RDs[i]) ** 2) * E(rating, ratings[i], enemy_RDs[i]) * (1 - E(rating, ratings[i], enemy_RDs[i]))
    Y[j] /= 1
    if j % 1000 == 0:
        print(j)

plt.plot(X, Y)
plt.show()