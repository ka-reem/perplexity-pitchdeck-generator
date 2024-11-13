from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'status': 'ok'})

@app.route('/generate', methods=['POST'])
def generate():
    try:
        company = request.json.get('company', '')
        if not company:
            return jsonify({'error': 'Company name required'}), 400

        # Test data - hard coded slides to verify frontend/backend communication
        test_slides = [
            {
                "title": "Introduction",
                "content": f"About {company}"
            },
            {
                "title": "Test Slide 2",
                "content": "Some content here"
            }
        ]

        return jsonify({
            'slides': test_slides,
            'status': 'success'
        })

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Server starting on http://localhost:5000")
    app.run(port=5000, debug=True)