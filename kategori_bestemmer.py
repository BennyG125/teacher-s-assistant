import openai
import os
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def bestem_kategori(tekst):
    prompt = f"Les denne teksten og avgjør hvilken kategori den tilhører. Kategorien kan være: 'novelle', 'essay', 'litteraturhistorie' eller 'rapport'. Vennligst svar kun med én av disse kategoriene."

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Du er en lærerassistent som hjelper med å kategorisere tekster."},
                  {"role": "user", "content": prompt + "\n\n" + tekst}],
        temperature=0,
        max_tokens=10
    )

    return response['choices'][0]['message']['content'].strip().lower()

