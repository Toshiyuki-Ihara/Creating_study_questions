import random
from nltk.corpus import wordnet as wn
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

def get_synonyms_eng(word, max_num=5):
    synonyms = []
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace('_', ' ')
            if name.lower() != word.lower():
                synonyms.append(name)
    return random.sample(synonyms, min(len(synonyms), max_num))

def generate_eng_choice_question(sentences, num_choices=4):
    quiz_list = []
    all_keywords = set()
    for s in sentences:
        words = s.split()
        kws = [w.strip('.,') for w in words if len(w) > 3 and w.isalpha()]
        all_keywords.update(kws)
    for sentence in sentences:
        words = sentence.split()
        keywords = [w.strip('.,') for w in words if len(w) > 3 and w.isalpha()]
        if not keywords:
            continue
        answer = random.choice(keywords)
        question = sentence.replace(answer, '_____', 1)
        synonyms = get_synonyms_eng(answer, max_num=num_choices - 1)
        distractor_pool = list(all_keywords - {answer} - set(synonyms))
        random.shuffle(distractor_pool)
        while len(synonyms) < (num_choices - 1) and distractor_pool:
            synonyms.append(distractor_pool.pop())
        choices = synonyms[:num_choices - 1] + [answer]
        random.shuffle(choices)
        quiz_list.append({
            "question": question,
            "answer": answer,
            "choices": choices
        })
    return quiz_list

def generate_eng_writing_question(sentences):
    quiz_list = []

    for sentence in sentences:
        words = sentence.split()
        keywords = [w.strip('.,') for w in words if len(w) > 3 and w.isalpha()]
        if not keywords:
            continue

        answer = random.choice(keywords)
        question = sentence.replace(answer, '_____', 1)

        quiz_list.append({
            "question": question,
            "answer": answer,
            "type": "writing"  # クライアント側で判別用に追加
        })

    return quiz_list
