# CMPUT 455 Assignment 1 starter code
# Implement the specified commands to complete the assignment
# Full assignment specification and game rules on Canvas

from sys import stderr
from typing import List, Dict, Callable
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
        
        return True
    
    def cmd_show(self, args: str) -> bool:
        print(f"k {self.komi} {self.state}")
        return True

    def cmd_toplay(self, args: str) -> bool:
        print(self.toplay)
        return True

    def cmd_play(self, args: str) -> bool:
        return not_yet()
    def cmd_legal(self, args: str) -> bool:
        return not_yet()
    def cmd_genmove(self, args: str) -> bool:
        return not_yet()
    def cmd_score(self, args: str) -> bool:
        return not_yet()
    def cmd_winner(self, args: str) -> bool:
        return not_yet()
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

