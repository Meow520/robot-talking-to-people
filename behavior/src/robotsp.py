import robotop as op
from gtts import gTTS 
from pydub import AudioSegment


def make_wav(text:str, output_file_path='temp.wav', slow=False) -> int:
    gTTS(text=text, lang='ja', slow=slow).save('temp.mp3')
    sound = AudioSegment.from_mp3('temp.mp3')
    sound.export(output_file_path, format='wav')
    return sound.duration_seconds

def say_text(ip:str, port:int, text:str) -> int:
    d = make_wav(text)
    op.play_wav(ip, port, 'temp.wav')
    return d