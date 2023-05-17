from langchain.output_parsers import RegexParser
from langchain.tools import tool

@tool
def move_disk(game, src, dst):
    """Moves a disk from a source tower to a destination tower and returns false if the move is invalid"""

    game.move_disk(src, dst)


class TowersOfHanoiAgent:
    def __init__(self, model, env):
        self.model = model
        self.env = env
        self.instructions = """
Your goal is to achieve an observation of [[],[1,2,3],[]] or [[],[],[1,2,3]] with the lowest number of turns. 
If one of the arrays is empty, you cannot move a disk from one tower to another.
I will give you an observation and the current number of turns, formatted as:

Observation: <observation>
Turns: <turns>

You will respond with an action, formatted as:

Action: 0 1

These two numbers correspond to the source tower that you would like to move a disk from and the destination tower of where
the disk should be moved to. You will replace these two numbers with the source and destination that you would like to move a disk to.
Do nothing else but return the action.
        """

        self.action_parser = RegexParser(
            regex=r"Action: (\d+) (\d+)",
            output_keys=['src_tower', 'dest_tower'],
            default_output_key='src_tower')
        self.message_history = []
        self.ret = 0

    def reset(self):
        self.message_history = [
            # self.docs,
            self.instructions,
        ]

    def observe(self, obs):

        obs_message = f"""
Observation: {obs}
Turns: {int(len(self.message_history) / 2) - 1}
        """
        self.message_history.append(obs_message)
        return obs_message
    def _act(self):
        act_message = ""
        src_tower = 0
        dest_tower = 0
        validMove = False

        while not validMove:
            act_message = self.model(self.message_history)

            try:
                self.message_history.append(act_message)
                src_tower = int(self.action_parser.parse(act_message)['src_tower'])
                dest_tower = int(self.action_parser.parse(act_message)['dest_tower'])
            except:
                self.message_history.append("The action is invalid because you did not match the syntax expected of Action 0 1")


            validMove = True

        return src_tower, dest_tower

    def act(self):
        src_tower, dest_tower = self._act()
        return src_tower, dest_tower

class TowersOfHanoiGame:
    won = False

    def __init__(self, init_state):
        if init_state:
            self.current_state = init_state
        else:
            self.current_state = [[1,2,3], [], []]

        if self.current_state[1] == [1,2,3] or self.current_state[2] == [1,2,3]:
            self.won = True

    def get_state(self):
        sublists = [str(sublist) for sublist in self.current_state]
        joined_sublists = ", ".join(sublists)
        result = f"[{joined_sublists}]"
        return result

    def reset(self):
        self.current_state = [[3, 2, 1], [], []]
        return self.current_state

    def move_disk(self, src, dst):
        if src > 2 or dst > 2:
            return self.get_state()

        if len(self.current_state[src]) == 0:
            return self.get_state()

        if len(self.current_state[dst]) == 0 or self.current_state[dst][0] > self.current_state[src][len(self.current_state[src]) - 1]:
            self.current_state[dst].append(self.current_state[src][len(self.current_state[src]) - 1])
            self.current_state[src].pop()

        if self.current_state[1] == [3, 2, 1] or self.current_state[2] == [3, 2, 1]:
            self.won = True

        return self.get_state()
