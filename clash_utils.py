from difflib import get_close_matches

def find_closest_match(card_name, original_list):
    closest_match = get_close_matches(card_name, original_list, n=1)
    return closest_match[0] if closest_match else None
