from generate_jp_quiz import generate_japanese_quizzes,generate_japanese_writing_quizzes
from generate_eng_quiz import generate_eng_choice_question,generate_eng_writing_question
from text_extraction import contains_japanese


def generate_quizzes_auto(sentences, num_choices=4):
    japanese_sentences = []
    english_sentences = []

    for sentence in sentences:
        if contains_japanese(sentence):
            japanese_sentences.append(sentence)
        else:
            english_sentences.append(sentence)

    quizzes = []

    if japanese_sentences:
        quizzes += generate_japanese_quizzes(japanese_sentences)

    if english_sentences:
        quizzes += generate_eng_choice_question(english_sentences, num_choices=num_choices)

    return quizzes

def generate_writing_quizzes_auto(sentences):
    japanese_sentences = []
    english_sentences = []

    for sentence in sentences:
        if contains_japanese(sentence):
            japanese_sentences.append(sentence)
        else:
            english_sentences.append(sentence)

    quizzes = []

    if japanese_sentences:
        quizzes += generate_japanese_writing_quizzes(japanese_sentences)

    if english_sentences:
        quizzes += generate_eng_writing_question(english_sentences)

    return quizzes
