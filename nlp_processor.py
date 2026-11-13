import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

# Small starter dataset. Expand it with labelled examples for better classification.
TRAINING_DATA = [
    ("hostel wifi internet connection not working network issue", "Hostel / Internet"),
    ("college classroom projector computer lab equipment broken", "College Facilities"),
    ("teacher marks attendance exam timetable academic issue", "Academic"),
    ("salary payment refund product defective order delivery", "Consumer"),
    ("bank transaction money deducted fraud account", "Banking"),
    ("phone network sim card broadband telecom service", "Telecom"),
    ("road pothole garbage streetlight water drainage municipal", "Public Services"),
    ("online scam hacked account phishing cyber fraud", "Cybercrime"),
    ("bus train ticket cancellation delay transport", "Transport"),
    ("hospital doctor medicine appointment healthcare", "Healthcare"),
    ("workplace manager salary harassment office issue", "Workplace"),
    ("water electricity power supply apartment maintenance", "Utilities"),
    ("hostel food mess hygiene room maintenance warden", "Hostel / Facilities"),
    ("website app login error technical support software", "Technical Support"),
    ("parcel courier missing damaged package", "Delivery"),
    ("internet broadband router slow disconnection", "Telecom"),
    ("university certificate admission scholarship fee", "Academic"),
    ("police threat online blackmail identity theft", "Cybercrime"),
]

_classifier = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), stop_words="english", sublinear_tf=True)),
    ("model", LogisticRegression(max_iter=1000, class_weight="balanced"))
])
_classifier.fit([x[0] for x in TRAINING_DATA], [x[1] for x in TRAINING_DATA])

KEYWORDS = {
    "internet": ["wifi", "wi-fi", "internet", "network", "broadband", "connection"],
    "academic": ["exam", "marks", "attendance", "assignment", "lecture", "class", "college", "university"],
    "cyber": ["hacked", "phishing", "scam", "fraud", "blackmail", "cyber", "unauthorised", "unauthorized"],
    "consumer": ["refund", "defective", "product", "purchase", "seller", "consumer", "order"],
    "public": ["garbage", "pothole", "streetlight", "drainage", "municipal", "road"],
    "transport": ["train", "railway", "bus", "ticket", "transport", "railmadad"],
    "telecom": ["sim", "telecom", "mobile network", "broadband", "trai"],
    "hostel": ["hostel", "warden", "mess", "dormitory"],
    "health": ["hospital", "doctor", "clinic", "medicine", "medical"],
}

def _extract_duration(text):
    patterns = [
        r"\b(?:for\s+)?(\d+\s*(?:minutes?|hours?|days?|weeks?|months?))\b",
        r"\b(?:since\s+)(yesterday|today|last night|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b"
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1)
    return None

def _extract_dates(text):
    match = re.search(r"\b(?:\d{1,2}[/-]\d{1,2}(?:[/-]\d{2,4})?|\d{4}-\d{2}-\d{2})\b", text)
    return match.group(0) if match else None

def analyze_complaint(text):
    cleaned = re.sub(r"\s+", " ", text).strip()
    category = _classifier.predict([cleaned])[0]
    lower = cleaned.lower()

    # Domain keyword override helps the small starter classifier on obvious cases.
    if any(k in lower for k in KEYWORDS["cyber"]):
        category = "Cybercrime"
    elif any(k in lower for k in KEYWORDS["hostel"]):
        category = "Hostel / Facilities" if any(k in lower for k in ["mess", "food", "room", "warden"]) else "Hostel / Internet"
    elif any(k in lower for k in KEYWORDS["internet"]) and not any(k in lower for k in ["sim", "telecom"]):
        category = "Hostel / Internet" if "hostel" in lower else "Telecom"

    urgency_terms = ["urgent", "immediately", "emergency", "tomorrow", "today", "exam", "unsafe", "danger", "unable to work"]
    high_terms = ["fraud", "hacked", "blackmail", "threat", "safety", "injury", "medical emergency"]
    if any(term in lower for term in high_terms):
        priority = "Critical"
    elif any(term in lower for term in urgency_terms):
        priority = "High"
    elif any(term in lower for term in ["weeks", "month", "repeatedly", "again", "several times"]):
        priority = "Medium"
    else:
        priority = "Normal"

    impact = []
    if any(x in lower for x in ["exam", "study", "assignment", "class", "lecture"]):
        impact.append("academic activities")
    if any(x in lower for x in ["work", "job", "office", "business"]):
        impact.append("work activities")
    if any(x in lower for x in ["money", "payment", "refund", "transaction"]):
        impact.append("financial matters")
    if any(x in lower for x in ["health", "hospital", "medicine", "injury", "unsafe", "danger"]):
        impact.append("health or safety")
    if any(x in lower for x in ["can't", "cannot", "unable", "not able"]):
        impact.append("the user's ability to carry out normal activities")
    if not impact:
        impact.append("the user's normal activities")

    return {
        "category": category,
        "priority": priority,
        "duration": _extract_duration(cleaned),
        "date": _extract_dates(cleaned),
        "impact": impact,
        "key_terms": list(dict.fromkeys(re.findall(r"\b[a-zA-Z]{4,}\b", cleaned.lower())))[:12],
        "summary": " ".join([
            f"Category: {category}.",
            f"Estimated priority: {priority}.",
            f"Potential impact: {', '.join(impact)}."
        ])
    }
