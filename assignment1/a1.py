# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification and game rules on Canvas

from sys import stderr
from typing import List, Dict, Callable
from random import choice
import ast

def not_yet() -> bool:
    raise NotImplementedError("Command not implemented.")
    return False

def print_error(error: str) -> None:
    print(error, file = stderr)

CommandMap = Dict[str, Callable[[str], bool]]

class CommandInterface:
    def __init__(self) -> None:
        # you can add your own initialisation here
        
        self.state = []
        self.toplay = 'b'
        self.komi = 0.0
        self.output = 0
        self.black_score = 0.0
        self.white_score = 0.0
        self.initialized = False
        self.commands: CommandMap = {
            "help": self.cmd_help,
            "heapgo": self.cmd_heapgo,
            "show": self.cmd_show,
            "toplay": self.cmd_toplay,
            "play": self.cmd_play,
            "legal": self.cmd_legal,
            "genmove": self.cmd_genmove,
            "score": self.cmd_score,
            "winner": self.cmd_winner,
            }

    def check_heap(self, state):
        
        if not isinstance(state, list):
            return -1
        
        if len(state) == 0 or len(state) > 10:
            return -1
            
        for i in range(len(state)):
            if not isinstance(state[i], list):
                return -1
            if len(state[i]) > 10 or len(state[i]) < 1:
                return -1
                
            for j in range(len(state[i])):
                if not isinstance(state[i][j],tuple):
                    return -1 
                if len(state[i][j]) != 2:
                    return -1
                if state[i][j][0] != 'w'and state[i][j][0] != 'b':
                    return -1
                if not isinstance(state[i][j][1], int) or state[i][j][1] < 1 or state[i][j][1] > 20 :
                    return -1
                        
        return 1
            
#============================================================================
# You need to implement the following methods.
#============================================================================
    def cmd_heapgo(self, args: str) -> bool:
        try:
            komi_text, seperator, state_text = args.partition(" ")
            
            if seperator == '' or state_text.strip() == '':
                return False
            
            komi = float(komi_text)
            state = ast.literal_eval(state_text)

        except (ValueError, SyntaxError):
            return False
        
        if komi % 1 != 0.5 or komi >= 100 or komi <= -100:
            return False
        
        if self.check_heap(state) != 1:
            return False
        
        self.komi = komi
        self.state = state
        self.black_score = 0
        self.white_score = komi
        self.toplay = 'b'
        self.initialized = True
        
        return True
    
    def cmd_show(self, args: str) -> bool:
        if not self.initialized:
            return False
        print(f"k {self.komi} {self.state}")
        return True

    def cmd_toplay(self, args: str) -> bool:
        if not self.initialized:
            return False
        color = args.strip()

        if color != 'b' and color != 'w':
            return False

        self.toplay = color
        return True

    def cmd_play(self, args: str) -> bool:
        if not self.initialized:
            return False
        try:
            heap_num = int(args)
        except (ValueError):
            return False
        
        if heap_num < 0:
            return False
        
        if heap_num > len(self.state) - 1:
            return False
        
        if len(self.state[heap_num]) == 0:
            return False
        
        if self.toplay == 'b':
            while True:
                if len(self.state[heap_num]) == 0:
                    self.toplay = 'w'
                    return True
                elif self.state[heap_num][-1][0] == 'w':
                    self.black_score += self.state[heap_num][-1][1]
                    self.state[heap_num].pop()
                    self.toplay = 'w'
                    return True
                elif self.state[heap_num][-1][0] == 'b':
                    self.black_score += self.state[heap_num][-1][1]
                    self.state[heap_num].pop()
                    
        if self.toplay == 'w':
            while True:
                if len(self.state[heap_num]) == 0:
                    self.toplay = 'b'
                    return True
                elif self.state[heap_num][-1][0] == 'b':
                    self.white_score += self.state[heap_num][-1][1]
                    self.state[heap_num].pop()
                    self.toplay = 'b'
                    return True
                elif self.state[heap_num][-1][0] == 'w':
                    self.white_score += self.state[heap_num][-1][1]
                    self.state[heap_num].pop()

        return False
        
    def cmd_legal(self, args: str) -> bool:
        if not self.initialized:
            return False
        try:
            location = int(args)
        except ValueError:
            return False
        if location >= len(self.state) or location < 0 or len(self.state[location]) == 0:
            print("no")
            return True
        print("yes")
        return True

    def cmd_genmove(self, args: str) -> bool:
        if not self.initialized:
            return False
        moves = []
        for i in range(len(self.state)):
            if len(self.state[i]) > 0:
                moves.append(i)
        if len(moves) > 0:
            i = choice(moves)
            print(i)
            self.cmd_play(str(i))
            return True
        else:
            return False

    def cmd_score(self, args: str) -> bool:
        if not self.initialized:
            return False
        print(f"b {self.black_score:.0f} w {self.white_score:.1f}")
        return True

    def cmd_winner(self, args: str) -> bool:
        if not self.initialized:
            return False
        # check if the game is over
        if any(len(heap) > 0 for heap in self.state):
            return False
        winner = 'b' if self.black_score > self.white_score else 'w'
        print(winner)
        return True
#============================================================================
# End of functions requiring implementation
#============================================================================

#============================================================================
# The code below should not need modification
# Anyway, you may change or add to this code as you see fit
# Examples:
# You can add class variables to __init__ above
# You can add better error messages
# You can put commands inside your own Heap Go class
# etc.
#============================================================================
    # List available commands
    def cmd_help(self, ignore_args: str) -> bool:
        print("\nKnown commands:")
        for cmd in self.commands:
            print(cmd)
        return True

    def process_command(self, cmd_name: str, cmd_args: str) -> None:
        # Try to find command, None if wrong name
        status = "= -1"
        cmd = self.commands.get(cmd_name)
        if cmd:
            try:
                if cmd(cmd_args): # success!
                    status = "= 1"
            except Exception as e:
                print_error(f"Command {cmd_name} with arguments {cmd_args} failed with exception: {e}")
        else:
            print_error("Unknown command. Type 'help' for commands.")
        print(status)
    
    def main_loop(self) -> None:
        process_commands = True
        while process_commands:
            try:
                line = input()
            except EOFError:
                break
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(maxsplit=1)
            cmd_name = parts[0]
            if cmd_name == "exit":
                process_commands = False
                continue
            cmd_args = parts[1] if len(parts) > 1 else ""
            self.process_command(cmd_name, cmd_args)

if __name__ == "__main__":
    interface = CommandInterface()
    interface.main_loop()

