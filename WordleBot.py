from random import choice


def WordleBot():
    word_list = extract_word_list()
    Introductions()
    average = 0
    for x in range(1, 100):
        average += solve_wordle(word_list)
    print(average/100)


def grade_guess(solution, guess):
    grade = ''
    list_guess = list(guess)
    list_solution = list(solution)
    seen_letters = []
    for letter in list_guess:
        solution_appearances = [x for x, v in enumerate(solution) if v == letter]
        guess_appearances = [x for x, v in enumerate(guess) if v == letter]
        if letter in solution:
            guess_index = guess_appearances[seen_letters.count(letter)]
            if guess_index in solution_appearances:
                grade += f'{letter}3 '
            else:
                grade += f'{letter}1 '
        else:
            grade += f'{letter}0 '
        seen_letters.append(letter)
    return grade


def Introductions():
    print('Hello! Thanks for checking out my WordleBot!'
          '\nTo enter a guess, put each letter followed by \'0\', \'1\', or \'3\' and a space:'
          '\n\'0\': The letter is grey, and is not contained in the word.'
          '\n\'1\': The letter is yellow, and is in the word in a different spot.'
          '\n\'3\': The letter is green, and is in the word in that spot.'
          '\nHere\'s an example input: \'h0 eY l0 l0 oG\''
          '\nIn this case, \'e\' is in the word, and \'o\' is the last letter.'
          '\nAfter every guess, the WordleBot will provide you with a list of words that could be the solution.'
          '\nThe WordleBot will automatically place the most common words at the beginning of the list.'
          '\nGood luck, Have fun!')


def extract_word_list():
    with open('5_letter_words.txt') as words:
        word_string = words.read()
        word_list = word_string.splitlines()
    return word_list


def solve_wordle(word_list):
    viable_words = list(word_list)
    the_word = {}  # Format: [index : [is, [is not]]]
    for x in range(0, 5):
        the_word[x] = ['', []]
    word_contains = []
    word_does_not_contain = []
    solution = choice(word_list)
    score = 0
    print(f'####SOLUTION####: \'{solution}\'')
    bot_guess = grade_guess(solution, 'irate')
    while len(viable_words) > 1:
        guess = bot_guess
        print(f'Guessing: \'{guess}\'...')
        guess_list = list(guess.replace(' ', ''))
        for x in range(0, 9):
            if x % 2 == 0:
                index = int(x / 2)
                if guess_list[x + 1] == '0':
                    is_green_elsewhere = False
                    for num in range(0, 5):
                        if the_word[num][0] == guess_list[x]:
                            is_green_elsewhere = True
                    if not is_green_elsewhere:
                        for num in range(0, 5):
                            the_word[num][1].append(guess_list[x])
                        word_does_not_contain.append(guess_list[x])
                if guess_list[x + 1] == '1':
                    word_contains.append(guess_list[x])
                    the_word[index][1].append(guess_list[x])
                if guess_list[x + 1] == '3':
                    the_word[index][0] = guess_list[x]
        print(f'Data gathered from this guess: {the_word}')
        print(f'Number of possible solutions before filtering: {len(viable_words)}')
        for word in word_list:
            # Check we have all known yellow letters
            if len(word_contains) >0:
                contains_all_yellow_letters = True
                word_to_list = list(word)
                for letter in word_contains:
                    if letter not in word_to_list:
                        contains_all_yellow_letters = False
                if not contains_all_yellow_letters and word in viable_words:
                    viable_words.remove(word)
                    if word == solution:
                        print(f'!!!!!!!YELLOW WEEDED SOLUTION: {solution}')

            for index in range(0, 5):
                if len(word_contains) > 0:
                    # Any words with yellow letters in the same spot are not viable
                    for yellow_letter in the_word[index][1]:
                        yellow_char_appearances = [x for x, v in enumerate(word) if v == yellow_letter]
                        if yellow_letter in word and index in yellow_char_appearances and word in viable_words:
                            viable_words.remove(word)
                            if word == solution:
                                print(f'!!!!!!!YELLOW2 WEEDED SOLUTION: {solution}')
                # If we have green letters, make sure the word has them and that they're in the right spot.
                if not the_word[index][0] == '' and the_word[index][0] not in word and word in viable_words:
                    viable_words.remove(word)
                    if word == solution:
                        print(f'!!!!!!!GREEN WEEDED SOLUTION: {solution}')

                if not the_word[index][0] == '' and the_word[index][0] in word and word in viable_words:
                    char_appearances = [x for x, v in enumerate(word) if v == the_word[index][0]]
                    if index not in char_appearances and word in viable_words:
                        viable_words.remove(word)
                        if word == solution:
                            print(f'!!!!!!!GREEN2 WEEDED SOLUTION: {solution}')

                # Check we don't have any uncontained letters
                if the_word[index][1] is not None:
                    for uncontained_letter in word_does_not_contain:
                        if uncontained_letter in word and word in viable_words:
                            viable_words.remove(word)
                            if word == solution:
                                print(f'!!!!!!!UNCONTAINED WEEDED SOLUTION: {solution}')
        print(f'Number of possible solutions after input: {len(viable_words)}')
        # print(f'Remaining possible solutions: {viable_words}')
        bot_guess = grade_guess(solution, viable_words[0])
        score += 1
    print(f'Game over, XXXXXXXXXX SCORE: {score} XXXXXXXXXX\n\n')
    return score


if __name__ == '__main__':
    WordleBot()
