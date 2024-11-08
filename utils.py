from inference_sdk import InferenceHTTPClient

CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="qsYSUO7B0OsAF1if0AVE"
)

def get_skin_type(image_path):
    # Replace 'skin-type-detection/2' with the correct model ID from Roboflow
    model_id = "skin-type-detection/2"
    
    try:
        # Call the Roboflow inference API
        result = CLIENT.infer(image_path, model_id=model_id)

        # Extract skin type result, confidence score, and mock recommendations
        skin_type = result['predictions'][0]['class']
        confidence = result['predictions'][0]['confidence'] * 100  # Convert to percentage
        recommendations = generate_recommendations(skin_type)

        return skin_type, confidence, recommendations

    except Exception as e:
        print(f"Error occurred: {e}")
        return "Unknown", 0, ["No recommendations available"]

def generate_recommendations(skin_type):
    # Mock recommendations; adjust according to your actual recommendation logic
    if skin_type == "Oily":
        return ["Oil-free moisturizer", "Gentle cleanser", "SPF 50 sunscreen"]
    elif skin_type == "Dry":
        return ["Hydrating serum", "Moisturizing cream", "Gentle cleanser"]
    elif skin_type == "Combination":
        return ["Balancing toner", "Lightweight moisturizer", "SPF 30 sunscreen"]
    elif skin_type == "Sensitive":
        return ["Soothing gel", "Fragrance-free moisturizer", "Mineral sunscreen"]
    else:
        return ["General skincare products"]
