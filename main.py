import openai
from dotenv import load_dotenv
import os

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
        model="gpt-3.5-turbo",  # Bruk riktig chat-modell
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
    # Skriv ut kategorien som ble valgt
    print(f"Kategorien som ble valgt er: {kategori}")

    # Hvis kategorien er 'novelle', går vi videre med vurdering
    if kategori.lower() == 'novelle':
        vurderingspunkter = [
            "Fortellerteknikk:",
            "Perspektiv: Er novellen skrevet i første, andre eller tredje person? Hvordan påvirker valget av perspektiv leserens forståelse av historien?",
            "Fortellerens pålitelighet og subjektivitet: Er fortelleren pålitelig eller ikke? Hvordan påvirker dette handlingen?",
            "Struktur: Er novellen godt strukturert med en tydelig begynnelse, midtdel og avslutning? Hvordan er overgangen mellom disse delene?",
            "Tema og budskap:",
            "Er temaet tydelig, og hvordan blir det utforsket gjennom novellen? Dette kan være alt fra kjærlighet, ensomhet, identitet, til samfunnskritikk.",
            "Budskapet: Hva prøver forfatteren å formidle til leseren gjennom novellen? Hvordan blir dette kommunisert?",
            "Karakterer:",
            "Karakterutvikling: Hvordan utvikler karakterene seg gjennom novellen? Er de realistiske og komplekse?",
            "Relasjoner: Hvordan påvirker relasjonene mellom karakterene historien og temaet?",
            "Språk og stil:",
            "Bruken av språk: Er språket passende for novellen og dens tema? Er det kreativt, presist eller poetisk?",
            "Bildebruk og symbolikk: Brukes metaforer, symboler eller andre litterære teknikker for å underbygge temaet?",
            "Plott og konflikter:",
            "Er plottet engasjerende og troverdig? Hvordan utvikler konflikten seg gjennom novellen, og hvordan løses den?",
            "Er det noen uventede vendinger eller overraskelser som holder på leserens interesse?",
            "Originalitet:",
            "Er novellen original? Bidrar den med noe nytt eller interessant innenfor sin sjanger?",
            "Rettskriving og grammatikk:",
            "Er det noen stavefeil eller grammatiske feil som trekker ned den tekniske kvaliteten på novellen?"
            
        ]
        
        # Bygg opp en prompt for å vurdere novellen basert på de nevnte punktene
        full_prompt = f"Vurder novellen basert på følgende punkter:\n\n"
        for punkt in vurderingspunkter:
            full_prompt += f"{punkt}\n"

        full_prompt += f"\nHer er novellen:\n\n{novelle_tekst}\n\nVennligst gi en detaljert vurdering av novellen basert på disse punktene."

        # Bruk OpenAI for å vurdere novellen
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Bruk riktig chat-modell
            messages=[{"role": "system", "content": "Du er en lærerassistent som hjelper med å vurdere tekster."},
                      {"role": "user", "content": full_prompt}],
            temperature=0.7,
            max_tokens=1500  # Øk max_tokens for å få plass til en detaljert vurdering
        )

        vurdering = response['choices'][0]['message']['content'].strip()
        return vurdering
    else:
        return "Denne teksten er ikke en novelle, og kan ikke vurderes som sådan."


# Eksempel på en novelle (kan være en kort tekst)
novelle_tekst = """
En vintermorgen i byen Kaldt, stille. Den grå himmelen hang tungt over byen, som om den prøvde å holde på alle minnene om tapt lys. Maren trakk frakken tett rundt kroppen og håpet på at de varme kaffebølgene som steg fra koppen i hånden hennes, skulle varme hele henne, ikke bare hendene. Men det var noe annet i luften den dagen, noe annet enn bare vinterens bitende kulde. \
Hun hadde alltid elsket denne tiden på året. Ikke nødvendigvis fordi vinteren var vakker, men fordi den brakte med seg en følelse av pause. Det var som om verden holdt pusten, og Maren lot seg selv gjøre det samme. Ingen hastverk, ingen forventninger – bare de stille morgenene før byen våknet for alvor. \
Hun satt på en benk i parken. Alle trærne var nakne, grenene strakte seg mot himmelen som utvaskede pensler. Et enslig løv virvlet fra treet nærmest henne og landet på bakken foran benken, som om det visste at det ville forsvinne snart. Hun rakte ut hånden og tok det, følte den tynne, sprø overflaten som om det var et minne som var i ferd med å visne bort. \
Hun visste at hun burde dra hjem, at hun burde begynne på dagen, men hun hadde ikke lyst. Tankene hennes fløt bort fra henne, og hun kunne nesten ikke huske hva det var hun skulle gjøre først. Så hørte hun et kjent steg bak seg. En lav, rolig lyd, som om noen bevisst gikk sakte. Hun kjente igjen trinnene, men det var først da hun snudde seg at hun så ham. \
Anders.De hadde ikke snakket på lenge. Måneder, kanskje. Livet hadde dratt dem i forskjellige retninger, men han sto der, rett foran henne, med et lett smil som ikke helt nådde øynene hans. Noen ganger virket det som om han aldri hadde vært borte, og andre ganger føltes det som om han hadde vært fraværende i en evighet. \
«Hei,» sa han, og stemmen hans var akkurat som hun husket – rolig, men med en liten usikkerhet som hun aldri hadde forstått før. Maren svarte med et nikk, men ordene satt fast i halsen. Hun visste ikke hva hun skulle si.«Det er kaldt i dag,» sa han, og lente seg litt framover, som om han ventet på noe fra henne. Hun lo svakt, men det føltes som om latteren ikke passet i den kalde luften. \
«Ja,» svarte hun, og hun visste ikke om hun svarte på været, eller på den tausheten som hadde vært mellom dem så lenge. De stod der en stund, i stillheten som bare gamle kjente kan dele. Uten at de sa mye, hadde de vært nære. De hadde gått gjennom så mye sammen før, men nå var alt forandret. Maren visste ikke om det var tiden som hadde endret dem, eller om det var alt det usagte. \
«Jeg tenkte på deg i går,» sa Anders plutselig. Øynene hans møtte hennes, og det var som om han ventet på et svar, men hun visste ikke hva hun skulle si. Hun visste bare at denne vintermorgenens stillhet føltes merkelig god, merkelig nok. Kanskje var det på tide å si det de begge hadde unngått i så lang tid. Eller kanskje det var på tide å bare la alt stå som det var. Maren klemte det visne bladet i hånden sin, som om hun holdt på noe verdifullt, som hun kanskje aldri kunne få tilbake. \
"""

# Kall funksjonen for å vurdere novellen
vurdering = vurder_novelle(novelle_tekst)

# Skriv ut vurderingen
print(vurdering)
