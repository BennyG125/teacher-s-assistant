import openai
import os
from dotenv import load_dotenv

# Last inn API-nøkkel
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def vurder_essay(essay_tekst):

    # Sjekk om teksten er for kort eller useriøs
    if len(essay_tekst.split()) < 350:
        return "INGEN VURDERING - Teksten er for kort eller useriøs"

    delimiter = "####"
    gjennomtenkt = "Tenk nøye og forsiktig igjennom hva som blir spurt"

    vurderingsinstruksjon = f"""Vurder essayet basert på følgende steg.
    Hvert steg er adskilt av {delimiter}.

    {delimiter} Pre-steg: {delimiter}
    Er teksten useriøs eller kortere enn 350 ord? {gjennomtenkt}.
    Hvis ja, svar kun **"INGEN VURDERING"**.
    Ikke gå videre til neste steg om du svarer "INGEN VURDERING".

    {delimiter} Steg 1: Tema og problemstilling: {delimiter}
    Er temaet klart og tydelig?
    Er problemstillingen relevant og interessant?
    Hvordan avgrenser og utforsker teksten temaet?

    {delimiter} Steg 2: Struktur og argumentasjon: {delimiter}
    Har essayet en klar innledning, hoveddel og konklusjon?
    Er argumentasjonen logisk og overbevisende?
    Bruker teksten eksempler og bevis for å underbygge påstandene?

    {delimiter} Steg 3: Personlig stemme og originalitet: {delimiter}
    Kommer forfatterens personlige stemme frem?
    Er essayet originalt og nyskapende i sin tilnærming?
    Skiller det seg fra andre tekster om samme tema?

    {delimiter} Steg 4: Språk og stil: {delimiter}
    Er språket klart, presist og variert?
    Er stilen passende for et essay?
    Bruker teksten retoriske virkemidler på en effektiv måte?

    {delimiter} Steg 5: Kilder og referanser: {delimiter}
    Er eventuelle kilder og referanser relevante og troverdige?
    Er de korrekt sitert og referert til?

    {delimiter} Steg 6: Rettskriving og grammatikk: {delimiter}
    Er det noen stavefeil eller grammatiske feil?
    Er tegnsettingen korrekt?

    {delimiter} Konklusjon: {delimiter}
    Gi en helhetlig vurdering av essayet.
    Avslutt med en karakter (A-F) hvis du ikke bedømmer innholdet som useriøst som fra {delimiter}pre-steg{delimiter}.
        Hvis innholdet vurderes som INGEN VURDERING.

    Uthev karakteren i fet skrift, hvis du gir vurdering.

    Bruk følgende format:
    Pre-steg:{delimiter} <pre-stegresonnering>
    Steg 1:{delimiter} <steg 1 resonnering>
    Steg 2:{delimiter} <steg 2 resonnering>
    Steg 3:{delimiter} <steg 3 resonnering>
    Steg 4:{delimiter} <steg 4 resonnering>
    Steg 5:{delimiter} <steg 5 resonnering>
    Steg 6:{delimiter} <steg 6 resonnering>
    Konklusjon:{delimiter} <konklusjon resonnering>

    Husk å bruke {delimiter} mellom hvert steg.
    """

    full_prompt = f"{vurderingsinstruksjon}\n\nHer er essayet:\n\n{essay_tekst}\n\nVennligst gi en detaljert vurdering basert på disse punktene."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Du er en lærerassistent som hjelper med å vurdere tekster."},
                {"role": "user", "content": full_prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )

        vurdering = response['choices'][0]['message']['content'].strip()

    except Exception as e:
        vurdering = f"Feil oppstod under vurdering: {e}"

    if vurdering == "INGEN VURDERING":
        return "Ingen vurdering kan gis på grunn av tekstens kvalitet eller lengde. Vennligst prøv en annen tekst."

    return vurdering