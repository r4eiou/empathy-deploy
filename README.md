# What Hafen Fella?: Emotion Detection in Journal Entries with Meme-Based Feedback in Filipino

## Developers
- @Albarracin, Clarissa
- @Brodeth, Charlize
- @Garcia, Reina Althea  
- @Santos, Miko  

## Project Description  
This project is a web-based application that analyzes **user-written journal entries** using an emotion detection model and responds with **Filipino meme-based feedback** to provide comfort and relatability.

- Uses the **GoEmotions dataset and RoBERTa model** for emotion detection.
- Maps detected emotions to **6+1 basic emotions**: happiness, sadness, fear, anger, surprise, disgust, and neutral.
- Displays culturally relevant **Filipino memes** based on the detected emotion.

## Features
- Journal entry submission through a web interface.
- Emotion detection using the `SamLowe/roberta-base-go_emotions` model via Hugging Face Transformers.
- Custom emotion mapping from 28 GoEmotions labels to 6+1 basic emotions.
- Meme feedback system using pre-categorized Filipino meme images.
- User session management (login, registration, profile dashboard).

## Setup & Configuration  
Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
## Running the App
To run the flask server:
```bash
python app.py
```
Once running, copy the displayed link and open it in your web browser
