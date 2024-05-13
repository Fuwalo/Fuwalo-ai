from fastapi import FastAPI, File, UploadFile
from fastapi.responses import Response
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from piano_transcription_inference import PianoTranscription, sample_rate, load_audio_from_memory
from io import BytesIO
from data import savemidi
import base64

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# Variable to store the MIDI data
midi_data_in_memory = None

@app.post('/transcribe')
async def transcribe_audio(audio: UploadFile = File(...)):
    global midi_data_in_memory

    if audio.content_type.startswith('audio/') is False:
        return JSONResponse(content={'error': 'Uploaded file is not an audio file'}, status_code=400)

    try:
        audio_data = await audio.read()
        (audio, _) = load_audio_from_memory(audio_data, sr=sample_rate, mono=True)
    except Exception as e:
        return JSONResponse(content={'error': f'Error loading audio: {str(e)}'}, status_code=500)

    buf = BytesIO()

    transcriptor = PianoTranscription(device='cuda',note_onoff=0.3, frame=0.8, checkpoint_path='model.pth')
    transcribed_dict = transcriptor.transcribe(audio, None, None, buf)

    # Return the MIDI data as raw bytes
    midi_data_in_memory = buf.getvalue()
    midi_base64 = base64.b64encode(midi_data_in_memory).decode('ascii')
    savemidi(midi_base64)
    return Response(content=midi_data_in_memory, media_type="audio/midi")
