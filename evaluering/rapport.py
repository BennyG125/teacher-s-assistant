import openai
import os
from dotenv import load_dotenv

# Last inn API-nøkkel
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funksjon for å vurdere rapport basert på vurderingspunktene
def vurder_rapport(rapport_tekst):
    # Først sjekker vi om rapporten er for kort eller inneholder useriøse elementer
    if len(rapport_tekst.split()) < 350:
        return "INGEN VURDERING - Teksten er for kort eller useriøs"
    
    # Gjennomtenkt melding som instruerer om nøyaktighet
    delimiter = "####"
    gjennomtenkt = "Ser du denne variabelen, tenk nøye og forsiktig igjennom hva som blir spurt"

    # Vurderingsinstruksjon
    vurderingsinstruksjon = f"""Vurder rapporten basert på følgende steg.
    Hvert steg er adskilt av {delimiter}.

    {delimiter} pre-steg: {delimiter}
    Gjør en vurdering på om teksten er useriøs eller færre enn 350 ord{gjennomtenkt}. Med "useriøs" menes at teksten ikke ser ut til å ha noen logisk sammenheng.
    Hvis teksten oppfyller ett eller begge av disse kriteriene, svar kun med **"INGEN VURDERING"**.
    Dersom du svarer **"INGEN VURDERING"**, skal du under ingen omstendigheter gå videre til de neste stegene. Ignorer alt annet i denne instruksjonen.

    {delimiter} Steg 1:{delimiter} Vurder rapportens struktur:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er rapporten godt strukturert med en tydelig innledning, metodikk, analyse, diskusjon og konklusjon?
    Hvordan er overgangen mellom disse delene? Er informasjonen logisk og sammenhengende?

    {delimiter} Steg 2:{delimiter} Vurder problemstilling og målsetting:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er problemstillingen tydelig formulert? Er det klart hva rapporten prøver å undersøke eller oppnå?
    Hvordan blir målsettingene adressert gjennom rapporten? Er de spesifikke, målbare og realistiske?

    {delimiter} Steg 3:{delimiter} Analyser metodikk:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er metodikken som er brukt i rapporten grundig og passende for å svare på problemstillingen?
    Er det beskrevet hvordan data er samlet inn, bearbeidet og analysert? Er metodene velbegrunnede og relevante for emnet?

    {delimiter} Steg 4:{delimiter} Vurder data og analyse:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er dataene som er presentert i rapporten relevante og pålitelige?
    Hvordan er analysen av dataene? Er den klar, logisk og støttet av dataene? Er det noen interessante funn eller mønstre?

    {delimiter} Steg 5:{delimiter} Diskusjon og konklusjon:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er diskusjonen i rapporten grundig og velbegrunnet? Knyttes funnene tilbake til problemstillingen?
    Hvordan drøftes resultatene i forhold til eksisterende forskning eller teori? Er konklusjonene godt støttet av analysen?

    {delimiter} Steg 6:{delimiter} Vurder språk og stil:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er språket i rapporten klart, presist og akademisk?
    Er det noen unødvendige ord eller uklare setninger som kan forbedres? Er setningene lette å følge, og er rapporten lett å forstå?

    {delimiter} Steg 7:{delimiter} Rettskriving og grammatikk:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er det noen stavefeil, grammatiske feil eller typografiske feil som trekker ned den tekniske kvaliteten?

    {delimiter} Steg 8:{delimiter} Relevans og originalitet:
    Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}
    Er rapporten original i sin tilnærming eller analyse? Bidrar den med nye ideer, teorier eller løsninger innenfor sitt fagfelt?
    Hvordan er rapporten relevant for emnet og aktuelle forskningsspørsmål?

    {delimiter} Konklusjon:{delimiter} Gi en helhetlig vurdering av rapporten og avslutt med en karakter (A-F) hvis du ikke bedømmer innholdet som useriøst som fra {delimiter}pre-steg{delimiter}. \
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
    Steg 8:{delimiter} <steg 8 resonnering>
    Konklusjon:{delimiter} <konklusjon resonnering>

    Vær sikker på at du deler opp stegene ved bruk av {delimiter}.
    """

    full_prompt = f"{vurderingsinstruksjon}\n\nHer er rapporten:\n\n{rapport_tekst}\n\nVennligst gi en detaljert vurdering basert på disse punktene."

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[{
                "role": "system", 
                "content": "Du er en lærerassistent som hjelper med å vurdere tekster."
            },{
                "role": "user", 
                "content": full_prompt
            }],
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

