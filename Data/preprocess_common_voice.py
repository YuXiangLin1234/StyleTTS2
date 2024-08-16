import pandas as pd
from hanziconv import HanziConv
from phonemizer import phonemize

def traditional_to_simplified(traditional_text):
    """Convert Traditional Chinese to Simplified Chinese."""
    simplified_text = HanziConv.toSimplified(traditional_text)
    return simplified_text

def text_to_phonemes(text, language='zh'):
    """Convert Chinese text to phonemes using phonemizer."""
    phonemes = phonemize(
        text,
        language=language,
        backend='espeak',
        strip=True,  # Removes extra spaces
        preserve_punctuation=True
    )
    return phonemes

def process_tsv(input_tsvs, output_file):
	"""Process the TSV file and generate the output file in the specified format."""


	with open(output_file, 'w', encoding='utf-8') as f_out:
		
		for input_tsv in input_tsvs:
			df = pd.read_csv(input_tsv, sep='\t')

			# Create a mapping from client_id (original) to a unique integer starting from 3000
			unique_clients = df['client_id'].unique()
			client_id_map = {client: idx + 3000 for idx, client in enumerate(unique_clients)}
			for _, row in df.iterrows():
				# Extract the necessary columns
				filename = row['path']
				sentence = row['sentence']
				client_id = client_id_map[row['client_id']]
				
				# Convert Traditional Chinese to Simplified Chinese (if needed)
				simplified_sentence = traditional_to_simplified(sentence)
				
				# Convert the sentence to phonemes
				phonemes = text_to_phonemes(simplified_sentence)
				
				# Write to output file in the format: filename.wav|phoneme|speaker
				f_out.write(f"{filename}|{phonemes}|{client_id}\n")

# Example usage
input_tsvs = ["/workspace/backup/cv-corpus-18.0-2024-06-14/zh-TW/train.tsv",
              "/workspace/backup/cv-corpus-18.0-2024-06-14/zh-TW/dev.tsv",
			  "/workspace/backup/cv-corpus-18.0-2024-06-14/zh-TW/invalidated.tsv",
              "/workspace/backup/cv-corpus-18.0-2024-06-14/zh-TW/other.tsv",
              "/workspace/backup/cv-corpus-18.0-2024-06-14/zh-TW/validated.tsv"]  # Replace with your input TSV file path
output_file = 'train.txt'  # Output file path

process_tsv(input_tsvs, output_file)
