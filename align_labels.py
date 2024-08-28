#### finding and aligning text labels


! pip install Levenshtein

import pandas as pd
#import Levenshtein

# Read the CSV files
predictions_df = pd.read_csv('ocr_predictions_file_name.csv')
labels_df = pd.read_csv('labels_file_name.csv')

# target file for results
destination_path ='predictions_with_closest_text.csv'

# Rename the columns
predictions_df.columns = ['file name', 'predicted text']
labels_df.columns = ['original text','text file name']
predictions_df.drop_duplicates(inplace=True)
predictions_df['predicted text'] = predictions_df['predicted text'].astype(str)
labels_df['original text'] = labels_df['original text'].astype(str)

def levenshtein(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        a, b = b, a
        n, m = m, n
    current_row = list(range(n+1))
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i] + [0] * n
        for j in range(1, n+1):
            add, delete, change = previous_row[j] + 1, current_row[j-1] + 1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)
    return current_row[n]

# Function to find the closest string and its Levenshtein distance
def find_closest_string_and_distance(predicted_text, labels_df):
    min_distance = float('inf')
    closest_original_text = ""
    closest_text_file_name = ""

    for index, row in labels_df.iterrows():
        original_text = row['original text']
        text_file_name = row['text file name']
        distance = levenshtein(original_text,predicted_text)/len(original_text)
        if distance < min_distance:
            min_distance = distance
            closest_original_text = original_text
            closest_text_file_name = text_file_name

    return closest_original_text, closest_text_file_name, min_distance

results_df=pd.read_csv(destination_path)

# Define the chunk size for processing and saving results in chunks
chunk_size = 30
# Process the DataFrame in chunks
for start in range(0, len(predictions_df), chunk_size):
    end = start + chunk_size
    chunk = predictions_df.iloc[start:end]

    # Apply the function to each row in the chunk
    results = chunk['predicted text'].apply(lambda x: find_closest_string_and_distance(x, labels_df))

    # Extract the results into separate columns
    chunk['closest original text'] = results.apply(lambda x: x[0])
    chunk['text file name'] = results.apply(lambda x: x[1])
    chunk['levenshtein distance'] = results.apply(lambda x: x[2])

    # Append the chunk results to the destination CSV file
    if start == 0:
        chunk.to_csv(destination_path, index=False, encoding='utf-8', mode='w')
    else:
        chunk.to_csv(destination_path, index=False, encoding='utf-8', mode='a', header=False)
    print('saved')
# Print a confirmation message
print(f"Processing completed. Results saved to {destination_path}")

results_df['levenshtein distance'].sort_values().plot.bar()

labels_df=results_df[(results_df['levenshtein distance']<0.63) ][['old file name','closest original text']]
labels_df['old file name']=labels_df.apply(lambda x: x[0].split('/')[-1],axis=1)
labels_df.rename(columns={"old file name": "file name", "closest original text": "text"},inplace=True)
