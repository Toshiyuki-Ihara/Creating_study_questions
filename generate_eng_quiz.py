import random
from nltk.corpus import wordnet as wn

def get_synonyms_eng(word, max_num=5):
    synonyms = []
    for syn in wn.synsets(word):
        for lemma in syn.lemmas():
            name = lemma.name().replace('_', ' ')
            if name.lower() != word.lower():
                synonyms.append(name)
    print(f"{word}の類義語一覧----------------")
    for syn in synonyms:
        print(syn)
    return random.sample(synonyms, min(len(synonyms), max_num))

def get_hypernyms_hyponyms_eng(word, pos=None, max_num=5):
    hypernyms = set()
    hyponyms = set()

    synsets = wn.synsets(word, pos=pos)
    for syn in synsets:
        # 上位語
        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                hypernyms.add(lemma.name().replace('_', ' '))

        # 下位語
        for hypo in syn.hyponyms():
            for lemma in hypo.lemmas():
                hyponyms.add(lemma.name().replace('_', ' '))

    print(f"{word} の上位語 (hypernyms) ----------------")
    for h in list(hypernyms)[:max_num]:
        print(h)

    print(f"\n{word} の下位語 (hyponyms) ----------------")
    for h in list(hyponyms)[:max_num]:
        print(h)

    return list(hypernyms.union(hyponyms))[:max_num]


def get_related_words_eng(word, max_num=10, pos=None):
    synonyms = set(get_synonyms_eng(word))
    hyper_hypo = set(get_hypernyms_hyponyms_eng(word, pos=pos))

    combined = synonyms.union(hyper_hypo)

    # 2語以上の語を除外
    filtered = [w for w in combined if ' ' not in w]

    print(f"\n{word} の関連語（1単語のみ） ----------------")
    for r in filtered[:max_num]:
        print(r)

    return filtered[:max_num]



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
        synonyms = get_related_words_eng(answer, max_num=num_choices - 1)
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
