# CounselorAI

![stock_thera](https://media.istockphoto.com/id/1388115351/photo/shot-of-a-young-man-having-a-therapeutic-session-with-a-psychologist.jpg?s=612x612&w=0&k=20&c=ABgfdHZRpzQCZpngz7jiaMfBiD081f5SONMTitDAGmQ=)

## What is CounselorAI?
With the rise of mental health problems in the world, we sought to build a web application to help those who just need some insights into their problems.
CounselorAI is a RAG model utilizing copius amounts of literature to define it's mental health service characteristics that much more over other LLM's

**RAG** (Retrieval Augmented Generation) utilizes new technologies in database querying to coincide with LLMs to produce real, non-hallucinated, sourced content. The concept of RAG is lead by Langchain in it's development.
For hosting our literature, we decided on MongoDB, utilizing their new Atlas Vector Search feature for our work. Have questions? Leave a comment!

## Examples
![ex pic](https://cdn.discordapp.com/attachments/1209124237848223829/1238167581752299631/image.png?ex=663f9e6b&is=663e4ceb&hm=fd2ad33b9cf7416d61d5bba9dafffc2a4e985a397dd99bf45a2442bc8adafa3c&)


## Getting Started


Follow these instructions to set up the project on your local machine for development and testing purposes.


### Prerequisites


- Python 3.8+.
- Conda (Anaconda or Miniconda) is recommended.


### Setting Up the Environment


1. **Clone the Repository**


   Clone the project repository to your local machine and navigate to the project directory:


   ```bash
   git clone https://your-repository-url.git
   cd your-project-directory


3. **Create and Activate a Conda Environment**


    ```bash
    # Create a Conda environment
    conda create --name speech_recog python=3.8
    # Activate the Conda environment
    conda activate speech_recog


4. **Install Dependencies**


    ```bash
    pip install -r requirements.txt


4. **Running the Application**


    ```bash
    python main.py


## Key Features
1. Instant Mental Health Counseling at the click of a button. No user information will be saved with this application so anonimity as well!
2. Trained on data specifically chosen by professionals in the field. CounselorAI's RAG is a collection of literature that helped the likes of Licensed Social Workers, PHD-Holding Therapists, and Business-Owning Liscensed Mental Health Counselors learn the art of helping someone. List of books coming soon!
3. *NEW* Speak with your counselor! Now with the implementation of a 3rd party library, we've set up a feature to allow for audible conversations from both sides within CounselorAI


## DEMO
### RAG Output vs. Base LLM Model
![Therapist Emotional Connection Q](https://i.imgur.com/raT3l89.png)
![Therapist Emotional Connection Q](https://i.imgur.com/qpAnimK.png)
When Presented with the two responses above, we found a unanimous decision in favor of our RAG model over ChatGPT 3.5 Turbo

![Therapist Emotional Connection Q](https://i.imgur.com/3Fe4sp3.png)
![Therapist Emotional Connection Q](https://i.imgur.com/mMcaTLy.png)
When Presented with the two responses above, we found a unanimous decision in favor of our RAG model over ChatGPT 3.5 Turbo

In tests with Human Feedback with our RAG model, we have found users to prefer our RAG model for mental health services over Chat GPT 3.5 Turbo

## License
Distributed under the MIT License. See [LICENSE](https://github.com/GeorgiosIoannouCoder/realesrgan/blob/main/LICENSE) for more information.

MIT License

Copyright (c) 2024 Tosic Slammers, Richard Palestri

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
