import re
from collections import defaultdict, OrderedDict
import math
from translate import translate

def extract_consonants(word, lang):
    word = word.lower()
    consonants = ''.join(OrderedDict.fromkeys(re.findall(r'[bcdfghjklmnpqrstvwxyz]', word)))
    consonant_replacements = {
        'sh': 'ʂ',
        'ch': 'ʂ',
        'zh': 'ʐ',
        'ts': 'ʂ',
        'th': 'θ',
        'ph': 'f',
        'gh': 'ɣh',
        'ng': 'nŋ',
        'y': 'j',
        'x': 'ks'
    }
    for old, new in consonant_replacements.items():
        consonants = consonants.replace(old, new)
    consonants = re.sub(r'c', 'k' if lang == "English" else 'ʂ', consonants)
    return consonants

def assign_weights(consonants, language):
    weights = {
        'English': 4,
        'Chinese': 3,
        'Latin': 1,
        'Esperanto': 2,
        'Russian': 2,
        'Hindi': 2,
        'Arabic': 2,
        'Finnish': 1,
        'Swahili': 1
    }
    return {c: weights.get(language, 0) for c in consonants}

def main_process(word):
    result = [f"*Translation results for \"{word}\":*"]
    translations = translate(word)
    
    if "Error" in translations:
        return f"Error: {translations['Error']}"

    total_weights = defaultdict(int)
    position_weights = defaultdict(int)
    position_counts = defaultdict(int)
    all_consonants = []

    for language, translated_word in translations.items():
        consonants = extract_consonants(translated_word, language)
        all_consonants.append(consonants)
        language_weights = assign_weights(consonants, language)
        
        for index, consonant in enumerate(consonants):
            total_weights[consonant] += language_weights[consonant]
            position_weights[consonant] += index + 1
            position_counts[consonant] += 1

        result.append(f"{language}: {translated_word}")
    
    average_positions = {c: position_weights[c] / position_counts[c] for c in position_counts}
    sorted_consonants = sorted(total_weights.keys(), key=lambda c: (-total_weights[c], average_positions[c]))

    result.append("\n*Weights and Average Positions:*")
    for consonant in sorted_consonants:
        result.append(f"{consonant}: weight = {total_weights[consonant]}, index = {round(average_positions[consonant])}")
    
    average_length = math.floor(sum(len(c) for c in all_consonants) / len(all_consonants))
    num_slots = max(2, min(average_length, 5))
    average_weight = math.ceil(sum(total_weights[c] for c in sorted_consonants) / len(sorted_consonants))
    filtered_weights = {k: v for k, v in total_weights.items() if v > average_weight}
    
    final_consonants = sorted(filtered_weights.keys(), key=lambda c: (-total_weights[c], average_positions[c]))[:num_slots]
    final_consonants = sorted(final_consonants, key=lambda c: (average_positions[c], -total_weights[c]))
    
    result.append("\n*Final Consonants:*")
    for consonant in final_consonants:
        result.append(f"{consonant}: weight = {total_weights[consonant]}, index = {round(average_positions[consonant])}")
    
    result_root = ''.join(final_consonants)
    result.append(f"\n*Result: {result_root}*")
    
    return "\n".join(result)
