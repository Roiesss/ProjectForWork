from flask import Flask, request, jsonify, render_template
from openai import OpenAI
from flask_cors import CORS
import os


app = Flask(__name__)
# Uncomment CORS if needed for frontend requests
# CORS(app, origins=[
#     "http://localhost:8000",
#     "http://127.0.0.1:8000",
#     "http://localhost:5000",
#     "http://127.0.0.1:5000"
# ])

client = OpenAI(
    api_key='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'
)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        data = request.get_json()
        if not data:
            return "Invalid request: No JSON data provided.", 400

        size = data.get("size")
        seats = data.get("seats")
        features = data.get("features", [])

        if not size or not seats:
            return "Invalid request: Missing required fields (size or seats).", 400

        # Use requirements loaded from JSON
        relevant = []
        for req in base_requirements:
            if "אם מוגש אלכוהול" in req.get("condition", "") and "alcohol" in features:
                relevant.append(req)
            elif req.get("condition", "") == "לכל עסק":
                relevant.append(req)
            # Add more filtering logic here as needed

        prompt = f"""
        לקוח פתח עסק מסוג מסעדה בגודל {size} מ"ר עם {seats} מקומות ישיבה. הוא כולל את המאפיינים הבאים: {', '.join(features)}.
        הדרישות הרגולטוריות עבורו הן:
        {relevant}

        צור דוח בעברית, ברור ומסודר לפי נושאים, עם המלצות פעולה.
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4.5-preview",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
        except Exception as e:
            return f"Error calling GPT model: {str(e)}", 500

        report = response.choices[0].message.content
        report_text = f"דוח לדוגמה עבור עסק בגודל {size} מ\"ר עם {seats} מקומות ישיבה. מאפיינים: {', '.join(features)}. דרישות רגולטוריות: {report}"
        return report_text, 200, {"Content-Type": "text/plain; charset=utf-8"}

    except Exception as e:
        return f"An unexpected error occurred: {str(e)}", 500

if __name__ == "__main__":
    app.run(debug=True)