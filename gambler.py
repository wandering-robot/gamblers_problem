from coin import Coin
import matplotlib.pyplot as plt

class Gambler:
    def __init__(self,goal):
        self.goal = goal
        self.coin = Coin(0.4)
        self.archive_list = []
        self.best_actions = {i:None for i in range(self.goal+1)}

        self.states = [s for s in range(self.goal+1)]
        self.state_actions = {i:[j for j in range(1,min([i,self.goal-i])+1)] for i in range(self.goal+1)}
        self.state_values = {i:0 for i in range(self.goal+1)}
        self.state_rewards = {i:0 for i in range(self.goal+1)}
        self.state_rewards[self.goal] = 1

    def learn(self,trials=100,eps=0.001):
        itr = 0
        while itr < trials:
            for state in self.states:
                max_action_value = None
                v = self.state_values[state]
                for action in self.state_actions[state]:
                    v_s = self.coin.p_succ * (self.state_rewards[state]+self.state_values[state+action]) + self.coin.p_fail * (self.state_rewards[state]+self.state_values[state-action])
                    if max_action_value == None:
                        max_action_value = (action,v_s)
                    elif v_s - max_action_value[1] > eps:
                        max_action_value = (action,v_s)
                if max_action_value == None:
                    self.state_values[state] = self.state_rewards[state]
                    self.best_actions[state] = 0
                else:
                    self.state_values[state] = max_action_value[1]
                    self.best_actions[state] = max_action_value[0]
            self.archive()
            itr += 1
        self.plot_actions(itr)
        # self.plot()
        # self.plot_actions()

    def plot_actions(self,itr):
        plt.bar(list(self.best_actions.keys()),list(self.best_actions.values()),label = f'{itr}')
        plt.legend()
        plt.show()

    def plot(self):
        for itr in range(0,len(self.archive_list),5):
            plt.plot(list(self.archive_list[itr].keys()),list(self.archive_list[itr].values()),label = f'{itr}')
        plt.legend()
        plt.show()

    def archive(self):
        self.archive_list.append(self.state_values.copy())

if __name__ == "__main__":
    player = Gambler(100)
    player.learn()
