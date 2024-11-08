from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from inference_sdk import InferenceHTTPClient  # Import the SDK client

app = Flask(__name__)
CORS(app)

# Initialize the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="qsYSUO7B0OsAF1if0AVE"
)

# Function to generate recommendations based on skin type
def generate_recommendations(skin_type):
    skin_type = skin_type.strip().capitalize()  # Normalize input

    if skin_type == "Oily":
        return ["Oil-free moisturizer", "Gentle cleanser", "SPF 50 sunscreen"]
    elif skin_type == "Dry":
        return ["Hydrating serum", "Moisturizing cream", "Gentle cleanser"]
    elif skin_type == "Combination":
        return ["Balancing toner", "Lightweight moisturizer", "SPF 30 sunscreen"]
    elif skin_type == "Sensitive":
        return ["Soothing gel", "Fragrance-free moisturizer", "Mineral sunscreen"]
    else:
        return ["SEEEMORE Soothing gel", "Fragrance-free moisturizer", "Mineral sunscreen"]

# Route to render the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle image upload and skin type detection
@app.route('/check_skin_type', methods=['POST'])
def check_skin_type():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    
    # Save the uploaded file temporarily
    file_path = "temp_image.jpg"
    file.save(file_path)
    
    # Use InferenceHTTPClient to get the prediction from Roboflow's API
    try:
        result = CLIENT.infer(file_path, model_id="skin-type-detection/2")  # Specify your model ID
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500
    
    # Extract skin type and confidence from the result
    predictions = result.get("predictions", [])
    if predictions:
        skin_type = predictions[0].get("class", "Unknown")
        confidence = predictions[0].get("confidence", 0) * 100  # Convert to percentage
    else:
        skin_type = "Unknown"
        confidence = 0

    recommendations = generate_recommendations(skin_type)
    
    # Return the response as JSON
    return jsonify({
        "skin_type": skin_type,
        "confidence": confidence,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
