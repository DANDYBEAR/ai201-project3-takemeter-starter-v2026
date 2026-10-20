#!/usr/bin/env python3
"""Apply reviewed TakeMeter labels by one-based CSV row number."""

import csv
from pathlib import Path


PATH = Path(__file__).with_name("labels.csv")

# The first 20 were labelled cold, before assisted pre-labelling began.
LABELS: dict[int, tuple[str, str]] = {
    1: ("open_question", "cold"),
    2: ("position", "cold; hard case: position vs worked_request; asks HN to add a feature rather than asking readers for advice"),
    3: ("open_question", "cold"),
    4: ("position", "cold"),
    5: ("worked_request", "cold"),
    6: ("case_report", "cold"),
    7: ("worked_request", "cold"),
    8: ("position", "cold"),
    9: ("position", "cold"),
    10: ("worked_request", "cold"),
    11: ("position", "cold; hard case: position vs case_report; the question supplies its own preferred answer and is rhetorical"),
    12: ("worked_request", "cold"),
    13: ("position", "cold"),
    14: ("position", "cold"),
    15: ("case_report", "cold; hard case: case_report vs position; the quoted spam incident supports a genuine request for others' experiences"),
    16: ("open_question", "cold"),
    17: ("worked_request", "cold"),
    18: ("position", "cold"),
    19: ("position", "cold"),
    20: ("worked_request", "cold"),
}

# Rows 21-200 were pre-labelled in batches, then read in full and checked.
ASSISTED: dict[int, str] = {
    21: "worked_request", 22: "worked_request", 23: "case_report",
    24: "case_report", 25: "worked_request", 26: "worked_request",
    27: "position", 28: "open_question", 29: "open_question",
    30: "position", 31: "case_report", 32: "worked_request",
    33: "worked_request", 34: "case_report", 35: "position",
    36: "case_report", 37: "position", 38: "open_question",
    39: "worked_request", 40: "worked_request", 41: "worked_request",
    42: "worked_request", 43: "position", 44: "worked_request",
    45: "worked_request", 46: "position", 47: "worked_request",
    48: "position", 49: "worked_request", 50: "worked_request",
    51: "position", 52: "position", 53: "worked_request",
    54: "position", 55: "position", 56: "open_question",
    57: "worked_request", 58: "worked_request", 59: "case_report",
    60: "position", 61: "worked_request", 62: "worked_request",
    63: "open_question", 64: "case_report", 65: "position",
    66: "worked_request", 67: "worked_request", 68: "position",
    69: "open_question", 70: "worked_request", 71: "worked_request",
    72: "position", 73: "open_question", 74: "worked_request",
    75: "position", 76: "position", 77: "open_question",
    78: "worked_request", 79: "position", 80: "position",
    81: "open_question", 82: "open_question", 83: "position",
    84: "position", 85: "open_question", 86: "worked_request",
    87: "case_report", 88: "worked_request", 89: "worked_request",
    90: "worked_request", 91: "case_report", 92: "worked_request",
    93: "case_report", 94: "open_question", 95: "open_question",
    96: "worked_request", 97: "case_report", 98: "position",
    99: "open_question", 100: "worked_request", 101: "worked_request",
    102: "position", 103: "open_question", 104: "case_report",
    105: "worked_request", 106: "worked_request", 107: "worked_request",
    108: "position", 109: "position", 110: "worked_request",
    111: "open_question", 112: "case_report", 113: "open_question",
    114: "open_question", 115: "open_question", 116: "position",
    117: "worked_request", 118: "open_question", 119: "case_report",
    120: "worked_request", 121: "worked_request", 122: "position",
    123: "position", 124: "open_question", 125: "open_question",
    126: "position", 127: "position", 128: "case_report",
    129: "position", 130: "worked_request", 131: "position",
    132: "position", 133: "case_report", 134: "case_report",
    135: "case_report", 136: "worked_request", 137: "open_question",
    138: "case_report", 139: "case_report", 140: "position",
    141: "case_report", 142: "case_report", 143: "open_question",
    144: "position", 145: "worked_request", 146: "open_question",
    147: "position", 148: "open_question", 149: "worked_request",
    150: "worked_request", 151: "position", 152: "open_question",
    153: "position", 154: "position", 155: "worked_request",
    156: "case_report", 157: "open_question", 158: "position",
    159: "position", 160: "case_report", 161: "worked_request",
    162: "open_question", 163: "position", 164: "open_question",
    165: "worked_request", 166: "open_question", 167: "worked_request",
    168: "worked_request", 169: "position", 170: "case_report",
    171: "position", 172: "worked_request", 173: "case_report",
    174: "position", 175: "worked_request", 176: "open_question",
    177: "open_question", 178: "position", 179: "case_report",
    180: "worked_request", 181: "open_question", 182: "position",
    183: "worked_request", 184: "worked_request", 185: "worked_request",
    186: "open_question", 187: "open_question", 188: "position",
    189: "position", 190: "worked_request", 191: "open_question",
    192: "position", 193: "case_report", 194: "open_question",
    195: "position", 196: "position", 197: "open_question",
    198: "worked_request", 199: "open_question", 200: "open_question",
}

HARD_NOTES = {
    29: "open_question vs position; treated the awareness question as a genuine request because the body does not answer it",
    59: "case_report vs position; the promotional tone did not override the supported request to explain a specific flagging incident",
    60: "position vs open_question; the questions support the author's conclusion rather than seek an answer",
    80: "position vs case_report; the documented overcharge ends in a petition to Anthropic, not a request for reader information",
    93: "case_report vs position; the breach-or-error question is answer-seeking despite the surrounding rant",
    124: "open_question vs position; the consequences question is answer-seeking, though the title also reads as venting",
    148: "open_question vs position; the post states a forecast but genuinely asks what could prevent it",
    156: "case_report vs worked_request; the reproducible delivery failure triggers incident precedence",
    170: "case_report vs open_question; named recent releases make the adoption question about a checkable external change",
    173: "case_report vs position; the legality question is genuine despite the heated closing sentence",
}

REPLACEMENT_184 = """Ask HN: Curious, who can afford to buy in SF?

I've worked in tech now for 15 years, generally \"high paying\". I lived in SF for the first 4 of this years, between 2014-2018 and remember hearing all about how it was us tech workers who were responsible for high home prices.
Fast forward 15 years and despite moving out of the city, and saving as much as I could, I still don't see how I could afford to live in SF.
Honestly it boggles the mind a little bit. I'm motivated, worked supposedly in the right industry, and would love to live there, but it makes zero financial sense whatsoever. WHO can afford these 1.5 - 3.0 ---> 15+ million dollar homes?
At times I wonder, have I just absolutely failed at working in tech? Should I have been pulling $500k a year or something for the last 10 years? I never did work for FANG so maybe thats it? I mean is that it? Work for FANG and you can afford SF? Or what am I missing? 15 years of working and saving and I still couldn't live there."""

BALANCE_REPLACEMENTS = {
    31: """Ask HN: How do swarms of AI agents work?

Andrej Karpathy posted about the growing gap in how people experience AI:
~75% have barely used LLMs
~20% use them casually
~0.2% use frontier models professionally for math and code
~0.00006% have access to frontier systems internally
He writes:
\"And finally we get to the ~5,000 people (~0.00006%) with access to frontier-grade systems internally. The external world has seen the preview. It looks like swarms of thousands of agents collaborating over weeks on software mega projects: minting zero days, running cyber attacks and defenses at machine speeds, discovering new science, advancing the frontier of mathematics.\"
Source: https://x.com/karpathy/status/2109361546505966046
Does anyone have an intuition, or even firsthand experience, of how these swarms of thousands of agents actually work?
I'm already struggling to get 2-3 agents to work together reliably. I can't really wrap my head around how you'd coordinate thousands of them, or what benefits you get from scaling to that many.""",
    64: """Ask HN: What are all my submissions getting flagged

I have tried a couple of time to show HN a open source project I am releasing and got an instant(non human) [flagged] mentioned in the title. I wonder why that is. I have been on HN for a long time and nothing should be suspicious about my account. Any ideas on what could be going on ?""",
    91: """Ask HN: Will Microsoft sue vibe coded wordcraft for copying its Word GUI?

The vibe coded gridcraft also copied the Excel GUI.
Do you think there will be lawsuits for these open source vibe coded apps?
P.S. To try these on macOS:
brew install wordcraft
brew install gridcraft""",
    97: """Ask HN: Locked out of Google despite knowing password and having email access

I'm trying to recover my Google account. I know the password, but unfortunately I've lost access to the phone number where Google keeps trying to send the verification code. It used to just ask me to fill in the missing digits of the number.
I still have access to Gmail through a third-party Android email app, where I can send and receive emails normally, but I can't sign in to my Google account anywhere else. The account is old, I never set up a recovery email and I haven't used it outside the email app for a long time. I've tried various devices, networks, and VPN combinations without success.
Google's own recovery help says:
\"Tip: We may send a verification code to the email address on the account you're trying to recover. This way, you can get the verification code if you have access to your Gmail inbox through a third-party email client or email forwarding.\"
But I've never been offered this option.
After multiple recovery attempts, I eventually got to a step asking for an alternative email address. I provided one and verified the code Google sent, but the final screen told me to reply to my Google support contact. I don't have one.
I found this HN thread where a Google employee (`luka`) helped someone in almost the exact same situation:
https://news.ycombinator.com/item?id=49744286
Unfortunately, I can no longer reply to that thread.
Does anyone know how to get a similar escalation or another way to recover access?""",
    112: """Ask HN: MS Outlook login without an extra email address

I have an email address which is like 16 years old. Microsoft changed their auth process, i gave them my phone number, fingerprint, and solved like 4+ captcha puzzles (lol), and now it asks for a secondary email address too confirm. I cannot get any further and cannot read my email now! There is some irony in needing another email address to access my email address, and it makes me want to leave as soon as possible. Would be helpful if I can access my email I am using for more than a decade. Do more people experienced this, and maybe found a way to login without an extra email address?""",
    119: """Ask HN: Fake abuse reports keep auto-blocking my site on Cloudflare

I run a small site on Cloudflare's Pro plan. Since 26 September, someone has filed the same fake abuse report against it six times. Each time, Cloudflare automatically puts a \"Suspected Malware\" warning on my homepage and login pages, and it stays until a person reviews it.
The reports are word for word identical. They describe an \"order\" and product pages that have never existed on my site (they return 404). The file hash in the report doesn't match the hash in its own VirusTotal link, which returns \"Item not found\". Only the date changes, and twice it's been misspelled (\"October 52026\", \"Octoboer 8 2026\"). Cloudflare's team has cleared four of them. The reporter pastes the same text again within a day.
The result is that my homepage has been blocked for most of two weeks, my traffic has halved, and Google is indexing the warning page instead of my site. I've opened support cases and requested reviews each time. I've had one reply, on 5 October, and nothing on a lasting fix.
I'm not asking for special treatment. I'd like to know:
1. Is there a way to stop automatic mitigations from a reporter or text that has already been shown to be false?
2. Is there a manual-review setting for a domain?
3. Has anyone else seen the abuse form used like this, and how did it end?
The same problem is described in my open case with Cloudflare (#02370521). Thanks for any pointers, and if anyone from Cloudflare's abuse team reads this, I'd welcome a reply.""",
    128: """Ask HN: Have you checked REA(reverse engineer anything) GitHub repo?

Hi members, I just came across a lot of X posts where they are talking about REA repository and that IP and software rights are almost worthless. Have you tried it ? What's your take on it ?""",
}


def main() -> None:
    with PATH.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    missing = sorted(set(LABELS) - set(range(1, len(rows) + 1)))
    if missing:
        raise ValueError(f"Mappings outside CSV: {missing}")

    rows[183]["text"] = REPLACEMENT_184
    for number, replacement in BALANCE_REPLACEMENTS.items():
        rows[number - 1]["text"] = replacement

    for number, label in ASSISTED.items():
        note = "pre-labelled, checked"
        if number in HARD_NOTES:
            note += f"; hard case: {HARD_NOTES[number]}"
        if number == 184:
            note += "; replaced a near-duplicate during review"
        if number in BALANCE_REPLACEMENTS:
            note += "; collected after balance check to strengthen case_report"
        LABELS[number] = (label, note)

    for number, (label, note) in LABELS.items():
        rows[number - 1]["label"] = label
        rows[number - 1]["note"] = note

    with PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["text", "label", "note"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"Applied {len(LABELS)} reviewed labels")


if __name__ == "__main__":
    main()
