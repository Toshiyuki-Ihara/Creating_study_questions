import random
from janome.tokenizer import Tokenizer
from nltk.corpus import wordnet as wn

tokenizer = Tokenizer()

def get_synonyms_jp(word, max_num=3):
    synsets = wn.synsets(word, lang='jpn')
    synonyms = set()
    for syn in synsets:
        for lemma in syn.lemmas(lang='jpn'):
            if lemma.name() != word:
                synonyms.add(lemma.name())
    print(f"{word}の類義語一覧----------------")
    for syn in synonyms:
        print(syn)
    return list(synonyms)[:max_num]

def get_hypernyms_hyponyms_jp(word, pos=None, max_num=5):
    hypernyms = set()
    hyponyms = set()

    synsets = wn.synsets(word, lang="jpn", pos=pos)
    for syn in synsets:
        # 上位語
        for hyper in syn.hypernyms():
            for lemma in hyper.lemmas():
                if lemma.lang() == 'jpn':
                    hypernyms.add(lemma.name().replace('_', ' '))

        # 下位語
        for hypo in syn.hyponyms():
            for lemma in hypo.lemmas():
                if lemma.lang() == 'jpn':
                    hyponyms.add(lemma.name().replace('_', ' '))

    print(f"{word} の上位語 (hypernyms) ----------------")
    for h in list(hypernyms)[:max_num]:
        print(h)

    print(f"\n{word} の下位語 (hyponyms) ----------------")
    for h in list(hyponyms)[:max_num]:
        print(h)

    return list(hypernyms.union(hyponyms))[:max_num]


def get_related_words_jp(word, max_num=10, pos=None):
    synonyms = set(get_synonyms_jp(word))
    hyper_hypo = set(get_hypernyms_hyponyms_jp(word, pos=pos))

    combined = synonyms.union(hyper_hypo)

    # 2語以上の語を除外
    filtered = [w for w in combined if ' ' not in w]

    print(f"\n{word} の関連語（1単語のみ） ----------------")
    for r in filtered[:max_num]:
        print(r)

    return filtered[:max_num]

def generate_japanese_quizzes(sentences, num_choices=4):
    quizzes = []
    spamaji = set()
    for s in sentences:
        for token in tokenizer.tokenize(s):
            if token.part_of_speech.startswith("名詞"):
                spamaji.add(token.surface)
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        nouns = [t.surface for t in tokens if t.part_of_speech.startswith("名詞")]
        candidates = [w for w in nouns if len(w) > 1]
        if not candidates:
            continue
        ans = random.choice(candidates)
        base = get_related_words_jp(ans, max_num=num_choices-1)
        distractors = [w for w in spamaji if w != ans and w not in base]
        random.shuffle(distractors)
        while len(base) < num_choices - 1:
            base.append(distractors.pop())
        choices = base[:num_choices - 1] + [ans]
        random.shuffle(choices)
        quiz = {
            "question": sentence.replace(ans, "_____"),
            "answer": ans,
            "choices": choices
        }
        quizzes.append(quiz)
    return quizzes


def generate_japanese_writing_quizzes(sentences):
    writing_quizzes = []
    for sentence in sentences:
        tokens = tokenizer.tokenize(sentence)
        nouns = [t.surface for t in tokens if t.part_of_speech.startswith("名詞")]
        candidates = [w for w in nouns if len(w) > 1]
        if not candidates:
            continue

        answer = random.choice(candidates)
        question = sentence.replace(answer, "_____")

        writing_quizzes.append({
            "question": question,
            "answer": answer,
            "type": "writing"
        })
    return writing_quizzes
