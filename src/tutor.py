from src.audio import Audio
from src.characters import pronunciation
import random
import time
from src.app import App
import string

class Tutor(App):

    def on_start(self):
        # todo: to be implemented shortly
        #self.audio.start_background_listening('stop')

        # instruction when app started, skip when user says skip
        self.app_instruction("The purpose of this application is to test how much you have learnt from Learn. Let's start testing. "
                             "You can answer the question with any word of your choice that starts with the letter you believe to be the correct answer, "
                             "but avoid using quit or exit unless you want to quit the application.")
        self.run_test()

    def run_test(self):
        # initialise good_pile and bad_pile
        good_pile = []
        bad_pile = []
        score = 0
        self.audio.speak("How would you like the length of the test be? Please choose one from the following: short, medium or full.")
        test_length_reply = self.audio.recognize_speech(app=self)["transcription"]

        if "short" in test_length_reply:
            test_length = "short"
        elif "medium" in test_length_reply:
            test_length = "medium"
        elif "full" in test_length_reply:
            test_length = "full"
        else:
            test_length = "short"

        for (c, chartype) in self.characters_shuffled(test_length=test_length):
            # initialise variables for each question
            chances = 3
            # display each character
            self.cells[1].print_character(c)

            #give instruction: digit/punctuation/special indicator/alphabet
            chartypes_output = {
                'alphabet': 'an alphabet character',
                'punctuation': 'a punctuation character',
                'indicator': 'a special indicator',
                'digit': 'a digit'
            }
            self.audio.speak('What letter is this? This is ' + chartypes_output[chartype] + '.')

            while chances > 0:
                answer = self.audio.recognize_speech(app=self)["transcription"]
                if answer == '': # speech recognizer returned error
                    self.audio.speak("I didn't quite get that. Please respond again.")
                    continue

                answer = answer.lower().strip()

                if chartype == 'alphabet':
                    correct_answer = c
                    # cut down length of input word to one character
                    # to allow 'Apple' for 'A' etc.
                    answer = answer[0]
                elif chartype == 'indicator':
                    correct_answer = c.lower()
                else: # digit or punctuation
                    correct_answer = pronunciation[c]

                if answer.find(correct_answer) != -1:
                    self.audio.speak('You correctly answered ' + pronunciation[c] + '! Moving on to the next question.')
                    good_pile.append(c)
                    score += 1
                    break
                else:
                    answer_output = answer
                    if answer in pronunciation:
                        answer_output = pronunciation[answer]

                    chances -= 1
                    if chances > 0:
                        self.audio.speak("You incorrectly answered " + answer_output + ". You have " + str(chances) + " more chances to respond.")
                    else:
                        self.audio.speak("You incorrectly answered " + answer_output + ". You have used all your chances to answer. The correct answer is " + pronunciation[c])
                        self.audio.speak("I will save this character for later.")
                        bad_pile.append(c)
                        self.audio.speak("Moving on to the next question.")

        self.test_done_instruction(bad_pile, score)

    def test_done_instruction(self, bad_pile, score):
        score_percentage = round(score * 100 / len(self.characters_shuffled()), 1)
        self.audio.speak("Testing is done. You got " + str(score_percentage) + " percent right.")

        if score_percentage != 100:
            self.audio.speak("Would you like to go through letters you got wrong?")
            if self.audio.recognize_speech()["transcription"] == "yes":
                self.audio.speak("Okay, lets go through the characters you answered wrong. You can move on to the next character by saying next.")
                for c in bad_pile:
                    self.cells[1].print_character(c)
                    self.audio.speak("This is " + pronunciation[c])
                    self.wait_for_audio("next")
                self.audio.speak("That were all the characters you answered wrong.")
        else:
            self.audio.speak("Well done!")

        self.audio.speak("Do you want to take another test?")
        if self.audio.recognize_speech()["transcription"] == "yes":
            self.run_test()

        self.audio.speak("The app will now close itself.")
        self.on_quit()

    def characters_shuffled(self, test_length):
        chars = (
            [(char, 'alphabet') for char in list(string.ascii_lowercase)] +
            [(char, 'punctuation') for char in self.punctuation()] +
            [(char, 'indicator') for char in self.special_indicators()] +
            [(char, 'digit') for char in list(string.digits)]
        )

        chars_shuffled_short = random.sample(chars, 10)
        chars_shuffled_mid = random.sample(chars, 20)
        chars_shuffled_full = random.sample(chars, len(chars[0])+len(chars[1])+len(chars[2])+len(chars[3]))

        if test_length == "short":
            return chars_shuffled_short
        elif test_length == "medium":
            return chars_shuffled_mid
        elif test_length == "full":
            return chars_shuffled_full
        else:
            return chars_shuffled_short

    def punctuation(self):
        return ['.', ',', ';', ':', '/', '?', '!', '@', '#', '+', '-', '*', '<', '>', '(', ')', ' ']

    def special_indicators(self):
        return ["CAPITAL", "LETTER", "NUMBER"]
