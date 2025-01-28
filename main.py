import openai
from dotenv import load_dotenv
import os
import streamlit as st

# Last inn API-nøkkel fra .env-fil
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Funksjon for å bestemme kategori av teksten
def bestem_kategori(svar):
    # Lag en prompt som ber GPT vurdere hva slags tekst det er, og vær spesifikk på at den kun skal gi kategorien
    prompt = f"Les denne teksten og avgjør hvilken kategori den tilhører. Kategorien kan være 'novelle' \
        eller 'Rapporter og undersøkelser'. Vennligst svar kun med én av de følgende kategoriene: 'novelle'. Ikke gi forklaringer, kun kategorien."

    # Bruk chat-API for å få svar
    response = openai.ChatCompletion.create(
        model="gpt-4o",  # Bruk riktig chat-modell
        messages=[{"role": "system", "content": "Du er en lærerassistent som hjelper med å kategorisere tekster."},
                  {"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=100
    )
    
    # Returner bare kategorien uten ekstra tekst
    kategori = response['choices'][0]['message']['content'].strip()
    return kategori
    
    print(kategori)

# Funksjon for å vurdere novelle basert på vurderingspunktene
def vurder_novelle(novelle_tekst):

    # Først bestemmer vi om novellen tilhører riktig kategori

    kategori = bestem_kategori(novelle_tekst)

    print(f"Kategorien som ble valgt er: {kategori}")

 

    # Hvis kategorien er 'novelle', går vi videre med vurdering

    if kategori.lower() == 'novelle':

        delimiter = "####"
        gjennomtenkt ="Ser du denne variabelen, tenk nøye og forsiktig igjennom hva som blir spurt" 

        vurderingsinstruksjon = f"""Vurder novellen basert på følgende steg.
        Hvert steg er adskilt av fire hashtags ({delimiter}).


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
            Hvis innholdet vurders som INGEN VURDERING.

        Uthev karakteren i fet skrift, hvis du gir vurdering.

        Bruk følgende format format:
        Pre-steg: :{delimiter} <pre-stegresonnering>
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
        return vurdering
    else:
        return "Denne teksten er ikke en novelle, og kan ikke vurderes som sådan."


# Streamlit UI
st.title("Lærerassistent for Novellevurdering")
st.write("Last opp en novelle eller lim inn teksten nedenfor for å få en vurdering.")

# Tekstinput
novelle_tekst = st.text_area("Lim inn novelle her", height=300)

if st.button("Vurder Novelle"):
    if novelle_tekst.strip():
        with st.spinner("Vurderer novellen, vennligst vent..."):
            resultat = vurder_novelle(novelle_tekst)
        st.subheader("Vurdering:")
        st.write(resultat)
    else:
        st.error("Vennligst lim inn en novelle for å fortsette.")



# Eksempel på en novelle (kan være en kort tekst)
novelle_tekst = """
En vintermorgen i byen Kaldt, stille. Den grå himmelen hang tungt over byen, som om den prøvde å holde på alle minnene om tapt lys. Maren trakk frakken tett rundt kroppen og håpet på at de varme kaffebølgene som steg fra koppen i hånden hennes, skulle varme hele henne, ikke bare hendene. Men det var noe annet i luften den dagen, noe annet enn bare vinterens bitende kulde. \
Hun hadde alltid elsket denne tiden på året. Ikke nødvendigvis fordi vinteren var vakker, men fordi den brakte med seg en følelse av pause. Det var som om verden holdt pusten, og Maren lot seg selv gjøre det samme. Ingen hastverk, ingen forventninger – bare de stille morgenene før byen våknet for alvor. \
Hun satt på en benk i parken. Alle trærne var nakne, grenene strakte seg mot himmelen som utvaskede pensler. Et enslig løv virvlet fra treet nærmest henne og landet på bakken foran benken, som om det visste at det ville forsvinne snart. Hun rakte ut hånden og tok det, følte den tynne, sprø overflaten som om det var et minne som var i ferd med å visne bort. \
Hun visste at hun burde dra hjem, at hun burde begynne på dagen, men hun hadde ikke lyst. Tankene hennes fløt bort fra henne, og hun kunne nesten ikke huske hva det var hun skulle gjøre først. Så hørte hun et kjent steg bak seg. En lav, rolig lyd, som om noen bevisst gikk sakte. Hun kjente igjen trinnene, men det var først da hun snudde seg at hun så ham. \
Anders.De hadde ikke snakket på lenge. Måneder, kanskje. Livet hadde dratt dem i forskjellige retninger, men han sto der, rett foran henne, med et lett smil som ikke helt nådde øynene hans. Noen ganger virket det som om han aldri hadde vært borte, og andre ganger føltes det som om han hadde vært fraværende i en evighet. \
«Hei,» sa han, og stemmen hans var akkurat som hun husket - rolig, men med en liten usikkerhet som hun aldri hadde forstått før. Maren svarte med et nikk, men ordene satt fast i halsen. Hun visste ikke hva hun skulle si.«Det er kaldt i dag,» sa han, og lente seg litt framover, som om han ventet på noe fra henne. Hun lo svakt, men det føltes som om latteren ikke passet i den kalde luften. \
«Ja,» svarte hun, og hun visste ikke om hun svarte på været, eller på den tausheten som hadde vært mellom dem så lenge. De stod der en stund, i stillheten som bare gamle kjente kan dele. Uten at de sa mye, hadde de vært nære. De hadde gått gjennom så mye sammen før, men nå var alt forandret. Maren visste ikke om det var tiden som hadde endret dem, eller om det var alt det usagte. \
«Jeg tenkte på deg i går,» sa Anders plutselig. Øynene hans møtte hennes, og det var som om han ventet på et svar, men hun visste ikke hva hun skulle si. Hun visste bare at denne vintermorgenens stillhet føltes merkelig god, merkelig nok. Kanskje var det på tide å si det de begge hadde unngått i så lang tid. Eller kanskje det var på tide å bare la alt stå som det var. Maren klemte det visne bladet i hånden sin, som om hun holdt på noe verdifullt, som hun kanskje aldri kunne få tilbake. \
"""

# Kall funksjonen for å vurdere novellen
#vurdering = vurder_novelle(novelle_tekst)

# Skriv ut vurderingen
#print(vurdering)


