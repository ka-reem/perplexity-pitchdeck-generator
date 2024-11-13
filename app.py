from flask import Flask, request, jsonify
from flask_cors import CORS
from perplexity_client import PerplexityClient

app = Flask(__name__)
CORS(app)

client = PerplexityClient()

@app.route('/generate', methods=['POST'])
def generate_pitch_deck():
    company = request.json.get('company')
    description = request.json.get('description')
    
    if not company or not description:
        return jsonify({"error": "Company name and description are required"}), 400

    try:
        messages = [
            client.create_message("system", "You are an AI assistant that creates detailed and well-structured pitch deck content. Provide comprehensive information for each slide, including relevant statistics and data points. Format the content clearly with proper headers and bullet points."),
            client.create_message("user", f"""Create a detailed pitch deck for {company}. Company description: {description}

Generate the following slides, each with specific, well-structured content and cite sources:

1. Title: Company name, tagline, and brief description
2. Problem: Clearly state the problem your company is solving
3. Solution: Describe your product or service and how it solves the problem
4. Market Size: Provide specific market size figures (TAM, SAM, SOM)
5. Business Model: Explain how your company makes money
6. Competition: Create a competitive landscape and highlight your unique selling proposition
7. Traction: Provide specific metrics and milestones achieved
8. Team: List key team members with their roles and relevant experience

For each slide, provide detailed content in a clear, structured format. Use bullet points where appropriate and include specific numbers, percentages, and facts. Ensure the content is tailored to the company description provided.""")
        ]

        response = client.get_completion(messages)
        content = response.choices[0].message.content

        # Parse the content into slides
        slides = parse_content_into_slides(content)

        return jsonify({"slides": slides})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def parse_content_into_slides(content):
    slides = []
    current_slide = None
    current_content = []
    
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith(('1.', '2.', '3.', '4.', '5.', '6.', '7.', '8.')):
            if current_slide:
                current_slide['content'] = '\n'.join(current_content)
                slides.append(current_slide)
            title = line.split(':', 1)[-1].strip() if ':' in line else line.split('.', 1)[-1].strip()
            current_slide = {'title': title, 'content': ''}
            current_content = []
        elif current_slide:
            current_content.append(line)
    
    if current_slide:
        current_slide['content'] = '\n'.join(current_content)
        slides.append(current_slide)
    
    return slides

if __name__ == '__main__':
    app.run(debug=True)