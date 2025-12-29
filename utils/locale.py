def detect_language(text: str) -> str:
    t = text.lower()
    tr_markers = ["ben", "vardı", "burada", "eskiden", "yok", "ama", "hiç", "ve"]
    en_markers = ["there", "used", "here", "was", "i ", "but", "no", "and"]
    
    tr_score = sum(1 for m in tr_markers if m in t)
    en_score = sum(1 for m in en_markers if m in t)
    
    if tr_score > en_score: return "tr"
    if en_score > tr_score: return "en"
    return "default"