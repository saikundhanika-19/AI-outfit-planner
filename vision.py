import json
import ollama


MODEL_NAME = "llama3.2-vision"


def analyze_clothing_image(image_path):
    """
    Analyze a clothing image using a vision-capable AI model.
    """

    schema = {
        "type": "object",
        "properties": {
            "clothing_type": {"type": "string"},
            "color": {"type": "string"},
            "pattern": {"type": "string"},
            "material": {"type": "string"},
            "style": {"type": "string"},
            "season": {"type": "string"},
            "formality": {"type": "string"},
            "matching_colors": {
                "type": "array",
                "items": {"type": "string"}
            },
            "confidence": {"type": "string"},
            "notes": {"type": "string"}
        },
        "required": [
            "clothing_type",
            "color",
            "pattern",
            "material",
            "style",
            "season",
            "formality",
            "matching_colors",
            "confidence",
            "notes"
        ]
    }

    prompt = """
    Analyze this clothing item for a digital wardrobe.

    Identify:

    1. Clothing type
    2. Main color
    3. Pattern
    4. Material, only if reasonably detectable
    5. Style
    6. Suitable season
    7. Formality
    8. Possible matching colors

    Important:
    - Do not infer body measurements.
    - Do not infer gender.
    - Do not infer ethnicity.
    - Do not infer health conditions.
    - If something cannot be determined from the image,
      say "Unknown" or explain the uncertainty.
    - Confidence should be "High", "Medium", or "Low".
    - Do not pretend uncertain information is certain.
    """

    response = ollama.chat(
        model=MODEL_NAME,
        format=schema,
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [image_path]
            }
        ],
        options={
            "temperature": 0
        }
    )

    result = json.loads(response.message.content)

    return result