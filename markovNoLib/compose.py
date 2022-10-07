import string
import random
from graph import Graph, Vertex

def get_words_from_txt(text_path):
    with open(text_path, 'rb') as f:
        text = f.read().decode("utf-8")

        text = ' '.join(text.split())
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation))

    words = text.split()
    return words


def makeGraph(words):
    g = Graph()
    previous_word = None

    for word in words:
        word_vertex = g.get_vertex(word)
        if previous_word:
            previous_word.increment_edge(word_vertex)

        previous_word = word_vertex
    g.generate_probability_mappings()

    return g

def compose(g, words, length=50):
    compostion = []
    word = g.get_vertex(random.choice(words))
    for _ in range(length):
        compostion.append(word.value)
        word = g.get_next_word(word)

    return compostion

def main():
    words = get_words_from_txt("texts/frankenstein.txt")
    g = makeGraph(words)

    composition = compose(g, words, 30)
    return ' '.join(composition)

if __name__ == '__main__':
    print(main())
