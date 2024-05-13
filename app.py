import streamlit as st
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio_from_memory
from io import BytesIO
import base64
import os




container1 = st.container()


st.title('Audio to Midi 🎶(BETA)')
st.write('Convert your audio to MIDI effortlessly. Instant, accurate, and free. Unleash your music'+'s potential with our easy-to-use Audio to MIDI converter')
audiofile = st.file_uploader('Upload audio file', type=['.wav'], accept_multiple_files=False)
my_bar = None

def print_progress(current, total):
    my_bar.progress(current / total)
    my_bar.text(f'Transcribing ({current + 1} / {total + 1} segments)...')

def create_audio_player(audio_bytes, format='wav'):
    st.audio(audio_bytes, format=f'audio/{format}', start_time=0)

def main():
    

    # Create a sidebar navigation bar
    
    page = st.sidebar.selectbox("Select a page", ["Home", "About", "Contact"])
    st.sidebar.button('Guitar (comingsoon)')


    # Display content based on the selected page


if audiofile is not None:
    audio_bytes = audiofile.read()
    st.text('Uploaded file')
    st.audio(audio_bytes, format='audio/wav')
    path = "C:\path\to\your\audio\file.wav"

    print("Path before realpath:", path)
    path = os.path.realpath(path)
    print("Path after realpath:", path)

    with st.spinner('Resampling...'):
        (audio, _) = load_audio_from_memory(audio_bytes, sr=sample_rate, mono=True)
    st.success('Resampling complete.')

    my_bar = st.progress(0)
    my_bar.text('Transcribing...')
    sencetivity=0.1
    acurate=0.3

    transcriptor = PianoTranscription(device='cuda',note_onoff=sencetivity, frame=acurate, checkpoint_path='model.pth')

    buf = BytesIO()

    transcribed_dict = transcriptor.transcribe(audio, None, print_progress, buf)

    filename = f'transcribed_{audiofile.name}.mid'

    b64 = base64.b64encode(buf.getvalue()).decode()
    st.markdown(f'<a href="data:audio/midi;base64,{b64}" download="{filename}">Download MIDI</a>', unsafe_allow_html=True)
    st.markdown('''
''', unsafe_allow_html=True)
    container1.success('Process completed successfully!')

main()



# FAQ data
faqs = [
    {"question": "How can i use it?🤔", "answer": "Streamlit is an open-source Python library that makes it easy to create web applications for data science and machine learning."},
    {"question": "Can I trust the security of this platform when uploading my audio files? 🤨", "answer": "You can install Streamlit using pip: `pip install streamlit`. Make sure you have Python installed on your system."},
    {"question": "What file formats are supported for audio input? 🎧", "answer": "Yes, you can customize the appearance using Streamlit's layout options, widgets, and by adding custom HTML and CSS when needed."}
]

# Display FAQ questions and answers
st.title("FAQs")

for faq in faqs:
    with st.expander(faq["question"]):
        st.write(faq["answer"])
