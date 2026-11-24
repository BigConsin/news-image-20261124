# Story data for Tuesday 24 November 2026 — verified against Reuters / AP /
# AFP / Al Jazeera / Xinhua / ESPNcricinfo items dated 2026-11-24.
# Numbers with known source conflicts use % moves or the fuller breakdown.
RED = (178, 26, 26); NAVY = (18, 38, 74); GOLD = (196, 138, 20); ORANGE = (214, 106, 20)
TEAL = (14, 110, 120); GREEN = (18, 110, 60); PURPLE = (96, 52, 140); GREY = (96, 92, 84)

DATE_LONG = "Tuesday 24 November 2026"
TOTAL = 36
REGIONS = 7
SUBLINE = "Sanofi's $41bn Insmed deal  •  Kremlin shuts Europe out of Ukraine talks  •  Chip rally unwinds"
DATA = [
    ("$41bn", "Sanofi-Insmed deal, $175/share", RED),
    ("103.3", "US confidence, near-2-year high", NAVY),
    ("175", "migrants missing off Senegal", GOLD),
    ("$237.5bn", "Venezuela debt = 242% of GDP", TEAL),
    ("699", "drones Russia says it downed", RED),
    ("-4.4%", "Nvidia, after +31.5% Monday", ORANGE),
]
REGION_BAR = [("EUROPE", 10, NAVY), ("MIDDLE EAST", 6, RED), ("ASIA", 5, TEAL),
              ("AMERICAS", 8, GREEN), ("AFRICA", 4, GOLD), ("OCEANIA", 1, PURPLE), ("WORLD", 2, GREY)]
TIMELINE = [("09:51", "Zaporizhzhia toll"), ("10:25", "France rare earths"), ("12:03", "UK sanctions Houthis"),
            ("13:18", "Nigeria budget"), ("16:15", "Congo $965m"), ("17:47", "Yemen strike toll")]
LEADS = [
    {"n": 1, "kicker": "RALLY UNWINDS", "loc": "NEW YORK  •  MARKETS",
     "head": "Chip rally unwinds: Nvidia slips after Monday's 31.5% surge",
     "body": "Futures fell Tuesday: Nasdaq 100 -1.11%, S&P 500 -0.46%. Micron, AMD and Marvell lost 3.3-4.3% premarket. (Reuters)",
     "body_long": "The chip rally that powered Monday's surge ran out of road before the opening bell. Nvidia, up 31.5% a day earlier, fell 4.4% in premarket trade, and the suppliers behind it followed: Micron, AMD and Marvell lost between 3.3% and 4.3%. Nasdaq 100 futures slid 1.11% and S&P 500 futures 0.46%. By the close in Europe the selling had spread: the Stoxx 600 ended 0.66% lower and Infineon fell 10%.",
     "art": "rally", "cert": "REPORTED"},
    {"n": 2, "kicker": "$41BN DEAL", "loc": "PARIS  •  PHARMA",
     "head": "Sanofi buys US drugmaker Insmed for $41bn in cash",
     "body": "$175 a share, 46% above the pre-rumour price, in 2026's biggest pharma deal. Insmed jumped 14% to $170.39. (Reuters)",
     "body_long": "Sanofi agreed to buy the American drugmaker Insmed for $41 billion in cash, the largest pharmaceutical takeover of 2026. The French group will pay $175 a share, 46% above the price before rumours of a deal. Insmed's stock jumped 14% to $170.39 as the terms emerged.",
     "art": "deal", "cert": "REPORTED"},
    {"n": 3, "kicker": "DAWN STRIKE", "loc": "ZAPORIZHZHIA, UKRAINE  •  WAR",
     "head": "Russian strike kills 2, wounds 40+ in Zaporizhzhia",
     "body": "Dawn raid destroyed a house and damaged flats; a baby is among the wounded. Kyiv says Russia launched 96 drones. (AFP)",
     "body_long": "A Russian strike at dawn destroyed a house and damaged blocks of flats in Zaporizhzhia, killing two people and wounding more than 40, among them a baby. Kyiv said Russia launched 96 drones in the overnight attack; the toll was still being counted as rescuers worked through the morning.",
     "art": "strike", "cert": "REPORTED"},
]
MIDS = [
    {"n": 4, "kicker": "TALKS", "loc": "MOSCOW",
     "head": "Kremlin: Europe adds 'no value' to Ukraine talks",
     "body": "Peskov: no date set for the next Abu Dhabi round. Berlin replies: 'only Putin is not ready.'", "art": "mic2"},
    {"n": 5, "kicker": "GAZA STRIKES", "loc": "GAZA CITY",
     "head": "Strikes kill 7 in Gaza, incl. Hamas security chief",
     "body": "Health ministry puts the war toll at 74,746 dead. Meningitis cases hit 272 in Oct, 8x normal.", "art": "gaza"},
    {"n": 6, "kicker": "175 MISSING", "loc": "DAKAR, SENEGAL",
     "head": "175 migrants missing as Dakar boat loses contact",
     "body": "Boat left Yoff about Nov 9-10. Over 8,000 reached the Canaries in November's first 12 days.", "art": "boat2"},
    {"n": 7, "kicker": "PROBE", "loc": "BEIJING, CHINA",
     "head": "China investigates Politburo member Chen Jining",
     "body": "Shanghai's party chief is the 4th member of the top body probed since 2025, Xinhua says.", "art": "gavel"},
    {"n": 8, "kicker": "103.3", "loc": "WASHINGTON, US",
     "head": "Consumer confidence jumps to a near-2-year high",
     "body": "Index leaps 11.4 points from 91.9, beating the 92.5 forecast, after the midterms.", "art": "conf"},
    {"n": 9, "kicker": "TARIFFS", "loc": "WASHINGTON, US",
     "head": "New tariffs loom after probe of 16 trade partners",
     "body": "Section 301 'excess capacity' findings due Tue/Wed; duties would stack on Trump's existing levies.", "art": "tariff"},
    {"n": 10, "kicker": "242% OF GDP", "loc": "CARACAS, VENEZUELA",
     "head": "Venezuela puts its debt at $237.5bn in new framework",
     "body": "First full picture in years; Caracas sees the economy doubling to $200.9bn within five years.", "art": "debt"},
    {"n": 11, "kicker": "T20 CRICKET", "loc": "AUSTRALIA",
     "head": "England rout Australia to level the T20 series 1-1",
     "body": "Donald 85 off 32, Salt 58: England chase 185 in 13.1 overs, reaching 188-2 with 41 balls left.", "art": "cricket2"},
    {"n": 12, "kicker": "$965M", "loc": "KINSHASA, DR CONGO",
     "head": "Congo mining forum unveils $965m in financing",
     "body": "Investment announced as the Makutano Mining Forum opens in the capital. (Reuters, 16:15)", "art": "mine2"},
    {"n": 13, "kicker": "OIL ROW", "loc": "BAGHDAD, IRAQ",
     "head": "PM orders takeover of Kurdistan border crossings",
     "body": "Federal body to run all crossings; oil ministry to manage fields in 4 provinces after smuggling probe.", "art": "oil2"},
]
PINS = [(1, 0.145, 0.28), (2, 0.485, 0.23), (3, 0.55, 0.25), (4, 0.565, 0.20), (5, 0.578, 0.365),
        (6, 0.445, 0.475), (7, 0.775, 0.35), (8, 0.175, 0.345), (9, 0.125, 0.375), (10, 0.235, 0.605),
        (11, 0.885, 0.79), (12, 0.525, 0.605), (13, 0.618, 0.325)]
ALSO_TITLE = "ALSO ON TUESDAY 24 NOVEMBER 2026"
ALSO = [
    {"n": 14, "where": "Kyiv", "text": "Ukraine needs $125bn support in 2027 (Reuters)"},
    {"n": 15, "where": "Moscow", "text": "Putin vows revenge for refinery strikes (Reuters)"},
    {"n": 16, "where": "London", "text": "UK sanctions Houthis + 4 officials (Reuters)"},
    {"n": 17, "where": "Aden", "text": "Houthis 60 km from Aden; city 'won't fall' (Reuters)"},
    {"n": 18, "where": "Lahj, Yemen", "text": "bus and truck strike kills 26 (AFP)"},
    {"n": 19, "where": "Hormuz", "text": "IRGC claims 3 tankers hit mines [CLAIM]"},
    {"n": 20, "where": "Munich", "text": "German Ifo morale up to 90.6, 7th rise (Reuters)"},
    {"n": 21, "where": "Hambach", "text": "BYD in exclusive talks for Ineos plant (Reuters)"},
    {"n": 22, "where": "Paris", "text": "France to stockpile rare earths (Reuters)"},
    {"n": 23, "where": "Frankfurt", "text": "Stoxx 600 -0.66%, DAX -1.3% at close (Reuters)"},
    {"n": 24, "where": "London", "text": "oil 3-month low: Brent $88.62, -0.8% (Reuters)"},
    {"n": 25, "where": "Abuja", "text": "Tinubu seeks budget cut to $48bn (Reuters)"},
    {"n": 26, "where": "Brasilia", "text": "Lula backs 2nd fiscal package (Reuters)"},
    {"n": 27, "where": "Eskisehir", "text": "AS-532 helicopter crashes in Turkiye (Reuters)"},
    {"n": 28, "where": "New York", "text": "Anthropic below $83 IPO price, at $82 (Reuters)"},
    {"n": 29, "where": "Washington", "text": "Schumer accuses Huang; testifies Dec 3 (Reuters)"},
    {"n": 30, "where": "Serang", "text": "candy factory fire toll rises to 26 (AFP)"},
    {"n": 31, "where": "Lausanne", "text": "CAS restores Senegal's AFCON title (Reuters)"},
    {"n": 32, "where": "Taipei", "text": "Asia markets rebound: Taiwan +9.1% (Reuters)"},
    {"n": 33, "where": "Jiuquan", "text": "Pakistani pilot joins Shenzhou-24 crew (AFP)"},
    {"n": 34, "where": "Doha", "text": "Pakistan A beat Nepal by 96 runs (cricket)"},
    {"n": 35, "where": "Washington", "text": "US to host Copa America 2028 (Reuters)"},
    {"n": 36, "where": "Yakima, US", "text": "WHO: 3 H5N1 cases, 1 death (Reuters)"},
]
DATE_CHECK = ("Every numbered story happened, or was first reported, on Tuesday 24 November 2026. Left out as earlier news: "
              "Monday's Nvidia rally itself, the COP31 collapse (Sun 22) and Sunday's sinking of the Merkury off Libya. #19 is one side's claim.")
SOURCES = "Sources: Reuters, AP, AFP, Al Jazeera, Xinhua and the day's wires, as tagged beside each story"
