import json
from nltk.corpus import stopwords
import nltk
import re

def process_acronyms(input_file, output_file):
    """
    Process acronyms JSON file to create a new JSON with lowercase keys and tokenized values.
    
    Args:
        input_file (str): Path to input JSON file
        output_file (str): Path to output JSON file
    """
    # Download required NLTK data
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords')
    
    # Get stopwords
    stop_words = set(stopwords.words('english'))
    
    # Read input JSON
    with open(input_file, 'r', encoding='utf-8') as f:
        acronyms = json.load(f)
    
    # Process each acronym
    processed_acronyms = {}
    
    for acronym, description in acronyms.items():
        # Convert acronym to lowercase
        lowercase_acronym = acronym.lower()
        
        # Tokenize the description
        # Split on non-alphanumeric characters and convert to lowercase
        tokens = set(re.findall(r'\w+', description.lower()))
        
        # Add the acronym itself to the tokens
        tokens.add(lowercase_acronym)
        
        # Remove stopwords
        tokens = tokens - stop_words
        
        # Store as list (JSON doesn't support sets)
        processed_acronyms[lowercase_acronym] = sorted(list(tokens))
    
    # Write output JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(processed_acronyms, f, indent=2)

# Example usage
if __name__ == "__main__":
    # Example input JSON structure:
    # {
    #     "API": "Application Programming Interface",
    #     "CPU": "Central Processing Unit"
    # }
    
    process_acronyms('acronyms.json', 'processed_acronyms.json')
