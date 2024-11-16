import json
from nltk.corpus import stopwords
import nltk
import re
from typing import List, Dict, Set
from collections import Counter
from tabulate import tabulate

def generate_token_statistics(processed_acronyms_file: str) -> None:
    """
    Generate and print statistics about token frequency across all acronyms.
    
    Args:
        processed_acronyms_file (str): Path to processed acronyms JSON file
    """
    # Read processed acronyms
    with open(processed_acronyms_file, 'r', encoding='utf-8') as f:
        processed_acronyms = json.load(f)
    
    # Count all tokens
    token_counter = Counter()
    for acronym, tokens in processed_acronyms.items():
        token_counter.update(tokens)
    
    # Prepare statistics
    total_tokens = sum(token_counter.values())
    unique_tokens = len(token_counter)
    
    # Prepare data for tabulate
    token_stats = [
        [rank + 1, token, count, f"{(count/total_tokens)*100:.2f}%"]
        for rank, (token, count) in enumerate(token_counter.most_common())
    ]
    
    # Print report
    print("\nToken Frequency Analysis Report")
    print("=" * 50)
    print(f"Total token occurrences: {total_tokens}")
    print(f"Unique tokens: {unique_tokens}")
    print(f"Average occurrences per token: {total_tokens/unique_tokens:.2f}")
    print("\nDetailed Token Statistics:")
    print(tabulate(
        token_stats,
        headers=['Rank', 'Token', 'Occurrences', 'Percentage'],
        tablefmt='grid'
    ))
    
    # Print some interesting insights
    print("\nKey Insights:")
    print(f"- Most common token: '{token_stats[0][1]}' ({token_stats[0][2]} occurrences)")
    single_occurrence = sum(1 for _, count in token_counter.items() if count == 1)
    print(f"- Tokens appearing only once: {single_occurrence} ({(single_occurrence/unique_tokens)*100:.2f}% of unique tokens)")
    
    # Save report to file
    report_file = "token_statistics_report.txt"
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("Token Frequency Analysis Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Total token occurrences: {total_tokens}\n")
        f.write(f"Unique tokens: {unique_tokens}\n")
        f.write(f"Average occurrences per token: {total_tokens/unique_tokens:.2f}\n\n")
        f.write("Detailed Token Statistics:\n")
        f.write(tabulate(
            token_stats,
            headers=['Rank', 'Token', 'Occurrences', 'Percentage'],
            tablefmt='grid'
        ))
    
    print(f"\nFull report saved to {report_file}")

# Example usage
if __name__ == "__main__":
    # First process the original acronyms file
    process_acronyms('acronyms.json', 'processed_acronyms.json')
    
    # Generate and print token statistics
    generate_token_statistics('processed_acronyms.json')
