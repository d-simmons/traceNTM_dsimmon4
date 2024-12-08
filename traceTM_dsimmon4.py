#!/usr/bin/env python3

import csv


class NTM:
    def __init__(self, file_name, max_depth=100, max_transitions=1000):
        self.name = None
        self.states = []
        self.start_state = None
        self.accept_state = None
        self.reject_state = None
        self.transitions = {}
        self.max_depth = max_depth
        self.max_transitions = max_transitions

        self.parse_file(file_name)

    def parse_file(self, file_name):
        with open(file_name, 'r') as file:
            reader = csv.reader(file)
            self.name = next(reader)[0]
            self.states = next(reader)
            _ = next(reader)  # Skip Σ
            _ = next(reader)  # Skip Γ
            self.start_state = next(reader)[0]
            self.accept_state = next(reader)[0]
            self.reject_state = next(reader)[0]

            for row in reader:
                state, char, next_state, write_char, direction = row
                key = (state, char)
                if key not in self.transitions:
                    self.transitions[key] = []
                self.transitions[key].append((next_state, write_char, direction))

    def simulate(self, input_string, debug=False):
        tree = []
        initial_config = ("", self.start_state, input_string)  # (left_of_head, state, right_of_head)
        current_level = [initial_config]
        total_transitions = 0

        while current_level and total_transitions < self.max_transitions:
            next_level = []
            tree.append(current_level)

            for config in current_level:
                left, state, right = config

                # check if in accept or reject state
                if state == self.accept_state:
                    print(f"String accepted in {len(tree) - 1} transitions")
                    self.print_path(tree, config)
                    return True
                if state == self.reject_state:
                    continue

                # get the current tape head character
                current_char = right[0] if right else "_"

                # generate next configurations
                key = (state, current_char)
                if key in self.transitions:
                    for next_state, write_char, direction in self.transitions[key]:
                        # modify the tape
                        new_left = left
                        new_right = right
                        if direction == "R":
                            new_left = left + write_char
                            new_right = right[1:] if len(right) > 1 else "_"
                        elif direction == "L":
                            new_left = left[:-1] if left else "_"
                            new_right = left[-1] + write_char if left else "_" + right

                        next_level.append((new_left, next_state, new_right))
                        total_transitions += 1

            # update the current level
            current_level = next_level

            # check depth limit
            if len(tree) >= self.max_depth:
                print(f"Execution stopped after reaching max depth of {self.max_depth}")
                return False

        # if all configurations lead to reject
        print(f"String rejected in {len(tree)} transitions")
        return False

    def print_path(self, tree, config):
        print("Path to accept:")
        for level in tree:
            if config in level:
                print(config)


# trace variables (change these to change what file, input, depth, etc.)
file_name = "aplus.csv"
input_string = "aaaaaaaaaaaaaaaa"
max_depth = 100
max_transitions = 1000

# run
ntm = NTM(file_name, max_depth, max_transitions)
ntm.simulate(input_string, debug=True)
