import os

class ScoreManager:
    def __init__(self, filename='high_scores.txt'):
        self.filename = filename
        self.scores = self.load_scores()

    def add_score(self, name, score):
        print(f"Adding score: {name}, {score}")
        self.scores.append((name, score))
        self.scores.sort(key=lambda x: x[1], reverse=True)  # Ordena por pontuação, maior primeiro

    def save_scores(self):
        with open(self.filename, 'w') as file:
            for name, score in self.scores:
                file.write(f"{name},{score}\n")

    def load_scores(self):
        scores = []
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as file:
                for line in file:
                    name, score = line.strip().split(',')
                    scores.append((name, int(score)))
        return scores

    def get_top_scores(self, n=3):
        return self.scores[:n]
