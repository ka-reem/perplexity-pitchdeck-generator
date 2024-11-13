from flask import Flask, request, jsonify
from flask_cors import CORS
from perplexity_client import PerplexityClient, format_citations

app = Flask(__name__)
CORS(app)

client = PerplexityClient()

@app.route('/generate', methods=['POST'])
def generate_pitch_deck():
    company = request.json.get('company')
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    try:
        messages = [
            client.create_message("system", "You are an AI assistant that creates pitch deck content."),
            client.create_message("user", f"Create a pitch deck for {company}. Include slides for: Introduction, Problem, Solution, Market Size, Business Model, Competition, Team, Financials, and Call to Action.")
        ]

        response = client.get_completion(messages)
        content = response.choices[0].message.content

        # Parse the content into slides
        slides = parse_content_into_slides(content)

        return jsonify({"slides": slides})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_content_into_slides(content):
    # This is a simple parser. You might need to adjust it based on the actual format of the response.
    slides = []
    current_slide = None

    for line in content.split('\n'):
        if line.strip().startswith('##'):
            if current_slide:
                slides.append(current_slide)
            current_slide = {"title": line.strip('# '), "content": ""}
        elif current_slide:
            current_slide["content"] += line + "\n"

    if current_slide:
        slides.append(current_slide)

    return slides

if __name__ == '__main__':
    app.run(debug=True)