import speech_recognition as sr
import keyboard

def main():
    # Initialize the recognizer
    r = sr.Recognizer()

    # Use the default microphone as the audio source
    with sr.Microphone() as source:
        print("Calibrating for background noise. Please wait...")
        r.adjust_for_ambient_noise(source, duration=1)  # Calibrate for ambient noise
        print("Please speak into the microphone.")

        audio = r.listen(source, timeout=10)
        text = r.recognize_google(audio)
        return "You: " + str(text)

if __name__ == "__main__":
    main()
