# third party library imports
from nltk.corpus import wordnet as wn
import pandas as pd
from nltk.stem import WordNetLemmatizer
import nltk

# functions
def get_more_common_pos(pos):
    general_pos = None
    if pos in ["NNP","NNS","NN","CD","NNPS"]:
        general_pos = "n"
    elif pos in ["IN","DT","TO","CC"]:
        general_pos = "functional_word" # not meaningful
    elif pos in ["PRP","WP","WRB","FW","WDT","PDT"]:
        general_pos = "s"
    elif pos in ["VBZ","VBP","VB","MD","VBN","VBG","VBD"]:
        general_pos = "v"
    elif pos in ["RB","RP","RBR"]:
        general_pos = "r"
    elif pos in ["JJ","JJS"]:
        general_pos = "a"
    return general_pos

def find_likely_meanings(row):
    # mapping to a more general part of speech for likely meanings
    general_pos = get_more_common_pos(row["POS"]) 
    # selecting the likely meanings
    possible_meanings = wn.synsets(row["Token"])
    output = [x for x in possible_meanings if str(x).find(f'.{general_pos}.') > -1]
    if len(possible_meanings) == 0:
        print(type(output))
        output = None
    elif len(possible_meanings) == 1 and output == []:
        output = ["?" + str(possible_meanings[0])]
    elif general_pos == "r" and output == []:
        output = [x for x in possible_meanings if str(x).find(f'.a.') > -1]
    return output

# annotated_tokens_df["LikelyMeanings"] = annotated_tokens_df.apply(find_likely_meanings,axis=1)

def make_token_sentence_number_pairs(sentences):
    token_and_sentence_pairings = []
    for i, sentence in enumerate(sentences):
        token_and_sentence_pairings += [list(annotated_token) for annotated_token
            in list(zip(([i] * len(sentence)),sentence))]
    return [[pairing[0]] + list(pairing[1]) for pairing in token_and_sentence_pairings]


def normalize_tokens(token):
    match token.lower():
        case "'cause":
            return "because"
        case "'re":
            return "are"
        case other:
            return token


if __name__ == "__main__":
    with open(r"get_vocabulary_and_likely_meanings\input.txt","r") as f:
        input_text = f.read()

    song_lines = input_text.split("\n")

    song_lines_with_annotations = [nltk.pos_tag(nltk.word_tokenize(line)) for line in song_lines]

    # putting the information into a table (dataframe) structure
    annotated_tokens_df = pd.DataFrame.from_records(make_token_sentence_number_pairs(
        song_lines_with_annotations))

    annotated_tokens_df.columns = ["SentenceNumber","Token","POS"]

    # cleaning the data
    annotated_tokens_df.loc[:,"Token"] = annotated_tokens_df["Token"].apply(normalize_tokens)
    annotated_tokens_df.loc[:,"POS"] = annotated_tokens_df["POS"].apply(lambda x: x if x.isalpha()
        else None)

    #
    annotated_tokens_df["LikelyMeanings"] = annotated_tokens_df.apply(find_likely_meanings,axis=1)

    # annotated_tokens_df[annotated_tokens_df["Token"] == "heavenly"]
    
    # @foo add in lemmatization? but the fix was made differently
    # lemmatizer = WordNetLemmatizer()
  
    # a denotes adjective in "pos"
    # lemmatizer.lemmatize("better", pos ="a")

    # saving the data (including collapsing synsets into a string of comma separated values)
    annotated_tokens_df.loc[:,"LikelyMeanings"] = annotated_tokens_df[
        "LikelyMeanings"].apply(
            lambda x: ",".join([str(meaning).replace(
            "Synset('","").replace("')","") for meaning in x]) if x != None else x)

    annotated_tokens_df.to_pickle("tokens_and_meanings.pkl")