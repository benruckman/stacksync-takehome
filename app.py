import io
import os
import sys
import traceback

import numpy as np
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/execute', methods=['POST'])
def handle_data():
    old_stdout = sys.stdout
    redirected_output = io.StringIO()
    sys.stdout = redirected_output
    
    try: 
        request_data = request.get_json()

        # Run request data's python main function
        exec_globals = {
            "pd": pd,
            "np": np,
            "os": os,
        }
        exec(request_data['script'], exec_globals)

        result = None
        main_func = exec_globals.get('main')
        print(exec_globals)
        if callable(main_func):
            result = main_func()
        else:
            return jsonify({'error': "The script must define a callable 'main' function."}), 400

        response_data = {'result': result, 'stdout': redirected_output.getvalue()}
        return jsonify(response_data), 201 # Return 201 status code for successful POST
    except Exception as e:
        error_trace = traceback.format_exc()
        response_data = {'error': str(e), 'traceback': error_trace}
        return jsonify(response_data), 400
    finally:
        sys.stdout = old_stdout

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))