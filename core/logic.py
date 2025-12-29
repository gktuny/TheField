class SignalProcessor:
    def process(self, text: str) -> dict:
        t = text.lower()
        markers_found = []

        forbidden_roots = [
            "ben", "sen", " o ", " o", "o ", 
            "biz", "siz", "onlar",
            "bana", "sana", "ona", "bize", "size",
            "beni", "seni", "onu", "bizi", "sizi", "onları",
            "i ", "you", "he ", "she ", "we ", "they", "my", "your"
        ]

        suffixed_negations = [
            "yokum", "yoksun", "yokuz", "yoksunuz", "yoklar",
            "varım", "varsın", "varız",
            "değilim", "değilsin", "değiliz",
            "exist", "am not" 
        ]

        valid_objectives = [
            "ben yok", "sen yok", "o yok", "biz yok", "siz yok", "onlar yok",
            "ben kalmadı", "sen bitti", "o silindi",
            "no i ", "no you ", "no self"
        ]

        has_pronoun = any(x in t for x in forbidden_roots)
        has_bad_suffix = any(y in t for y in suffixed_negations)
        is_valid_objective = any(z in t for z in valid_objectives)

        subject_collapsed = False
        if has_bad_suffix: subject_collapsed = False
        elif not has_pronoun: subject_collapsed = True
        elif has_pronoun and is_valid_objective: subject_collapsed = True
        else: subject_collapsed = False

        if subject_collapsed: markers_found.append("no_self_reference")

        if not any(x in t for x in ["dün", "yarın", "was", "will", "future", "past", "olacak", "vardı", "gelecek", "önce", "sonra"]):
            markers_found.append("timeless_marker")

        if not any(x in t for x in ["neden", "niçin", "why", "meaning", "explain", "nasıl", "kim", "ne zaman", "what"]):
            markers_found.append("observer_equals_observed")

        clean_text = text.strip()
        is_final_strike = clean_text in [".", "...", "…", "ok", "tamam", "OK", "Ok"]
        primary_marker = markers_found[0] if markers_found else "noise"

        return {"marker": primary_marker, "final_strike": is_final_strike}