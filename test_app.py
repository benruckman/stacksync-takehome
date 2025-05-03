# test_app.py
import json
import unittest

import numpy as np
import pandas as pd

from app import app


class ExecuteScriptTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_valid_script(self):
        script = '''
def main():
    print("Hello, test!")
    return 42
'''
        response = self.client.post('/execute', json={'script': script})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['result'], 42)
        self.assertIn("Hello, test!", data['stdout'])

    def test_missing_main(self):
        script = '''
def not_main():
    print("Should fail")
'''
        response = self.client.post('/execute', json={'script': script})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("callable 'main'", data['error'])

    def test_exception_in_script(self):
        script = '''
def main():
    raise Exception("Test error")
'''
        response = self.client.post('/execute', json={'script': script})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertIn("Test error", data['error'])

    def test_script_with_multiple_functions_script(self):
        script = '''
def main():
    print("Hello, test!")
    return 42
def not_main():
    print("goodbye, test!")
    return "uh oh"
'''
        response = self.client.post('/execute', json={'script': script})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['result'], 42)
        self.assertIn("Hello, test!", data['stdout'])

    def test_bad_python_with_main(self):
        script = '''main'''
        response = self.client.post('/execute', json={'script': script})

        self.assertEqual(response.status_code, 400)
    def test_script_with_pandas_and_numpy(self):
        script = '''
import pandas as pd
import numpy as np

def main():
    # Creating a DataFrame from a dictionary
    data = {'col_1': [1, 2, 3], 'col_2': ['A', 'B', 'C']}
    df = pd.DataFrame(data)
    print("DataFrame from dictionary:", df)

    # Creating a DataFrame from a list of lists
    data_list = [[1, 'A'], [2, 'B'], [3, 'C']]
    df_list = pd.DataFrame(data_list, columns=['col_1', 'col_2'])
    print("DataFrame from list of lists:", df_list)

    # Creating a DataFrame from a NumPy array
    numpy_array = np.array([[1, 'A'], [2, 'B'], [3, 'C']])
    df_np = pd.DataFrame(numpy_array, columns=['col_1', 'col_2'])
    print("DataFrame from NumPy array:", df_np)

    return [84, df.to_string(), df_list.to_string(), df_np.to_string()]
'''
        response = self.client.post('/execute', json={'script': script})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("DataFrame from dictionary:", data['stdout'])
        d = {'col_1': [1, 2, 3], 'col_2': ['A', 'B', 'C']}
        df = pd.DataFrame(d)
        data_list = [[1, 'A'], [2, 'B'], [3, 'C']]
        df_list = pd.DataFrame(data_list, columns=['col_1', 'col_2'])
        numpy_array = np.array([[1, 'A'], [2, 'B'], [3, 'C']])
        df_np = pd.DataFrame(numpy_array, columns=['col_1', 'col_2'])
        self.assertEqual(data['result'], [84, df.to_string(), df_list.to_string(), df_np.to_string()])

if __name__ == '__main__':
    unittest.main()