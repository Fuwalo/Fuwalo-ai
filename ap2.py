from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio_from_memory
from io import BytesIO
import concurrent.futures
from data import savemidi
import base64
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_root():
    return {"message": "Hello, world!"}

@app.post('/transcribe')
async def transcribe_audio(audio: UploadFile = File(...)):
    if not audio.content_type.startswith('audio/'):
        return JSONResponse(content={'error': 'Uploaded file is not an audio file'}, status_code=400)

    try:
        audio_data = await audio.read()
        (audio, _) = load_audio_from_memory(audio_data, sr=sample_rate, mono=True)
    except Exception as e:
        return JSONResponse(content={'error': f'Error loading audio: {str(e)}'}, status_code=500)

    buf = BytesIO()

    def print_progress(current, total):
        progress_percent = (current / total) * 100
        return {'progress': f'{progress_percent:.2f}% completed'}

    transcriptor = PianoTranscription(device='cuda', note_onoff=0.6, frame=0.88, checkpoint_path='model.pth')

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(transcriptor.transcribe, audio, None, print_progress, buf)

        try:
            transcribed_dict = future.result()
        except Exception as e:
            return JSONResponse(content={'error': f'Error during transcription: {str(e)}'}, status_code=500)

    midi_data = buf.getvalue()
    midi_base64 = base64.b64encode(midi_data).decode('ascii')
    savemidi(midi_base64)

    return {
        'midi': midi_data.decode('latin1')
    }
