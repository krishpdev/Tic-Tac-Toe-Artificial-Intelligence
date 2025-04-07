from __future__ import annotations
import treeStruct
import pygame
import pickle
import python_ta

class MlModel:
    """Class to handle training of ml model
    
    Instance Attributes:
        - decisionTree: an object instance of an initialized decision tree of the game with all possible moves
        - iterationCount: an integer representing the number of games the model is trained on
    
    Representation Invariants:
        - iterationCount >= 0
    
    """
    decisionTree: treeStruct.Tree
    iterationCount: int
    
    def __init__(self, iteration: int, dec_tree: treeStruct.Tree) -> None:
        self.iterationCount = iteration
        self.decisionTree = dec_tree
    
    def play(self) -> None:
        """Simulate a game of tic-tac-toe to train the model."""
        curr_tree = self.decisionTree
        moves = []
        while curr_tree.children:
            move = curr_tree.choose_random()
            moves.append(move)
            curr_tree = curr_tree.children[move]
            
        win_state = curr_tree.root.get_game_result()
        
        curr_tree = self.decisionTree 

        if win_state in {1, 2}:  # if one of the player won
            for i in range(len(moves)):
                curr_tree = curr_tree.children[moves[i]]
                if i % 2 == win_state - 1:  # Every odd/even node gets adjusted based on which player won
                    curr_tree.weight *= 0.00003 * (3 ** ((10 / len(moves)) * (i + 0.2))) + 1
                    # curr_tree.weight = min(curr_tree.weight, 5)
                else:
                    curr_tree.weight *= -0.00003 * (3 ** ((10 / len(moves)) * (i + 0.2))) + 1
                    # curr_tree.weight = max(curr_tree.weight, 0.000001)

        elif win_state == 0:  # If the game ends in a draw
            for i in range(len(moves)):
                curr_tree = curr_tree.children[moves[i]]
                curr_tree.weight *= 0.00001 * (3 ** ((10 / len(moves)) * (i + 0.2))) + 1
                # curr_tree.weight = min(curr_tree.weight, 5)   
                
    def play_iter(self, iterations: int) -> None:
        """Run game a specific number of times to train model."""
        for _ in range(iterations):
            self.play()
            
    def save_model(self, filename: str) -> None:
        """Saves ML model to pickle file for later use."""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    def load_model(self, filename: str) -> MlModel:
        """Loads previously pickled ML model for use."""
        with open(filename, 'rb') as b:
            return pickle.load(b)


# t = MlModel(15000000, treeStruct.Tree())
# t.play_iter(15000000)
# for child in t.decisionTree.children:
#     print(child.weight)

# t.save_model("hard_game_model.pkl")

# loaded_test_model = t.load_model("hard_game_model.pkl")

# for child in loaded_test_model.decisionTree.children:
#     print(child.weight)
    
 