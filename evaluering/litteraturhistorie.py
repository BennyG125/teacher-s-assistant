import openai
import os
from dotenv import load_dotenv
from kategori_bestemmer import bestem_kategori
from evaluering import novelle, essay, litteraturhistorie, rapport

# Last inn API-nøkkel
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funksjon for å vurdere litteraturhistorie basert på vurderingspunktene
def vurder_litteraturhistorie(litteraturhistorie_tekst):

    # Først sjekker vi om teksten er for kort eller inneholder useriøse elementer
    if len(litteraturhistorie_tekst.split()) < 350:
        return "INGEN VURDERING - Teksten er for kort eller useriøs"

    # Gjennomtenkt melding som instruerer om nøyaktighet
    delimiter = "####"
    gjennomtenkt = "Ser du denne variabelen, tenk nøye og forsiktig igjennom hva som blir spurt"

    # Vurderingsinstruksjon
    vurderingsinstruksjon = f"""Vurder litteraturhistorie-teksten basert på følgende steg.
    Hvert steg er adskilt av {delimiter}.

    {delimiter} pre-steg: {delimiter}
    Gjør en vurdering på om teksten er useriøs eller færre enn 350 ord{gjennomtenkt}. Med "useriøs" menes at teksten ikke ser ut til å ha noen logisk sammenheng.
    Hvis teksten oppfyller ett eller begge av disse kriteriene, svar kun med **"INGEN VURDERING"**.
    Dersom du svarer **"INGEN VURDERING"**, skal du under ingen omstendigheter gå videre til de neste stegene. Ignorer alt annet i denne instruksjonen.

    {delimiter} Steg 1:{delimiter} Analyser tema og historisk kontekst:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}    
    Hvordan beskriver teksten den historiske og kulturelle bakgrunnen for emnet?
    Hvordan setter teksten emnet i perspektiv i forhold til litteraturhistoriske strømninger og perioder (for eksempel renessanse, modernisme, postmodernisme)?

    {delimiter} Steg 2:{delimiter} Vurder struktur og argumentasjon:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
    Er teksten godt strukturert med en klar innledning, hoveddel og konklusjon?
    Hvordan er argumentasjonen bygget opp og underbygget? Er argumentene logiske og relevante for litteraturhistorien?

    {delimiter} Steg 3:{delimiter} Analyser kilder og referanser:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
    Er kildene og referansene til litteraturhistorie troverdige og relevant brukt i teksten?
    Hvordan benyttes disse kildene for å underbygge påstandene? Er det en god balanse mellom primær- og sekundærkilder, og hvordan styrker de analysen?

    {delimiter} Steg 4:{delimiter} Vurder teoretiske perspektiver:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
    Benytter teksten litteraturhistoriske teorier og kritiske perspektiver (som strukturalisme, postkolonialisme, feminisme etc.) for å analysere emnet?
    Hvordan påvirker disse perspektivene analysen og forståelsen av teksten?

    {delimiter} Steg 5:{delimiter} Språk og stil:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
    Er språket akademisk, presist og passende for litteraturhistorisk analyse?
    Hvordan er stilistiske valg (som bruk av fagterminologi, setningsstruktur, og tone) med på å formidle de litteraturhistoriske ideene?

    {delimiter} Steg 6:{delimiter} Relevans og originalitet:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
    Er teksten relevant for temaet? Bidrar den med ny innsikt eller original analyse innen litteraturhistorie, eller bygger den på eksisterende litteratur og teorier?

    {delimiter} Steg 7:{delimiter} Rettskriving og grammatikk:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
    Er det noen stavefeil eller grammatiske feil som trekker ned den tekniske kvaliteten?

    {delimiter} Konklusjon:{delimiter} Gi en helhetlig vurdering av litteraturhistorie-teksten og avslutt med en karakter (A-F) hvis du ikke bedømmer innholdet som useriøst som fra {delimiter}pre-steg{delimiter}. \
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
    Steg 7:{delimiter} <steg 7 resonnering>
    Konklusjon:{delimiter} <konklusjon resonnering>

    Vær sikker på at du deler opp stegene ved bruk av {delimiter}.
    """

    full_prompt = f"{vurderingsinstruksjon}\n\nHer er litteraturhistorie-teksten:\n\n{litteraturhistorie_tekst}\n\nVennligst gi en detaljert vurdering basert på disse punktene."

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

    # Hvis vurderingen er "INGEN VURDERING", returnerer vi en melding
    if vurdering == "INGEN VURDERING":
        return "Ingen vurdering kan gis på grunn av tekstens kvalitet eller lengde. Vennligst prøv en annen tekst."
    
    return vurdering
