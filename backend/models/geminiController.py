import json
import dotenv
import os
import google.generativeai as genai

# Load environment variables from a .env file
dotenv.load_dotenv()

try:
    # Get the API key from the environment variables
    GEMINI_API_KEY = os.environ.get('GEMINI_KEY')
    if not GEMINI_API_KEY:
        raise ValueError("Error: GEMINI_KEY not found. Please ensure it is set in your .env file.")
    
    # Configure the generative AI library
    genai.configure(api_key=GEMINI_API_KEY)
    print("Gemini API key configured successfully.")

except Exception as e:
    print(e)

def getGeminiNL(data):
    # Now you can create a model without worrying about the key here
    model = genai.GenerativeModel('gemini-2.5-pro')
    sentiment_data_string = json.dumps(data,indent=2)

    ## need to finish off making the prompt


def getNewsSummary(news,ticker_sym):
    # The model is already configured with the API key
    model = genai.GenerativeModel('gemini-2.5-flash')
    news_string = json.dumps(news,indent=2)

    prompt = f"""
        Analayse the following recent headlines for the stock {ticker_sym}
        and determine the overall sentiment for the stock based on the headlines and summary
        then give a response on the sentiment in a maximum of 2 sentences:

        {news_string}
    """

    try:
        print('Producing Gemini News Summary...')
        print(GEMINI_API_KEY)
        response = model.generate_content(prompt)
        return response.text

    except Exception as e:
        print(f'Error producing analysis > {e}')
        return f'ERROR > {e}'