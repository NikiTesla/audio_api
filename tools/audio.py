from pydub import AudioSegment
import io

def convert_to_mp3(wav_file):
    wav_audio = AudioSegment.from_file(wav_file, format="wav")
    mp3_data = io.BytesIO()
    wav_audio.export(mp3_data, format="mp3")

    mp3_data.seek(0)

    return mp3_data