class BowlingFrame():
    def __init__(self, roll1, roll2):
        self.roll1 = roll1
        self.roll2 = roll2

    def score(self):
        return self.roll1 + self.roll2

    def is_spare(self):
        return not self.is_strike() and self.roll1 + self.roll2 == 10

    def is_strike(self):
        return self.roll1 == 10

class Game():
    def __init__(self, frames):
        self.frames = frames

    def score(self):
        score = 0

        for current_frame_index in range(10):
            frame = self.frames[current_frame_index]

            score += frame.score()
            score += self.next_frame_bonus_score(current_frame_index)


        return score

    def next_frame_bonus_score(self, index):
        return self.spare_bonus_score(index) + self.strike_bonus_score(index)

    def spare_bonus_score(self, index):
        currentFrame = self.frames[index]
        if currentFrame.is_spare() and index < 9:
            next_frame = self.frames[index + 1]
            return next_frame.roll1
        return 0

    def strike_bonus_score(self, index):
        currentFrame = self.frames[index]

        if not currentFrame.is_strike():
            return 0

        next_frame = self.frames[index + 1]

        if not next_frame.is_strike() or index >= 8:
            return next_frame.score()

        next_next_frame = self.frames[index + 2]
        return next_frame.roll1 + next_next_frame.roll1


def test_no_strike_no_spare_game():
    frames = [BowlingFrame(1,1)] * 10
    game = Game(frames)
    assert game.score() == 20

    frames = [BowlingFrame(9,0)] * 10
    game = Game(frames)
    assert game.score() == 90

def test_game_with_one_spare():
    frames = [BowlingFrame(5,5), BowlingFrame(1,1)] + [BowlingFrame(0,0)] * 8
    game = Game(frames)
    assert game.score() == 5+5 + 1*2  + 1
    frames = [BowlingFrame(5,2), BowlingFrame(7,3), BowlingFrame(2,2)] + [BowlingFrame(0,0)]* 7
    game = Game(frames)
    assert game.score() == 7 + 10 + 2 + 4

def test_two_spares_in_a_row():
    frames = [BowlingFrame(5,5), BowlingFrame(7,3), BowlingFrame(2,2)] + [BowlingFrame(0,0)] * 7
    game = Game(frames)
    assert game.score() == 10 + 7 + 10 + 2 + 4

def test_game_with_a_single_strike():
    frames = [BowlingFrame(10, 0), BowlingFrame(2,5)] + [BowlingFrame(0,0)] * 8
    game = Game(frames)
    assert game.score() == 10 + 2 + 5 + 7

def test_game_with_two_strikes_in_a_row():
    frames = [BowlingFrame(10, 0), BowlingFrame(10,0), BowlingFrame(5,2)] + [BowlingFrame(0,0)] * 7
    game = Game(frames)
    assert game.score() == 10 + (10 + 5) + 10 + (5 + 2) + 7
