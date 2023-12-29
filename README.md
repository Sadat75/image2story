Story Teller
Introduction
Story Teller is a web-based application that transforms uploaded images into captivating stories. Utilizing advanced AI models, the application generates a short story based on the content of the image and converts the text into speech. This project combines image-to-text, text generation, and text-to-speech technologies to create an interactive and engaging user experience.

Features
Image Upload: Users can upload an image to the application.
Image to Text: Converts the uploaded image into a descriptive text using an image captioning model.
Story Generation: Generates a short story based on the image description.
Text to Speech: Converts the generated story into an audio format.
Installation
To run Story Teller, you need to install the required dependencies. You can do this by running the following command:

bash
Copy code
pip install -r requirements.txt
Save to grepper
Usage
To start the application, run the following command in your terminal:

bash
Copy code
streamlit run app.py
Save to grepper
Navigate to the provided local URL in your web browser to interact with the application.

Requirements
Python 3.x
Dependencies listed in requirements.txt
Environment Variables
Ensure to set your Hugging Face API token in a .env file:

makefile
Copy code
HUGGINGFACEHUB_API_TOKEN=your_token_here
Save to grepper
Contributing
Contributions to the Story Teller project are welcome. Please ensure to follow best practices for code contributions and pull requests.