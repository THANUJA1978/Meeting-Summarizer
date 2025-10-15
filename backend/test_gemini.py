from dotenv import load_dotenv
import os
from vertexai import init
from vertexai.generative_models import GenerativeModel

# -------------------
# Load environment
# -------------------
load_dotenv()

project = os.getenv("GCP_PROJECT_ID")
location = os.getenv("GCP_LOCATION")
model_name = os.getenv("GEMINI_MODEL")

print("Project:", project)
print("Location:", location)
print("Model:", model_name)

# -------------------
# Initialize Vertex AI
# -------------------
init(project=project, location=location)

# -------------------
# Connect to Gemini Model
# -------------------
try:
    model = GenerativeModel(model_name)
    print(f"✅ Connected to Gemini Model: {model_name}")
except Exception as e:
    print("❌ Connection failed:", e)
