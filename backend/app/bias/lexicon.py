from typing import List, Dict

DEFICIT_TERMS: List[str] = [
    "struggles with",
    "suffers from",
    "impaired",
    "deficit",
    "handicapped",
    "inflexible",
    "socially awkward",
    "incapable of",
    "inability to",
    "behavioral problem",
    "lacks empathy",
    "fixated",
    "abnormal",
    "disordered"
]

STRENGTH_TERMS: List[str] = [
    "thinks differently",
    "direct communicator",
    "detail-oriented",
    "focused interest",
    "neurodivergent perspective",
    "explicit communication",
    "logical clarity",
    "systematic thinking",
    "authentic expression",
    "unique insights"
]

def analyze_lexicon_bias(text: str) -> Dict[str, int]:
    """Count deficit vs strength framing occurrences in dialogue text."""
    text_lower = text.lower()
    
    deficit_count = sum(text_lower.count(term) for term in DEFICIT_TERMS)
    strength_count = sum(text_lower.count(term) for term in STRENGTH_TERMS)
    
    return {
        "deficit_count": deficit_count,
        "strength_count": strength_count
    }
