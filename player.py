from state import State,Game
from random import randint

class Player:
    def __init__(self,riskyness):
        self.game = Game()
        self.game.init_states()

        self.coin = self.game.coin
        self.game.change_odds(0.5)

        self.money = randint(10,40)
        self.goal = self.game.goal
        self.game.discount_rate = riskyness

    def learn(self,itr):
        self.game.run(itr=itr)
    
    def choose(self):
        return self.game.states[self.money].best_action

    def play(self):
        result = 'win'
        tries = 0
        while self.money < self.goal:
            bet = self.choose()
            print(f'Player betting {bet} with ${self.money}')
            tries += 1
            if self.coin.flip():
                self.money += bet
            else:
                self.money -= bet
            if self.money == 0:
                result = 'lose'
                break
        print(f'You {result} after {tries} tries')


if __name__ == "__main__":
    player = Player(1)
    player.learn(itr=20)
    player.play()


