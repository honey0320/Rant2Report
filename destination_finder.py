def recommend_destinations(category, complaint):
    text = complaint.lower()
    results = []

    if category == "Cybercrime" or any(w in text for w in ["hacked", "phishing", "cyber fraud", "online blackmail"]):
        results.append({
            "name": "National Cyber Crime Reporting Portal",
            "description": "For reporting cybercrime in India. For financial cyber fraud, contact the helpline promptly.",
            "url": "https://www.cybercrime.gov.in/",
            "helpline": "1930 (financial cyber fraud)"
        })
    elif category == "Consumer":
        results.append({
            "name": "National Consumer Helpline",
            "description": "For consumer grievances involving products and services.",
            "url": "https://consumerhelpline.gov.in/",
            "helpline": "1915"
        })
    elif category in ["Hostel / Internet", "Hostel / Facilities", "Academic", "College Facilities"]:
        results.append({
            "name": "Institutional grievance cell",
            "description": "Contact the college or university grievance cell, hostel administration, or the relevant department first.",
            "url": "https://www.ugc.gov.in/",
            "helpline": "Check your institution's official contact details"
        })
        results.append({
            "name": "UGC e-Samadhan",
            "description": "University Grants Commission grievance redressal platform, where applicable.",
            "url": "https://samadhaan.ugc.ac.in/",
            "helpline": "Use the portal for current contact options"
        })
    elif category == "Telecom":
        results.append({
            "name": "TRAI Consumer Information",
            "description": "Review the telecom complaint process; first approach your service provider's complaint centre.",
            "url": "https://www.trai.gov.in/consumer-info",
            "helpline": "Contact your operator first"
        })
    elif category == "Transport":
        results.append({
            "name": "RailMadad",
            "description": "For complaints and assistance related to Indian Railways.",
            "url": "https://railmadad.indianrailways.gov.in/",
            "helpline": "Use the portal for current assistance"
        })
    elif category == "Public Services":
        results.append({
            "name": "CPGRAMS",
            "description": "For eligible grievances concerning central government public services.",
            "url": "https://pgportal.gov.in/",
            "helpline": "See portal guidance"
        })
    else:
        results.append({
            "name": "Relevant organisation's grievance channel",
            "description": "Submit the report to the official customer support, grievance officer, or responsible department.",
            "url": "https://www.india.gov.in/",
            "helpline": "Check the organisation's official website"
        })

    return results
