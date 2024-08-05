import pandas as pd

def load_and_preprocess_data(file_path):
    # Load the data
    df = pd.read_csv(file_path)
    
    # Check for missing values and handle them if necessary
    if df.isnull().values.any():
        df = df.dropna()
    
    # Ensure correct data types
    df['Serial Number'] = df['Serial Number'].astype(int)
    df['Error Type'] = df['Error Type'].astype(str)
    df['Ungrammatical Statement'] = df['Ungrammatical Statement'].astype(str)
    df['Standard English'] = df['Standard English'].astype(str)
    
    return df

def main():
    file_path = '/Users/cclam/Desktop/CSS497 Capstone/grammarTrainResources/Grammar Correction.csv'
    data = load_and_preprocess_data(file_path)
    
    # Save the preprocessed data for future use
    data.to_csv('/Users/cclam/Desktop/CSS495 Capstone/readyToGoGrammarTrainResources/GTP3TrainningResource/preprocessed_grammar_data.csv', index=False)
    print("Data preprocessed and saved to 'preprocessed_grammar_data.csv'")

if __name__ == '__main__':
    main()
