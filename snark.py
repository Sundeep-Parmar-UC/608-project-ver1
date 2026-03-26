# given Remark type needed 1) first move  2) general move  3)Black won 4) UniqueMovePosition 5)Illegal Move
# given SnarkLevel : off, neutral, positive, evil
# given MoveNumber

# prepare API remark statement
# pre-defined remark types
dict_RemarkType = {
    "start": "This is the first pair moves of the game.",
    "general_move": "This is a normal mid‑game move.",
    "illegal_move": "The move played is illegal.",
    "Wend": "The human player won the game, AI is defeated",
    "Bend": "AI has won the game",
    "Uend": "The game is reached a unique position and cannot be played further",
    
}

#pre-defined snark levels
dict_SnarkLevel= {
    #"off": "No snark. Respond with an empty string.",
    "neutral": "Respond with a neutral, factual tone.",
    "positive": "Respond with a friendly, encouraging tone.",
    "evil": "Respond with a slightly arrogant, mocking, evil-humor, or snarky tone.",
}

#connect to Google Gemini API
import google.generativeai as genai


genai.configure(api_key="AIzaSyD1lonYSXcoD0Yl6JuJ4asjEFttrPNj29I")
model = genai.GenerativeModel("gemini-3.1-flash-lite-preview")

# return remark text
def snark(RemarkType, SnarkLevel, MoveNumber):
    #if snark is off, return empty string
    if SnarkLevel == "off":  
        return ""

    #lookup RemarkType and SnarkLevel from dict, if not exist, fallback on the quotes as stated
    remark_context = dict_RemarkType.get(RemarkType, "General chess remark as if bot played responding move")
    snark_tone = dict_SnarkLevel.get(SnarkLevel, "Respond in a neutral tone.")

    #call Gemini
    prompt = (
        "Give me a single short chess remark based somewhat on the following:\n"
        f"- Snark level: {SnarkLevel}\n"
        f"- Remark type: {RemarkType}\n"
        f"- Meaning: {remark_context}\n"
        f"- Tone instruction: {snark_tone}\n"
        f"- Move number: {MoveNumber}\n"
        "Keep it short (1–2 sentences). Do not explain chess rules."
    )

    RemarkText = model.generate_content(prompt)
    return RemarkText.text


    #snark remark level: 
            #low(every 10 moves, ~starting+2+ending = 4), 
            #medium(every 3 move, ~8+2 =10 remarks), 
            #high(every move)
