import pandas as pd
from nltk.corpus import brown
from nltk.corpus import wordnet as wn
from nltk import FreqDist

def find_frequency_ranking(word):
    """This is meant to find the most unusual words with
    high numbers, but to ignore anything with punctuation
    that is much more common."""
    output = 100000 # bigger than any in the brown corpus 
    if word.isalpha():
        try:
            output = words_ranked.index(word.lower())
        except:
            pass
    else:
        output = 0 # insignificant
    return output

def get_specific_input(text="Yes/No",options=["Yes","No"]):
    while True:
        output = input(text)
        if output in options:
            return output
        else:
            print("Please type one of the following options: " + " ".join(options) 
                + "\n")

if __name__ == "__main__":
    annotated_tokens_df = pd.read_pickle("tokens_and_meanings.pkl")

    # pull in the brown corpus
    def get_frequency_of_brown_words_case_insensitive():
        return FreqDist([word.lower() for word 
            in brown.words() if word.isalpha()])

    word_frequencies = get_frequency_of_brown_words_case_insensitive()

    words_ranked = list(word_frequencies.keys())
    # ranking the words according to their frequency in that corpus
    
    annotated_tokens_df["BrownFrequency"] = annotated_tokens_df["Token"].apply(
        lambda x: find_frequency_ranking(x))

    unique_words = annotated_tokens_df[~annotated_tokens_df.duplicated("Token")]

    # presenting the words to a user for approving 10
    approved_ten = []
    
    for _, row in unique_words.sort_values(["BrownFrequency"],ascending=False).iterrows():
        # presenting the word
        sentence_number, token, POS, likelymeanings, _ = row
        if token.isalpha():
            if likelymeanings != None and likelymeanings != '' and "?" not in likelymeanings:
                likelymeanings = likelymeanings.split(",")
                approval = get_specific_input(f"The next suggested word is {token} ({POS})."
                    + "\nShould it be included in the exercise? (Yes/No/Context/Full details) ",
                    ["Yes","No","Context","Full details"])
                if approval == "Context":
                    approval = get_specific_input(f"The word {token} comes from this sentence:\n"
                        + " ".join(annotated_tokens_df[annotated_tokens_df["SentenceNumber"]
                            == sentence_number]["Token"].tolist())
                        + f"\nDo you want to include it? (Yes/No/Full details) ")
                if approval == "Full details":
                    approval = get_specific_input(f"The word {token} comes from this sentence:\n"
                        + " ".join(annotated_tokens_df[annotated_tokens_df["SentenceNumber"]
                            == sentence_number]["Token"].tolist())
                        + "\nThese are the possible meanings suggested for it:\n"
                        + "\n".join([f"{i} {wn.synset(meaning).definition()}" for i, meaning in enumerate(likelymeanings)])
                        + f"\nDo you want to include it? (Yes/No/Full details) ")
                if approval == "Yes":
                    approved_ten.append(token)
        if len(approved_ten) == 10:
            break
    print("You did not select enough words.")
    # add possible loop?

    unique_words[unique_words.Token.isin(approved_ten)].to_pickle("unique_selected_words.pkl")

    annotated_tokens_df[annotated_tokens_df.Token.isin(approved_ten)].to_pickle("selected_words.pkl")

    