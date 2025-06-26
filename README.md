# project3
password strength analyzer

 The tool evaluates password strength using zxcvbn and generates custom wordlists based on user inputs (name, date of birth, pet name, password) with variations like leetspeak and appended years, exporting them as .txt files for use in cracking tools.

Tools Used
Python: Core programming language.
argparse: For CLI argument parsing.
NLTK: To enhance wordlists with related English words.
zxcvbn: For robust password strength analysis (score, crack time, feedback).
tkinter: For the GUI interface.
Features
Password Strength Analysis:
Uses zxcvbn to compute strength score (0-4), estimated crack time, and feedback.
Custom entropy calculation based on character set size (lowercase, uppercase, digits, special characters).
Displays results in GUI or CLI with suggestions for improvement.
Custom Wordlist Generation:
Accepts user inputs: name, date of birth (YYYY-MM-DD), pet name, and password.
Generates variations:
Leetspeak: Substitutes characters (e.g., 'a' → '4', '@').
Years: Appends years from 1900 to current year (e.g., "john2023", "2023john").
Case Variations: Adds lowercase, uppercase, and capitalized forms.
NLTK Words: Includes related words from NLTK's corpus if they contain or are contained in user inputs.
Exports wordlist as a .txt file.
Interfaces:
GUI: Built with tkinter, includes fields for password, name, DOB, pet name, checkboxes for leetspeak and years, and buttons to analyze and save wordlists.
CLI: Supports command-line arguments for password analysis and wordlist generation.
Output:
Password analysis shows strength, crack time, entropy, and suggestions.
Wordlist is displayed (first 100 entries in GUI) and saved as a .txt file.
Deliverables
A Python script (password_analyzer.py) that:
Analyzes password strength with zxcvbn and custom entropy.
Generates attack-specific wordlists based on user inputs.
Supports GUI and CLI interfaces.
Exports wordlists in .txt format compatible with cracking tools like Hashcat or John the Ripper.
