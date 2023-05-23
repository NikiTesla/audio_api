from pydub import AudioSegment
import io

def convert_to_mp3(wav_file):
    """convert_to_mp3 makes mp3 file from wav and returns io.BytesIO with it"""
    wav_audio = AudioSegment.from_file(wav_file, format="wav")

    mp3_data = io.BytesIO()
    wav_audio.export(mp3_data, format="mp3")
    mp3_data.seek(0)

    return mp3_data

def generate_link(audio_id: int, user_id: int) -> str:
    """generate_link generates link with default host, port, add user and audio id as a parameters of query"""
    host = "127.0.0.1"
    port = 8000
    return f"http://{host}:{port}/record?id={audio_id}&user={user_id}"