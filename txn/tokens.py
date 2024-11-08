import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk

def extract_unique_tokens(table_info):
    """
    Extract unique tokens from table/column names and descriptions.
    
    Args:
    table_info (dict): Dictionary containing:
        - table_name (str): Name of the table
        - table_description (str): Description of the table
        - columns (list): List of dictionaries with 'name' and 'description' keys
        
    Returns:
    set: Set of unique tokens
    """
    # Download required NLTK data (run once)
    try:
        nltk.data.find('tokenizers/punkt')
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('punkt')
        nltk.download('stopwords')
    
    # Initialize set for unique tokens
    unique_tokens = set()
    
    def process_name(name):
        """Process table/column names by splitting on dots and underscores"""
        # Split on dots and underscores
        tokens = re.split('[._]', name.lower())
        # Remove empty strings and add to set
        return {token for token in tokens if token}
    
    def process_description(description):
        """Process descriptions by removing stopwords and tokenizing"""
        # Get English stopwords
        stop_words = set(stopwords.words('english'))
        
        # Tokenize and convert to lowercase
        tokens = word_tokenize(description.lower())
        
        # Remove stopwords, punctuation, and numbers
        tokens = {token for token in tokens 
                 if token not in stop_words 
                 and token.isalnum() 
                 and not token.isnumeric()}
        
        return tokens
    
    # Process table name
    unique_tokens.update(process_name(table_info['table_name']))
    
    # Process table description
    unique_tokens.update(process_description(table_info['table_description']))
    
    # Process column information
    for column in table_info['columns']:
        unique_tokens.update(process_name(column['name']))
        unique_tokens.update(process_description(column['description']))
    
    return unique_tokens

# Example usage
if __name__ == "__main__":
    sample_input = {
        'table_name': 'user_profile.details',
        'table_description': 'This table stores detailed information about user profiles',
        'columns': [
            {
                'name': 'user_id',
                'description': 'Unique identifier for each user in the system'
            },
            {
                'name': 'profile.last_login',
                'description': 'Timestamp of the most recent user login'
            }
        ]
    }
    
    tokens = extract_unique_tokens(sample_input)
    print("Unique tokens:", sorted(tokens))
