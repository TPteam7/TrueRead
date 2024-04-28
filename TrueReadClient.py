from google.cloud import texttospeech
import requests
import os
import json
from ChatGPTClient import ChatGPTClient
from io import BytesIO
from google.cloud import texttospeech
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame

app_id = os.getenv('MATHPIX_APP_ID')
api_key = os.getenv('MATHPIX_API_KEY')

class TrueReadClient:
    def __init__(self):
        self.app_id = app_id
        self.api_key = api_key

    def process_image(self, image):
        """
        Send an image to the MathPix API and return the extracted text in LaTeX format.
        Convert the PIL Image object to bytes before sending.
        """
        # Convert PIL Image to bytes
        byte_array = BytesIO()
        image.save(byte_array, format='PNG')
        byte_array.seek(0)  # Important: rewind the buffer after writing

        # Prepare the multipart/form-data request
        files = {
            "file": ("image.png", byte_array, "image/png")  # Correct tuple structure
        }
        data = {
            "options_json": json.dumps({
                "math_inline_delimiters": ["$", "$"],
                "rm_spaces": True
            })
        }
        headers = {
            "app_id": self.app_id,
            "app_key": self.api_key
        }

        # Make the POST request
        response = requests.post(
            "https://api.mathpix.com/v3/text",
            headers=headers,
            files=files,
            data=data
        )

        responseDict = json.loads(json.dumps(response.json(), indent=4, sort_keys=True))

        return responseDict
    
    def get_latex(self, image):
        responseDict = self.process_image(image=image)

        latex = responseDict["text"]
        return latex
    
    def get_prompt(self, latex):
        prompt = f"""Take this LaTeX equation: {latex}, and convert it to a text based equation. I want you to write out the text
            based equation in words and not in symbols. This is going to go to text-to-speech for a person with dyslexia to be able
            to understand the equation. Do not give me any filler/surrounding text. Please only give me what I need.
            """
        
        return prompt
    
    def get_text(self, image):
        latex = self.get_latex(image=image)

        prompt = self.get_prompt(latex)

        chat = ChatGPTClient()
        text = chat.ask_question(prompt=prompt)

        return text

    def get_audio(self, image):
        text = self.get_text(image)
        client = texttospeech.TextToSpeechClient()

        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )

        # Use WAV format
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.LINEAR16
        )

        response = client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content

    def play_audio(self, audio):
        # Initialize pygame mixer to match TTS output settings
        pygame.init()
        pygame.mixer.init(frequency=22050, size=-16, channels=1)

        # Load and play audio from BytesIO
        audio_stream = BytesIO(audio)
        sound = pygame.mixer.Sound(file=audio_stream)
        sound.play()

        # Wait for the audio to finish playing
        while pygame.mixer.get_busy():
            pygame.time.delay(100)

        pygame.quit()