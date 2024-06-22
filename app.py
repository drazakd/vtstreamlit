import streamlit as st
import speech_recognition as sr
from moviepy.editor import VideoFileClip, AudioFileClip
from deep_translator import GoogleTranslator
from gtts import gTTS
import os
import tempfile


def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio, language="en-US")  # Utilisation de la langue anglaise par défaut
        return text
    except sr.UnknownValueError:
        return "Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Speech Recognition service; {e}"


def main():
    st.title("Video Translator")

    source_lang = st.selectbox("Select source language", ["en", "fr", "es"], index=0)
    dest_lang = st.selectbox("Select destination language", ["en", "fr", "es"], index=1)

    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])

    if uploaded_file is not None:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
            temp_video.write(uploaded_file.read())
            video_path = temp_video.name

        st.write("Processing video...")
        video = VideoFileClip(video_path)

        with st.spinner('Extracting audio...'):
            audio_path = 'audio.wav'
            video.audio.write_audiofile(audio_path)

        st.progress(20)

        with st.spinner('Transcribing audio...'):
            text = transcribe_audio(audio_path)

        st.progress(50)

        with st.spinner('Translating text...'):
            translated_text = GoogleTranslator(source=source_lang, target=dest_lang).translate(text)

        st.progress(70)

        with st.spinner('Synthesizing speech...'):
            tts = gTTS(translated_text, lang=dest_lang)
            translated_audio_path = 'translated_audio.mp3'
            tts.save(translated_audio_path)

        st.progress(90)

        with st.spinner('Merging audio with video...'):
            translated_audio = AudioFileClip(translated_audio_path)
            final_video = video.set_audio(translated_audio)
            final_video_path = 'translated_video.mp4'
            final_video.write_videofile(final_video_path)

        st.progress(100)

        # Cleanup
        os.remove(audio_path)
        os.remove(translated_audio_path)

        st.success("Translation completed!")
        st.video(final_video_path)
        st.markdown(f"[Download Translated Video](translated_video.mp4)")


if __name__ == "__main__":
    main()

# import streamlit as st
# import speech_recognition as sr
# from moviepy.editor import VideoFileClip, AudioFileClip
# from googletrans import Translator
# from gtts import gTTS
# import os
# import tempfile
#
#
# def transcribe_audio(audio_path):
#     recognizer = sr.Recognizer()
#     with sr.AudioFile(audio_path) as source:
#         audio = recognizer.record(source)
#     try:
#         text = recognizer.recognize_google(audio)
#         return text
#     except sr.UnknownValueError:
#         return "Google Speech Recognition could not understand audio"
#     except sr.RequestError as e:
#         return f"Could not request results from Google Speech Recognition service; {e}"
#
#
# def main():
#     st.title("Video Translator")
#
#     source_lang = st.selectbox("Select source language", ["en", "fr", "es"], index=0)
#     dest_lang = st.selectbox("Select destination language", ["en", "fr", "es"], index=1)
#
#     uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
#
#     if uploaded_file is not None:
#         with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_video:
#             temp_video.write(uploaded_file.read())
#             video_path = temp_video.name
#
#         st.write("Processing video...")
#         video = VideoFileClip(video_path)
#
#         with st.spinner('Extracting audio...'):
#             audio_path = 'audio.wav'
#             video.audio.write_audiofile(audio_path)
#
#         st.progress(20)
#
#         with st.spinner('Transcribing audio...'):
#             text = transcribe_audio(audio_path)
#
#         st.progress(50)
#
#         with st.spinner('Translating text...'):
#             translator = Translator()
#             translated_text = translator.translate(text, src=source_lang, dest=dest_lang).text
#
#         st.progress(70)
#
#         with st.spinner('Synthesizing speech...'):
#             tts = gTTS(translated_text, lang=dest_lang)
#             translated_audio_path = 'translated_audio.mp3'
#             tts.save(translated_audio_path)
#
#         st.progress(90)
#
#         with st.spinner('Merging audio with video...'):
#             translated_audio = AudioFileClip(translated_audio_path)
#             final_video = video.set_audio(translated_audio)
#             final_video_path = 'translated_video.mp4'
#             final_video.write_videofile(final_video_path)
#
#         st.progress(100)
#
#         # Cleanup
#         os.remove(audio_path)
#         os.remove(translated_audio_path)
#
#         st.success("Translation completed!")
#         st.video(final_video_path)
#         st.markdown(f"[Download Translated Video](translated_video.mp4)")
#
#
# if __name__ == "__main__":
#     main()
