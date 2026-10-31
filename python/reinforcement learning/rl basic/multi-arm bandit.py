import numpy as np
from matplotlib import pyplot as plt

class BernouliBandit:
    def __init__(self, K):
        self.probs = np.random.uniform(size=K)
        self.best_prob_idx = np.argmax(self.probs)
        self.best_prob = self.probs[self.best_prob_idx]
        self.K = K

    def step(self, k):
        if np.random.uniform() > self.probs[k]:
            return 1
        else: 
            return 0

np.random.seed(105)
K = 10
bandit_10_arm = BernouliBandit(10)
print('best_prob_idx: %d best_prob: %.4f' % (bandit_10_arm.best_prob_idx, bandit_10_arm.best_prob))

class Solver:
    def __init__(self, bandit):
        self.bandit = bandit
        self.counts = np.zeros(self.bandit.K)  
        self.regret = 0. 
        self.actions = []  
        self.regrets = []  

    def update_regret(self, k): 
        self.regret += self.bandit.best_prob - self.bandit.probs[k]
        self.regrets.append(self.regret)

    def run_one_step():

        raise NotImplementedError

    def run(self, num_steps):
        for _ in range(num_steps):
            k = self.run_one_step()
            self.counts[k] += 1
            self.actions.append(k)
            self.update_regret(k)

    