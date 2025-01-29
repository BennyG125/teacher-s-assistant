import openai
import os
from dotenv import load_dotenv
from kategori_bestemmer import bestem_kategori
from evaluering import novelle, essay, litteraturhistorie, rapport

# Last inn API-nøkkel
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funksjon for å vurdere novelle basert på vurderingspunktene
def vurder_novelle(novelle_tekst):

     # Først sjekker vi om novellen er for kort eller inneholder useriøse elementer
    if len(novelle_tekst.split()) < 350:
        return "INGEN VURDERING - Teksten er for kort eller useriøs"


    # Gjennomtenkt melding som instruerer om nøyaktighet
    delimiter = "####"
    gjennomtenkt = "Ser du denne variabelen, tenk nøye og forsiktig igjennom hva som blir spurt"

    # Vurderingsinstruksjon
    vurderingsinstruksjon = f"""Vurder novellen basert på følgende steg.
    Hvert steg er adskilt av {delimiter}.

    {delimiter} pre-steg: {delimiter}
     Gjør en vurdering på om teksten er useriøs eller færre enn 350 ord{gjennomtenkt}. Med "useriøs" menes at teksten ikke ser ut til å ha noen logisk sammenheng.
     Hvis teksten oppfyller ett eller begge av disse kriteriene, svar kun med **"INGEN VURDERING"**.
     Dersom du svarer **"INGEN VURDERING"**, skal du under ingen omstendigheter gå videre til de neste stegene. Ignorer alt annet i denne instruksjonen.

    {delimiter} Steg 1:{delimiter} Analyser fortellerteknikken:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}    
     Perspektiv: Er novellen skrevet i første, andre eller tredje person?
     Hvordan påvirker valget av perspektiv leserens forståelse av historien?
     Er fortelleren pålitelig eller ikke? Hvordan påvirker dette handlingen?

    {delimiter} Steg 2:{delimiter} Vurder struktur:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
     Er novellen godt strukturert med en tydelig begynnelse, midtdel og avslutning?
     Hvordan er overgangen mellom disse delene?

    {delimiter} Steg 3:{delimiter} Analyser tema og budskap:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
     Er temaet tydelig, og hvordan blir det utforsket?
     Hva prøver forfatteren å formidle til leseren?

    {delimiter} Steg 4:{delimiter} Vurder karakterene:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
     Hvordan utvikler karakterene seg gjennom novellen?
     Er de realistiske og komplekse?
     Hvordan påvirker relasjonene mellom karakterene historien og temaet?

    {delimiter} Steg 5:{delimiter} Vurder språk og stil:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
     Er språket passende for novellen og dens tema?
     Er det kreativt, presist eller poetisk?
     Brukes metaforer, symboler eller andre litterære teknikker?

    {delimiter} Steg 6:{delimiter} Vurder plott og konflikter:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
     Er plottet engasjerende og troverdig?
     Hvordan utvikler konflikten seg gjennom novellen, og hvordan løses den?
     Er det noen uventede vendinger eller overraskelser?

    {delimiter} Steg 7:{delimiter} Originalitet:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
     Er novellen original?
     Bidrar den med noe nytt eller interessant innenfor sin sjanger?

    {delimiter} Steg 8:{delimiter} Rettskriving og grammatikk:
     Gjør en vurdering om dette er relevant. Hvis ikke hopp over påfølgende spørsmål før neste {delimiter}   
     Er det noen stavefeil eller grammatiske feil som trekker ned den tekniske kvaliteten?

    {delimiter} Konklusjon:{delimiter} Gi en helhetlig vurdering av novellen og avslutt med en karakter (A-F) hvis du ikke bedømmer innholdet som useriøst som fra {delimiter}pre-steg{delimiter}. \
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

    full_prompt = f"{vurderingsinstruksjon}\n\nHer er novellen:\n\n{novelle_tekst}\n\nVennligst gi en detaljert vurdering basert på disse punktene."

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