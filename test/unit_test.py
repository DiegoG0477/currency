import unittest
from io import StringIO
from automaton import Automaton
import xml.etree.ElementTree as ET

class TestAutomaton(unittest.TestCase):
    
    def setUp(self):
        """
        This method will be executed before each test case to initialize the automaton.
        We are using the optimized XML file for the automaton.
        """
        # Load the automaton (assuming it's saved in "eur_auto.xml")")
        self.automaton = Automaton("automaton.xml")

    def test_valid_inputs(self):
        """
        Test cases with valid inputs that should be accepted by the automaton.
        """
        valid_inputs = [
            "123$",       # Simple number
            "456€",       # Number followed by €
            "456,78€",   # Number with a comma
            "39,99€",     # Number with a comma and €
            "39.99$",     # Number with a decimal point and $
            "123,459$",    # Number with a comma and $
            "123.45$",    # Decimal number with €
            "10$",
            "10€",
            "5,99€",
            "5.99$",
            "500,000,000.00$",
            "500,000,000$",
            "500.000.000,00€",
            "500.000.000€",
            "1799,99€",
            "1.449,62€",
            "1478.50$",
            "1,480.50$",
            "10,330,480.20$",
            "8.900,70€",
            "5€",
            "5$",
            "10.3$",
            "123 $",
            "456 €",
            "456,78 €",
            "39,99 €",
            "39.99 $",
            "123,459 $",
            "123.45 $",
            "10 $",
            "10 €",
            "5,99 €",
            "5.99 $",
            "500,000,000.00 $",
            "500,000,000 $",
            "500.000.000,00 €",
            "500.000.000 €",
            "1799,99 €",
            "1478.50 $",
            "1,480.50 $",
            "10,330,480.20 $",
            "8.900,70 €",
            "5 €",
            "5 $",
            "10.3 $",
            "1 MXN",
            "10 MXN",
            "100 MXN",
            "100.50 MXN",
            "1,050 MXN",
            "1,050.50 MXN",
            "10,500 MXN",
            "10,500.50 MXN",
            "105,000 MXN",
            "105,000.50 MXN",
            "1,050,000 MXN",
            "1,050,000.50 MXN",
            "1 USD",
            "10 USD",
            "100 USD",
            "100.50 USD",
            "1,050 USD",
            "1,050.50 USD",
            "10,500 USD",
            "10,500.50 USD",
            "105,000 USD",
            "105,000.50 USD",
            "1,050,000 USD",
            "1,050,000.50 USD",
            "1 EUR",
            "10 EUR",
            "100 EUR",
            "100,50 EUR",
            "1.050 EUR",
            "1.050,50 EUR",
            "10.500 EUR",
            "10.500,50 EUR",
            "105.000 EUR",
            "105.000,50 EUR",
            "1.050.000 EUR",
            "1.050.000,50 EUR",
            "$0.25",
            "$0.50",
            "$1",
            "$1.50",
            "$10",
            "$10.50",
            "$100",
            "$100.50",
            "$1,050",
            "$1,050.50",
            "$10,500",
            "$10,500.50",
            "$105,000",
            "$105,000.50",
            "$1,050,000",
            "$1,050,000.50",
            "¥0.25",
            "¥0.50",
            "¥1",
            "¥1.50",
            "¥10",
            "¥10.50",
            "¥100",
            "¥100.50",
            "¥1,050",
            "¥1,050.50",
            "¥10,500",
            "¥10,500.50",
            "¥105,000",
            "¥105,000.50",
            "¥1,050,000",
            "¥1,050,000.50",
            "$ 0.25",
            "$ 0.50",
            "$ 1",
            "$ 1.50",
            "$ 10",
            "$ 10.50",
            "$ 100",
            "$ 100.50",
            "$ 1,050",
            "$ 1,050.50",
            "$ 10,500",
            "$ 10,500.50",
            "$ 105,000",
            "$ 105,000.50",
            "$ 1,050,000",
            "$ 1,050,000.50",
            "¥ 0.25",
            "¥ 0.50",
            "¥ 1",
            "¥ 1.50",
            "¥ 10",
            "¥ 10.50",
            "¥ 100",
            "¥ 100.50",
            "¥ 1,050",
            "¥ 1,050.50",
            "¥ 10,500",
            "¥ 10,500.50",
            "¥ 105,000",
            "¥ 105,000.50",
            "¥ 1,050,000",
            "¥ 1,050,000.50",
            "USD 0.50",
            "USD 0.25",
            "USD 1",
            "USD 1.50",
            "USD 10",
            "USD 10.50",
            "USD 100",
            "USD 100.50",
            "USD 1,050",
            "USD 1,050.50",
            "USD 10,500",
            "USD 10,500.50",
            "USD 105,000",
            "USD 105,000.50",
            "USD 1,050,000",
            "USD 1,050,000.50",
            "MXN 0.50",
            "MXN 0.25",
            "MXN 1",
            "MXN 1.50",
            "MXN 10",
            "MXN 10.50",
            "MXN 100",
            "MXN 100.50",
            "MXN 1,050",
            "MXN 1,050.50",
            "MXN 10,500",
            "MXN 10,500.50",
            "MXN 105,000",
            "MXN 105,000.50",
            "MXN 1,050,000",
            "MXN 1,050,000.50",
            "USD0.50",
            "USD0.25",
            "USD1",
            "USD1.50",
            "USD10",
            "USD10.50",
            "USD100",
            "USD100.50",
            "USD1,050",
            "USD1,050.50",
            "USD10,500",
            "USD10,500.50",
            "USD105,000",
            "USD105,000.50",
            "USD1,050,000",
            "USD1,050,000.50",
            "MXN 0.50",
            "MXN 0.25",
            "MXN 1",
            "MXN 1.50",
            "MXN 10",
            "MXN 10.50",
            "MXN 100",
            "MXN 100.50",
            "MXN 1,050",
            "MXN 1,050.50",
            "MXN 10,500",
            "MXN 10,500.50",
            "MXN 105,000",
            "MXN 105,000.50",
            "MXN 1,050,000",
            "MXN 1,050,000.50",
            "0.25$",
            "0.5$",
            "0.25 $",
            "0.5 $",
            "0,25€",
            "0,5€",
            "0,25 €",
            "0,5 €",
            "0.25MXN",
            "0.5MXN",
            "0.25 MXN",
            "0.5 MXN",
            "0.25USD",
            "0.5USD",
            "0.25 USD",
            "0.5 USD",
            "0,25EUR",
            "0,5EUR",
            "0,25 EUR",
            "0,5 EUR",
        ]

        print(f"{len(valid_inputs)} valid inputs to test.")
        
        for input_string in valid_inputs:
            with self.subTest(input_string=input_string):
                self.assertTrue(self.automaton.simulate(input_string), f"'{input_string}' should be accepted.")
    
    def test_invalid_inputs(self):
        """
        Test cases with invalid inputs that should be rejected by the automaton.
        """
        invalid_inputs = [
            "abc",         # Non-numeric characters
            "12a",         # Mixed letters and numbers
            "12,",         # Invalid comma position
            "12.",         # Invalid decimal position
            "123.456,",    # Incorrect use of comma after decimal
            "1,2,3",       # Multiple commas incorrectly placed
            "1€2",         # Incorrect symbol position
            "€123$",       # Multiple currency symbols
            "78,90$",    # Comma-separated number with $
            "78.90€",    # Decimal number with €
            "12,34,567$",  # Multiple commas followed by $
            "500,000,000.$",  # Multiple commas followed by a period
            "500.000.000,€",  # Multiple periods followed by a comma
        ]
        
        for input_string in invalid_inputs:
            with self.subTest(input_string=input_string):
                self.assertFalse(self.automaton.simulate(input_string), f"'{input_string}' should be rejected.")
    
    def test_empty_input(self):
        """
        Test with an empty input, which should be rejected.
        """
        self.assertFalse(self.automaton.simulate(""), "Empty input should be rejected.")
    
    def test_large_number(self):
        """
        Test with a large valid number that should be accepted.
        """
        large_numbers = [
            "1626126,890120€",
            "1626126,890120 €",
            "1626126.890120$",
            "1626126.890120 $",
            "1626126,890120 EUR",
            "1626126.890120 USD",
            "1626126.890120 MXN",
            "1000$",
            "1000€",
            "10000$",
            "10000€",
            "100000$",
            "100000€",
            "1000000$",
            "1000000€",
            "10000000$",
            "10000000€",
            "100000000$",
            "100000000€",
            "1000000000$",
            "1000000000€",
            "10000000000$",
            "1000 $",
            "1000 €",
            "10000 $",
            "10000 €",
            "100000 $",
            "100000 €",
            "1000000 $",
            "1000000 €",
            "10000000 $",
            "10000000 €",
            "100000000 $",
            "100000000 €",
            "1000000000 $",
            "1000000000 €",
            "10000000000 $",
            "1000 MXN",
            "1000 MXN",
            "10000 MXN",
            "10000 MXN",
            "100000 MXN",
            "100000 MXN",
            "1000000 MXN",
            "1000000 MXN",
            "10000000 MXN",
            "10000000 MXN",
            "100000000 MXN",
            "100000000 MXN",
            "1000000000 MXN",
            "1000000000 MXN",
            "10000000000 MXN",
            "1000 USD",
            "1000 USD",
            "10000 USD",
            "10000 USD",
            "100000 USD",
            "100000 USD",
            "1000000 USD",
            "1000000 USD",
            "10000000 USD",
            "10000000 USD",
            "100000000 USD",
            "100000000 USD",
            "1000000000 USD",
            "1000000000 USD",
            "10000000000 USD",
            "1000 EUR",
            "1000 EUR",
            "10000 EUR",
            "10000 EUR",
            "100000 EUR",
            "100000 EUR",
            "1000000 EUR",
            "1000000 EUR",
            "10000000 EUR",
            "10000000 EUR",
            "100000000 EUR",
            "100000000 EUR",
            "1000000000 EUR",
            "1000000000 EUR",
            "10000000000 EUR",
        ]

        for large_number in large_numbers:
            with self.subTest(large_number=large_number):
                self.assertTrue(self.automaton.simulate(large_number), f"'{large_number}' should be accepted.")

if __name__ == "__main__":
    unittest.main()