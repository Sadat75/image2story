from dotenv import find_dotenv, load_dotenv
from transformers import pipeline
from langchain import PromptTemplate, LLMChain
from langchain_community.chat_models import ChatOpenAI
import requests
import os
import streamlit as st
from PIL import Image
import io

load_dotenv(find_dotenv())
HUGGINGFACE_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

def img2text(img):
    """
    Convert an image to text using the Salesforce/blip-image-captioning-base model.

    Parameters:
        img (bytes): The image file to be converted.

    Returns:
        str: The generated text from the image.
    """

    image = Image.open(io.BytesIO(img.getvalue()))
    image_to_text = pipeline("image-to-text", model="Salesforce/blip-image-captioning-base")
    text = image_to_text(image)[0]['generated_text']
    
    print(text)
    
    return text


def generate_story(scenario):
    """
    Generate a short story based on the given scenario.

    Parameters:
        scenario (str): The scenario for the story.

    Returns:
        str: The generated story.
    """
    
    template = """
    You are a story teller;
    You can generate a short story based on the following scenario: {scenario}, the story should be between 30 and 40 words long.
    """
    prompt = PromptTemplate(template = template, input_variables = ["scenario"])
    story_llm  = LLMChain(llm = ChatOpenAI(model_name = "gpt-3.5-turbo", temperature=1), prompt = prompt, verbose = True)
    
    story = story_llm.predict(scenario = scenario)
    print(story)
    
    return story


def text2speech(text):
    """
    Converts text to speech using the Hugging Face API.

    Args:
        text (str): The text to be converted to speech.

    Returns:
        None: The converted audio file is saved as "audio.flac".
    """
    API_URL = "https://api-inference.huggingface.co/models/espnet/kan-bayashi_ljspeech_vits"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payloads = {
        "inputs": text
    }
    response = requests.post(API_URL, headers=headers, json=payloads)
    with open("audio.flac", "wb") as f:
        f.write(response.content)


def main():
    """
    This function is the main entry point of the program. It sets the page configuration for the Story Teller app, 
    including the page title and icon. It then displays a header to introduce the app to the user. The function 
    prompts the user to upload an image file of type jpg. If an image file is uploaded, it is saved locally and 
    displayed in the app. The function then processes the uploaded image using the img2text function to extract 
    the scenario. The scenario is then used as input to the generate_story function to generate a story. The story 
    is converted to speech using the text2speech function. The function displays the scenario, story, and audio 
    using st.expander and st.write. Finally, the function removes the temporary audio and image files.
    """
    
    st.set_page_config(page_title="Story Teller", page_icon="📖")
    
    st.header("Turn your captured moments into a story")
    uploaded_file = st.file_uploader("Upload an image", type="jpg")
    
    if uploaded_file is not None:
        print(uploaded_file)
        bytes_data = uploaded_file.getvalue()
        with open(uploaded_file.name, 'wb') as file:
            file.write(bytes_data)
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        
        scenario = img2text(uploaded_file)
        story = generate_story(scenario)
        text2speech(story)
        
        with st.expander("Scenario"):
            st.write(scenario)
        with st.expander("Story"):
            st.write(story)
        with st.expander("Audio"):
            st.audio("audio.flac")

        
if __name__ == "__main__":
    main()