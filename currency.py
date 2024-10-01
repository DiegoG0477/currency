import xml.etree.ElementTree as ET
import re

#el alfabeto de nuestro automata es:
#{0, 1, 2, 3, 4, 5, 6, 7, 8, 9, $, €, ¥, [,], [.], ' ', E, U, R, M, X, N, S, D}

class Automaton:
    def __init__(self, xml_file):
        self.states = {}
        self.transitions = []
        self.initial_state = None
        self.final_states = set()
        self.load_automaton(xml_file)
        
    def load_automaton(self, xml_file):
        tree = ET.parse(xml_file)
        root = tree.getroot()

        # Parse states
        for state in root.find('automaton').findall('state'):
            state_id = state.get('id')
            state_name = state.get('name')
            is_initial = state.get('initial') == 'true'
            is_final = state.get('final') == 'true'
            
            self.states[state_id] = state_name
            if is_initial:
                self.initial_state = state_id
            if is_final:
                self.final_states.add(state_id)

        # Parse transitions
        for transition in root.find('automaton').findall('transition'):
            from_state = transition.find('from').text
            to_state = transition.find('to').text
            read_value = transition.find('read').text
            self.transitions.append((from_state, to_state, read_value))
    
    def is_valid_transition(self, current_state, char):
        """
        Returns the next state if there is a valid transition, otherwise None.
        """
        for (from_state, to_state, read_value) in self.transitions:
            if from_state == current_state:
                if self.match_transition(read_value, char):
                    return to_state
        return None

    def match_transition(self, read_value, char):
        """
        Matches the input character with the transition's read value.
        Handles ranges like [0-9], symbols, and special cases like [SPC] for space.
        """

        # Handle the special case for space represented as [SPC]
        if read_value == '[SPC]':
            return char == ' '  # Compare against a space character

        # If the read_value is a character range like [0-9]
        if read_value.startswith('[') and read_value.endswith(']'):
            # Extract the range inside the square brackets
            range_pattern = read_value[1:-1]
            return bool(re.match(f"[{range_pattern}]", char))
        
        # Otherwise, just match the literal value
        return read_value == char

    def simulate(self, input_string):
        """
        Simulates the automaton on the given input string and returns True if accepted.
        """
        current_state = self.initial_state
        
        for char in input_string:
            # print(f"Processing '{char}' in state '{self.states[current_state]}'")
            next_state = self.is_valid_transition(current_state, char)
            if next_state is None:
                return False  # Invalid transition
            current_state = next_state
        
        # After processing the input, check if the automaton ends in a final state
        return current_state in self.final_states

def main():
    # Load the automaton from the XML file
    automaton = Automaton("automaton.xml")
    
    while True:
        # Get input from the user
        user_input = input("Enter a string to test (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        if automaton.simulate(user_input):
            print(f"The input '{user_input}' is accepted.")
        else:
            print(f"The input '{user_input}' is rejected.")

if __name__ == "__main__":
    main()