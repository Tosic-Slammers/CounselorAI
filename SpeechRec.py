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

        while True:
            try:
                audio = r.listen(source, timeout=10)
                text = r.recognize_google(audio)
                return "You: " + text

                if keyboard.is_pressed('esc'):
                    print("Escape key pressed, exiting...")
                    break

            except sr.WaitTimeoutError:
                print("No speech detected within the timeout period")
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except KeyboardInterrupt:
                print("Interrupted by user")
                break

if __name__ == "__main__":
    main()
