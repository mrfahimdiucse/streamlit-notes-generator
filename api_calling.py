from google import genai
from dotenv import load_dotenv
import os
from gtts import gTTS
import io
#loading environment variable 
load_dotenv()

my_api_key=os.environ.get("GEMINI_API_KEY")

# initialize a client 
client = genai.Client(api_key=my_api_key)
# note generator 
def note_generator(images):
    prompt="Analyze the uploaded image and generate complete, accurate, well-organized study notes in Markdown, including headings, bullet points, definitions, examples, formulas, and exam-focused summaries"
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[images,prompt])
    return response.text

def audio(text):
    speech=gTTS(text,lang="en", slow=False)
    audio_buffer=io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer

def quiz_generator(images,difficulty):
    prompt=f"Generate 5 quizes based on the {difficulty}. Make sure to add markdown to differentiate the options"
    response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents=[images,prompt])
    return response.text
