import random
import OpenHowNet
from janome.tokenizer import Tokenizer
import os

if not os.path.exists(os.path.expanduser("~/.openhownet/en_wn_data_v1.json")):
    print("📥 OpenHowNet辞書をダウンロード中...")
    OpenHowNet.download()

hownet = OpenHowNet.HowNetDict()
tokenizer = Tokenizer()

def get_jp_synonyms(word, max_num=3):
    sememe_infos = hownet.get_sememes_by_word(word)
    synonyms = set()
    for info in sememe_infos:
        sememe_list = info.get("sememes", [])
        for sememe in sememe_list:
            senses = hownet.get_senses_by_sememe(sememe)
            for sense in senses:
                candidate = sense.get("word", "")
                if candidate != word:
                    synonyms.add(candidate)
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
