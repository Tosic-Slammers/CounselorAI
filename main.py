from transformers import pipeline
import gradio as gr
import os

#loading whisper AI (Speach recognition), lite version (Enflish only, more responsive)
asr = pipeline("automatic-speech-recognition", model="facebook/wav2vec2-base-960h")

# Initialize the Gradio Blocks
demo = gr.Blocks()
###########################################################
# Define the transcription function
def transcribe_long_form(filepath):
    if filepath is None:
        gr.Warning("No audio found, please retry.")
        return ""
    output = asr(
      filepath,
      max_new_tokens=256,
      chunk_length_s=30,
      batch_size=8,
    )
    return output["text"]
###########################################################
# Define microphone and file upload interfaces
mic_transcribe = gr.Interface(
    fn=transcribe_long_form,
    inputs=gr.Audio(sources="microphone",
                    type="filepath"),
    outputs=gr.Textbox(label="Transcription",
                       lines=3),
    allow_flagging="never")

file_transcribe = gr.Interface(
    fn=transcribe_long_form,
    inputs=gr.Audio(sources="upload",
                    type="filepath"),
    outputs=gr.Textbox(label="Transcription",
                       lines=3),
    allow_flagging="never",
)
###########################################################
# Set up the tabbed interface inside the demo block
with demo:
    gr.TabbedInterface(
        [mic_transcribe, file_transcribe],
        ["Transcribe Microphone", "Transcribe Audio File"],
    )

# Launch the Gradio app
demo.launch(share=True, debug=True)

