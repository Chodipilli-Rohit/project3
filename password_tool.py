import argparse
import zxcvbn
import nltk
from nltk.corpus import words
import itertools
import re
import string
import math
from datetime import datetime
import os

# Download NLTK words if not already present
try:
    nltk.data.find('corpora/words')
except LookupError:
    nltk.download('words')

def calculate_entropy(password):
    """Calculate Shannon entropy of a password."""
    charset_size = 0
    if any(c in string.ascii_lowercase for c in password):
        charset_size += 26
    if any(c in string.ascii_uppercase for c in password):
        charset_size += 26
    if any(c in string.digits for c in password):
        charset_size += 10
    if any(c in string.punctuation for c in password):
        charset_size += 32
    if charset_size == 0:
        return 0
    return len(password) * math.log2(charset_size)

def analyze_password(password):
    """Analyze password strength using zxcvbn and custom entropy."""
    result = zxcvbn.zxcvbn(password)
    entropy = calculate_entropy(password)
    
    score = result['score']
    strength = {
        0: "Very Weak",
        1: "Weak",
        2: "Fair",
        3: "Good",
        4: "Strong"
    }
    
    feedback = {
        'strength': strength.get(score, "Unknown"),
        'score': score,
        'entropy': round(entropy, 2),
        'crack_time': result['crack_times_display']['offline_slow_hashing_1e4_per_second'],
        'suggestions': result['feedback']['suggestions'],
        'warnings': result['feedback']['warning']
    }
    return feedback

def leetspeak_variations(word):
    """Generate leetspeak variations of a word."""
    leet_map = {
        'a': ['4', '@'],
        'e': ['3'],
        'i': ['1', '!'],
        'o': ['0'],
        's': ['5', '$'],
        't': ['7']
    }
    variations = [word]
    
    for char, subs in leet_map.items():
        new_variations = []
        for var in variations:
            for sub in subs:
                new_variations.append(var.replace(char, sub).replace(char.upper(), sub))
            new_variations.append(var)
        variations = new_variations
    return list(set(variations))

def generate_wordlist(names, dates, pets, output_file):
    """Generate custom wordlist with user inputs and common patterns."""
    wordlist = set()
    word_set = set(words.words())
    
    # Basic user inputs
    inputs = names + dates + pets
    
    # Add original inputs
    wordlist.update(inputs)
    
    # Generate variations
    for input_str in inputs:
        # Case variations
        wordlist.add(input_str.lower())
        wordlist.add(input_str.upper())
        wordlist.add(input_str.capitalize())
        
        # Leetspeak variations
        wordlist.update(leetspeak_variations(input_str))
        
        # Common patterns: append years (last 50 years and next 10)
        current_year = datetime.now().year
        for year in range(current_year - 50, current_year + 10):
            wordlist.add(f"{input_str}{year}")
            wordlist.add(f"{input_str}{str(year)[-2:]}")
        
        # Common patterns: append numbers and special chars
        for suffix in ['123', '!', '@', '#', '1']:
            wordlist.add(f"{input_str}{suffix}")
        
        # Combine with common words
        for common_word in list(word_set)[:100]:  # Limit to 100 common words
            wordlist.add(f"{input_str}{common_word}")
            wordlist.add(f"{common_word}{input_str}")
    
    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(wordlist):
            if len(word) > 0:  # Skip empty strings
                f.write(f"{word}\n")
    
    return len(wordlist)

def main():
    parser = argparse.ArgumentParser(description="Password Analysis and Wordlist Generator")
    parser.add_argument('--password', help="Password to analyze")
    parser.add_argument('--names', nargs='*', default=[], help="Names for wordlist generation")
    parser.add_argument('--dates', nargs='*', default=[], help="Dates for wordlist generation")
    parser.add_argument('--pets', nargs='*', default=[], help="Pet names for wordlist generation")
    parser.add_argument('--output', default="wordlist.txt", help="Output file for wordlist")
    
    args = parser.parse_args()
    
    # Password analysis
    if args.password:
        print("\nPassword Analysis:")
        feedback = analyze_password(args.password)
        print(f"Strength: {feedback['strength']} (Score: {feedback['score']}/4)")
        print(f"Entropy: {feedback['entropy']} bits")
        print(f"Crack Time (offline, slow hashing): {feedback['crack_time']}")
        if feedback['warnings']:
            print(f"Warning: {feedback['warnings']}")
        if feedback['suggestions']:
            print("Suggestions:")
            for suggestion in feedback['suggestions']:
                print(f"- {suggestion}")
    
    # Wordlist generation
    if args.names or args.dates or args.pets:
        print("\nGenerating wordlist...")
        count = generate_wordlist(args.names, args.dates, args.pets, args.output)
        print(f"Generated {count} words in {args.output}")
    elif not args.password:
        parser.print_help()

if __name__ == "__main__":
    main()
