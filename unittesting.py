import unittest
from unittest.mock import patch
from io import StringIO
import sys


# Assuming closer() is a function to close a port
def closer():
    # Placeholder implementation
    port = input("Enter port number to close: ")
    print(f"Port {port} successfully closed.")

class TestFirewallFunctions(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_closer(self, mock_stdout):
        # Patching input to provide a port
        with patch.object(sys, 'argv', ['bhawana_firewall.py']):   
            with patch('builtins.input', return_value='8080'):
                closer()
                output = mock_stdout.getvalue().strip()
                self.assertEqual(output, "Port 8080 successfully closed.")


if __name__ == '__main__':
    unittest.main()

 