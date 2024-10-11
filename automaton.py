import xml.etree.ElementTree as ET
import re

# automaton alphabet:
# { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, $, €, ¥, [,], [.], ' ', E, U, R, M, X, N, S, D }

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
        if read_value == '[SPC]':
            return char == ' '

        if read_value.startswith('[') and read_value.endswith(']'):
            # Extract the range inside the square brackets
            range_pattern = read_value[1:-1]
            return bool(re.match(f"[{range_pattern}]", char))
        
        return read_value == char

    def find_valid_sequences(self, input_string):
        """
        Processes the entire input string, detecting valid sequences
        according to the automaton, and returns a list of valid substrings with their initial and final indices.
        """
        valid_sequences = []
        current_sequence = ""
        current_state = self.initial_state
        initial_char = None

        for i in range(len(input_string)):
            char = input_string[i]
            next_state = self.is_valid_transition(current_state, char)

            if next_state is None:
                if current_state in self.final_states and current_sequence:
                    valid_sequences.append((current_sequence, initial_char, i - 1))
                
                current_state = self.initial_state
                current_sequence = ""
                initial_char = None
            else:
                if current_sequence == "":
                    initial_char = i

                current_sequence += char
                current_state = next_state

        if current_state in self.final_states and current_sequence:
            valid_sequences.append((current_sequence, initial_char, len(input_string) - 1))

        return valid_sequences

def main():
    automaton = Automaton("automaton.xml")
    
    while True:
        user_input = input("Enter a string to test (or 'exit' to quit): ")
        if user_input.lower() == 'exit':
            break

        valid_sequences = automaton.find_valid_sequences(user_input)
        if valid_sequences:
            print(f"Valid sequences found: {', '.join(valid_sequences)}")
        else:
            print("No valid sequences found.")

if __name__ == "__main__":
    main()