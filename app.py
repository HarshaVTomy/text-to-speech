import streamlit as st
from transformers import pipeline
from gtts import gTTS

# Custom CSS for styling
st.markdown("""
<style>
/* Background Gradient */
body {
    background: linear-gradient(135deg, #F0F4F8, #E4E9F2); /* Light gradient background */
    color: #333; /* Dark gray text color for readability */
}

/* Container Styling */
.stApp {
    background-color: #FFFFFF; /* White background for the app container */
    border-radius: 10px; /* Rounded corners */
    padding: 20px; /* Padding inside the container */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Subtle shadow for depth */
    max-width: 800px; /* Max width for the container */
    margin: auto; /* Centering the container */
}

/* Title Styling */
h1 {
    color: #4A90E2; /* Bright blue color for the title */
    text-align: center;
    font-size: 2.5em;
    margin-bottom: 20px;
}

/* Text Input Styling */
.stTextInput>div>div>input {
    border-radius: 5px;
    padding: 10px;
    border: 1px solid #4A90E2; /* Blue border */
    background-color: #FFFFFF; /* White background */
    color: #333; /* Dark gray text */
}

/* Button Styling */
button {
    background-color: #FFEFD5; /* Blue background */
    color: white;
    border-radius: 5px;
    padding: 12px 24px;
    font-size: 1.2em;
    border: none;
    cursor: pointer;
    transition: background-color 0.3s ease, transform 0.3s ease;
}

button:hover {
    background-color: #FFEFD5; /* Darker blue on hover */
    transform: scale(1.05);
}

/* Spinner Styling */
.css-1cqj0bq {
    border-top-color: transparent;
    border: 4px solid rgba(0, 0, 0, 0.1); /* Light gray border */
    border-radius: 50%;
    border-right-color: #4A90E2; /* Blue spinner */
}
</style>
""", unsafe_allow_html=True)

# Streamlit UI
st.title("Text-to-Speech Converter with LLM")
st.write("This application generates text using GPT-2 and converts it to speech.")

# Input text for LLM
input_text = st.text_input("Enter a prompt for text generation", "Once upon a time")

if st.button("Generate and Convert to Speech"):
    # Step 1: Generate text using GPT-2
    with st.spinner("Generating text..."):
        try:
            generator = pipeline('text-generation', model='gpt2')
            generated_text = generator(input_text, max_length=50, num_return_sequences=1)[0]['generated_text']
            st.success("Text generation complete!")
            st.write("Generated Text: ", generated_text)
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # Step 2: Convert generated text to speech using gTTS
    with st.spinner("Converting text to speech..."):
        tts = gTTS(generated_text)
        tts.save("output.mp3")
        st.success("Text-to-speech conversion complete!")

    # Step 3: Play the generated speech
    audio_file = open("output.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

    # Optional: Provide a download link for the audio file
    st.download_button(label="Download the audio", data=audio_bytes, file_name="output.mp3", mime="audio/mp3")
