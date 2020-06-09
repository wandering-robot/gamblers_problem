from random import choices
class Coin:
    def __init__(self,p_succ):
        self.p_succ = p_succ
        self.p_fail = 1-p_succ
    
    def flip(self):
        win = [True,False]
        return choices(win,weights=[self.p_succ,self.p_fail])[0]

if __name__ == "__main__":
    coin = Coin(0.4)
    win = 0
    lose = 0
    for _ in range(100):
        if coin.flip():
            win += 1
        else:
            lose += 1

    print(f'Win = {win}, Lose = {lose}')
