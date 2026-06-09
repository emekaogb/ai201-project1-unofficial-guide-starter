import pdfplumber

DIRECTORY = "./documents/"
FILE_NAMES = [
        "CMSC131 _ PlanetTerp.pdf",
        "CMSC132 _ PlanetTerp.pdf",
        "CMSC216 _ PlanetTerp.pdf",
        "CMSC250 _ PlanetTerp.pdf",
        "CMSC330 _ PlanetTerp.pdf",
        "CMSC351 _ PlanetTerp.pdf",
        "Schedule of Classes - CMSC1XX.pdf",
        "Schedule of Classes - CMSC2XX.pdf",
        "Schedule of Classes - CMSC3XX.pdf",
        "Schedule of Classes - CMSC4XX.pdf",
    ]

for fn in FILE_NAMES:
    pdf = pdfplumber.open(DIRECTORY + fn)
    text = "\n\n".join(p.extract_text() for p in pdf.pages if p.extract_text())
    # do somehting else here?
