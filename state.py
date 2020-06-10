from coin import Coin
import matplotlib.pyplot as plt
import os.path
import pathlib
class Game:
    def __init__(self):
        self.coin = Coin(0.4)
        self.goal = 100
        self.discount_rate = 1
        self.epsilon = 0.000001

        self.value_archive = []
        self.action_archive = []
    
    @staticmethod
    def get_path(file_name):
        abs_path = pathlib.Path(__file__).parent.absolute()
        complete_name = os.path.join(abs_path,'records',file_name+'.png')
        return complete_name

    def init_states(self):              #needs to be outside of __init__ or else recursion error for subclass initialization
        self.states = [State(i) for i in range(self.goal+1)]

    def change_odds(self,p_succ):
        self.coin = Coin(p_succ)

    def change_goal(self,new_goal):
        self.goal = new_goal

    def display(self):      #for debugging only
        for state in game.states:
            print(state,state.actions)

    def display_values(self):   #for debugging only
        for state in game.states:
            print(f'{state}={state.value:.3f}', end='\t')
        print('\n')

    def new_state(self,state,num):  #calculate the new state an action will lead to
        return self.states[state.money+num]

    def update_state_values(self):  #where the magic happens
        for state in self.states:
            _value, _best_action = state.value, state.best_action
            if state.money == 12:
                a=3
            if state.actions:
                for action in state.actions:
                    win_state = self.new_state(state,action)
                    lose_state = self.new_state(state,-action)
                    v_s = self.coin.p_succ*(state.reward + self.discount_rate * win_state.value) + self.coin.p_fail*(state.reward + self.discount_rate * lose_state.value)
                    if v_s > _value + self.epsilon:
                        _value, _best_action = v_s, action
            else:
                _value, _best_action = state.reward, 0
            state.value, state.best_action = _value, _best_action

    def archive_values(self):
        self.value_archive.append(([state.money for state in self.states],[state.value for state in self.states]))

    def archive_actions(self):
        self.action_archive.append(([state.money for state in self.states],[state.best_action for state in self.states]))

    def plot_values(self):
        for itr in range(len(self.value_archive)):
            money_data,value_data = self.value_archive[itr]
            plt.plot(money_data,value_data,label = f'Iter: {itr}')
        plt.legend()
        plt.savefig(self.get_path(f'act_iter_{itr}'))
        # plt.show()

    def plot_actions(self):
        for itr in range(len(self.action_archive)):
            plt.clf()
            money_data,action_data = self.action_archive[itr]
            plt.bar(money_data,action_data,label = f'Iter: {itr}')
            plt.legend()
            plt.savefig(self.get_path(f'iter_{itr}'))
            # plt.show()

    def run(self,itr=1):
        for _ in range(itr):
            self.update_state_values()
            self.archive_values()
            self.archive_actions()

class State(Game):
    def __init__(self,money,init_value=0):
        super().__init__()
        self.money = money

        self.actions = [s for s in range(1,min(self.money,(self.goal-self.money))+1)]
        self.reward = self.set_reward()

        self.value = init_value
        self.best_action = 0

    def display(self):
        print(f'State {self.money}: Value={self.value:.3f}\tAction={self.best_action}')

    def set_reward(self):
        if self.money == self.goal:
            return 1
        elif self.money == 0:
            return 0
        else:
            return 0

    def __repr__(self):
        return f'State {self.money}'

if __name__ == "__main__":
    game = Game()
    game.init_states()
    game.run(itr=15)
    game.plot_values()
    game.plot_actions()





