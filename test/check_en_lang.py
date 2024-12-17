import unicodedata
import string

chunks = [
    "Full on auto!\nGot this team on auto and got full stars!The content is sourced from the Lineup Assistant tool. Click it to view the character and Relic stat details~",
    "Perfect Coin Flip\nKaeya’s idle animations are my favorite!\n\n(I think I was trying to capture Chenyu Vale at a distance, but at least you can see Fontaine from here!",
    "Это так странно, но и так смешно..",
    "噫——伊万,boss装载冲呀芬德boss?",
    """Tips: I'll also be updating this guide in other language regions at the same time, make sure to check out the posts and leave a comment~ Your feedback is greatly appreciated! 



CN|TW|JP|KR |RU


>>>Click to Start Game<<<



Hello, Trailblazers! Today, I bring you a strategy guide for the Apocalyptic Shadow [Gusty Primate]. Hope it helps!"""
]

def is_english(text):
    unicode_punctuation = [' ','«','»','¿','‐','‑','‒','–','—','―','‖','‘','’','“','”','†','‡','•','…','‰','′','″','※','‼','⁇','⁈','⁉','₠','₡','₢','₣','₤','₥','₦','₧','₨','₩','₪','₫','€','₹','∀','∂','∃','∅','∇','∈','∉','∋','∑','−','√','∞','∠','∧','∨','∩','∪','　','、','。','〃','々','〈','〉','《','》','「','」','『','』','【','】','〔','〕','〖','〗','〜','！','＂','＃','＄','％','＆','＇','（','）','＊','＋','，','－','．','／','：','；','＜','＝','＞','？','＠','︰','︱','︳','﹉','﹐','﹑','﹒','﹔','﹕','﹖','﹗','｡','｢','｣','､','･']
    allowed = string.ascii_letters + string.digits + string.punctuation + string.whitespace
    allowed_list = list(allowed) + unicode_punctuation
    return all(char in allowed_list for char in text)

# for chunk in chunks:
#     chunk = unicodedata.normalize('NFKD', chunk).encode('ASCII', 'ignore').decode('ASCII')
#     print(chunk)
#     for char in chunk:
#         if char not in (string.ascii_letters + string.digits + string.punctuation + string.whitespace):
#             print(f"Unexpected character: {char!r} (Unicode: U+{ord(char):04X})")


print([is_english(chunk) for chunk in chunks])