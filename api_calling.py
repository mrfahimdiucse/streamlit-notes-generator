import os ,io
import streamlit as st





try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

my_api_key = os.getenv("GEMINI_API_KEY")

def _get_client():
    api_key = my_api_key
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except Exception:
            api_key = None
    if not api_key:
        raise RuntimeError(
            "Missing GEMINI_API_KEY. Add it to Streamlit Cloud secrets or your local .env file."
        )
    from google import genai

    return genai.Client(api_key=api_key)



# note generator 
def note_generator(images):

    prompt = """Summarize the picture in note format in language Bangla at max 100 words
    make sure to add necessary markdown to differentiate different section"""


    response = _get_client().models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[*images, prompt]
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty note summary.")
    return response.text



def audio_transcription(text):
    from gtts import gTTS

    speech = gTTS(text,lang='bn',slow=False)
    audio_buffer = io.BytesIO()
    speech.write_to_fp(audio_buffer)
    return audio_buffer.getvalue()


def quiz_generator(image,difficulty):

    prompt = f"Generate 3 quizzes based on the {difficulty}. Make sure to add markdown to differentiate the options. Add correct answer too,after the quiz"


    response = _get_client().models.generate_content(
        model = "gemini-3-flash-preview",
        contents=[*image, prompt]
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty quiz.")
    return response.text
