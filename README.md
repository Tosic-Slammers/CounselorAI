# CounselorAI

![stock_thera](https://media.istockphoto.com/id/1388115351/photo/shot-of-a-young-man-having-a-therapeutic-session-with-a-psychologist.jpg?s=612x612&w=0&k=20&c=ABgfdHZRpzQCZpngz7jiaMfBiD081f5SONMTitDAGmQ=)

## What is CounselorAI?
With the rise of mental health problems in the world, we sought to build a web application to help those who just need some insights into their problems.
CounselorAI is a RAG model utilizing copius amounts of literature to define it's mental health service characteristics that much more over other LLM's

**RAG** (Retrieval Augmented Generation) utilizes new technologies in database querying to coincide with LLMs to produce real, non-hallucinated, sourced content. The concept of RAG is lead by Langchain in it's development.
For hosting our literature, we decided on MongoDB, utilizing their new Atlas Vector Search feature for our work. Have questions? Leave a comment!

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
