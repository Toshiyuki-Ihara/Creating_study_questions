import random
from janome.tokenizer import Tokenizer
from nltk.corpus import wordnet as wn

tokenizer = Tokenizer()

def get_jp_synonyms(word, max_num=3):
    synsets = wn.synsets(word, lang='jpn')
    synonyms = set()
    for syn in synsets:
        for lemma in syn.lemmas(lang='jpn'):
            if lemma.name() != word:
                synonyms.add(lemma.name())
    return list(synonyms)[:max_num]

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
        base = get_jp_synonyms(ans, max_num=num_choices-1)
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
