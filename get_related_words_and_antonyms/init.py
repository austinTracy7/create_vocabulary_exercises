import pandas as pd
from nltk.corpus import wordnet as wn

def get_specific_input(text="Yes/No",options=["Yes","No"]):
    while True:
        output = input(text)
        if output in options:
            return output
        else:
            print("Please type one of the following options: " + " ".join(options) 
                + "\n")

unique_selected_words_df = pd.read_pickle("unique_selected_words.pkl")

# ensuring correct meanings are selected and getting more specific

for _, row in unique_selected_words_df.iterrows():
    possible_meanings = row.LikelyMeanings.split(",")
    accepted_meanings = []
    if len(possible_meanings) > 1:
        for i, meaning in enumerate(possible_meanings):
            print(i, wn.synset(meaning).definition())
        response = get_specific_input(text="""Input the number for the correct meaning or 
            either Context or Full Details for more information.""", options=[str(x) for x 
            in list(range(len(meaning)))] + ["Context", "Full Details"])

        if response == "Context":
            response = get_specific_input(text="""Input the number for the correct meaning or 
            Full Details for more information.""", options=[str(x) for x 
            in list(range(len(meaning)))] + ["Full Details"])
        if response == "Full details":
            response = get_specific_input(text="""Input the number for the correct meaning.""", 
            options=[str(x) for x in list(range(len(meaning)))])
        accepted_meanings.append()
    elif len(possible_meanings) == 1:
        accepted_meanings.append()


#get_specific_input

# getting related words

# getting antonyms

