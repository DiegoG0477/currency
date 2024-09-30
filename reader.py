from io import StringIO
from currency import Automaton
from html_extract import extract_text_from_html
import xml.etree.ElementTree as ET

automaton = Automaton("currency_auto.xml")

text = extract_text_from_html('html/gobierno.html')

text_array = text.split(' ')

symbols = ['$', '€', '¥', 'USD', 'EUR', 'MXN']

currencies = []

def evaluate_word(word):
    current_state = automaton.initial_state
    for char in word:
        next_state = automaton.is_valid_transition(current_state, char)
        if next_state is None:
            return False
        current_state = next_state
    return current_state in automaton.final_states

# Este fue reemplazado por un bug existente cuando hay distintos MXN, USD, EUR o €
# for word in text_array:
#     current_state = automaton.initial_state

#     # print(word)

#     print(text_array.index('USD'))

#     if word in symbols:
#         # print(word)
#         symbol_index = text_array.index(word)
#         print(text_array[symbol_index-1], word)
#         print(word, text_array[symbol_index+1])

#         if evaluate_word(text_array[symbol_index-1] + ' ' + word):
#             currencies.append(text_array[symbol_index-1] + ' ' + word)
#             continue

#         if evaluate_word(word + ' ' + text_array[symbol_index+1]):
#             currencies.append(word + ' ' + text_array[symbol_index+1])

#     elif evaluate_word(word):
#         currencies.append(word)

for i in range(len(text_array)):
    current_state = automaton.initial_state
    word = text_array[i]

    if word in symbols:
        symbol_index = i
        print(text_array[symbol_index-1], word)
        print(word, text_array[symbol_index+1])

        if evaluate_word(text_array[symbol_index-1] + ' ' + word):
            currencies.append(text_array[symbol_index-1] + ' ' + word)
            continue

        if evaluate_word(word + ' ' + text_array[symbol_index+1]):
            currencies.append(word + ' ' + text_array[symbol_index+1])

    elif evaluate_word(word):
        currencies.append(word)

print(currencies)