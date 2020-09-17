import random

AGENT_ID = 1
OPPONENT_ID = 2


class State:
    def __init__(self):
        self.board = [0] * 9

    def update(self, board):
        self.board = board

    def board(self):
        return board

    def apply_action(self, action):
        if action is None:
            return
        player, row, col = action
        self.board[3*row+col] = player

    def is_gameover(self):
        return 0 not in self.board

    def win_lose_tie(self):
        indices = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
                   [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
        for a, b, c in indices:
            s = [self.board[a], self.board[b], self.board[c]]
            if s == [AGENT_ID]*3:
                return 1
            elif s == [OPPONENT_ID]*3:
                return 0
        return -1

    def __repr__(self):
        board = [str(x) for x in self.board]
        s = ''
        for i in range(3):
            s += board[i*3] + ' ' + board[i*3+1] + ' ' + board[i*3+2]
            s += '\n'
        return s

    def key(self):
        return ''.join([str(x) for x in self.board])


class Env:
    def __init__(self):
        pass

    def next_state(self, state, action):
        state.apply_action(action)
        opponent_action = self.random_action(state.board)
        state.apply_action(opponent_action)
        return state

    def random_action(self, board):
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row*3+col] == 0:
                    actions.append([OPPONENT_ID, row, col])
        return random.choice(actions) if len(actions) > 0 else None


class Agent:
    def __init__(self):
        self.values = {}  # cache all state values
        self.history = []  # cache agent all history moves
        self.eps = 0.1

    def take_action(self, state):
        state_key = state.key()
        if state_key not in self.values:
            self.values[state_key] = 0.5

        if random.random() < self.eps:
            print('Agent take random move')
            return self.take_random_action(state)

        actions = []
        max_value = -1
        for i in range(9):
            if state_key[i] == '0':
                new_state_key = state_key[:i] + '1' + state_key[i+1:]
                if new_state_key not in self.values:
                    self.values[new_state_key] = 0.5
                if self.values[new_state_key] > max_value:
                    actions = []
                    max_value = self.values[new_state_key]
                if self.values[new_state_key] == max_value:
                    row = i // 3
                    col = i % 3
                    actions.append([1, row, col, new_state_key])
        action = random.choice(actions)
        self.history.append(action[-1])
        return action[:-1]

    def take_random_action(self, state):
        state_key = state.key()
        actions = []
        for i in range(9):
            if state_key[i] == '0':
                new_state_key = state_key[:i] + '1' + state_key[i+1:]
                if new_state_key not in self.values:
                    self.values[new_state_key] = 0.5
                row = i // 3
                col = i % 3
                actions.append([AGENT_ID, row, col, new_state_key])
        action = random.choice(actions)
        return action[:-1]

    def update_values(self, last_value):
        if len(self.history) == 0:
            return
        lr = 0.1
        self.values[self.history[-1]] = last_value
        for state_key in self.history[::-1]:
            self.values[state_key] += lr * \
                (last_value - self.values[state_key])
            last_value = self.values[state_key]

    def clear_history(self):
        self.history = []


def play_once():
    env = Env()
    state = State()
    while not state.is_gameover():
        print(state)
        s = input("Your turn: ")
        row = int(s[0])
        col = int(s[1])
        env.next_state(state, [1, row, col])

        if state.win_lose_tie() == 1:
            print('You win')
            break
        elif state.win_lose_tie() == 0:
            print('You lose')
            break
    if state.win_lose_tie() == -1:
        print('We tie')
    print(state)


def play_once_with_agent(env, agent):
    state = State()
    while not state.is_gameover():
        print(state)
        action = agent.take_action(state)
        env.next_state(state, action)
        if state.win_lose_tie() != -1:
            break
    print(state)
    ret = state.win_lose_tie()
    if ret != -1:
        agent.update_values(ret)
    agent.clear_history()
    return ret


if __name__ == '__main__':
    # play_once()
    win = lose = tie = 0
    env = Env()
    agent = Agent()
    for i in range(10000):
        print("Game %d" % i)
        ret = play_once_with_agent(env, agent)
        if ret == 1:
            win += 1
            print('Agent win')
        elif ret == 0:
            lose += 1
            print('Agent Lose')
        else:
            tie += 1
            print('Tie')
    print('win=%d, lose=%d, tie=%d' % (win, lose, tie))
