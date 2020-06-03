import random


# Roll class for categories of the game and rolling dice
class Roll:
    def __init__(self):
        self._current_dice_list = []
        self._current_kept_dice = []

    def single_values(self, dice_list, check_value):
        roll_score = 0
        for die in dice_list:
            if die == check_value:
                roll_score += die
        return roll_score

    def check_pair(self, dice_list):
        dice_list.sort()
        if dice_list[0] == dice_list[1] or dice_list[1] == dice_list[2] or dice_list[2] == dice_list[3]or dice_list[3] == dice_list[4]:
            return dice_list
        return 0

    def check_two_pairs(self, dice_list):
        dice_list.sort()
        if (dice_list[0] == dice_list[1] and dice_list[2] == dice_list[3]) or (dice_list[0] == dice_list[1] and dice_list[3] == dice_list[4]) or (dice_list[1] == dice_list[2] and dice_list[3] == dice_list[4]):
            return dice_list
        return 0

    def check_three_kind(self, dice_list):
        dice_list.sort()
        if dice_list[0] == dice_list[2] or dice_list[1] == dice_list[3] or dice_list[2] == dice_list[4]:
            return dice_list
        return 0

    def check_four_kind(self, dice_list):
        dice_list.sort()
        if dice_list[0] == dice_list[3] or dice_list[1] == dice_list[4]:
            return dice_list
        return 0

    def check_small_straight(self, dice_list):
        dice_list.sort()
        if len(set(dice_list)) == 5 and dice_list[4] == 5 and dice_list[0] == 1:
            return 15
        return 0

    def check_large_straight(self, dice_list):
        dice_list.sort()
        if len(set(dice_list)) == 5 and dice_list[4] == 6 and dice_list[0] == 2:
            return 20
        return 0

    def check_full_house(self, dice_list):
        dice_list.sort()
        if (len(set(dice_list))) != 2:
            return 0
        if dice_list[0] != dice_list[3] or dice_list[1] != dice_list[4]:
            return dice_list
        return 0

    def check_chance(self, dice_list):
        return dice_list[0]+dice_list[1]+dice_list[2]+dice_list[3]+dice_list[4]

    def check_yatzy(self, dice_list):
        if len(set(dice_list)) == 1:
            return 50
        return 0

    def roll_dice(self):
        self._current_kept_dice.clear()
        self._current_dice_list = [random.randint(1, 6) for die in range(0, 5)]
        print(f'You rolled {self._current_dice_list} ! \n')
        return self._current_dice_list

    def keep_dice(self):
        while True:
            keep_input = input('which dice do you want to keep?(comma separated: e.g. 1,1,5): ')
            split_input = keep_input.split(',')
            split_input_int = [int(item) for item in split_input]

            # if the user types nothing keep all:
            if keep_input == '':
                return self._current_dice_list
            elif any(die not in self._current_dice_list for die in split_input_int):
                continue
            elif any(split_input_int.count(die) > self._current_dice_list.count(die) for die in split_input_int):
                print("Wrong Selection Try again")

                continue
            else:
                for die in split_input_int:
                    self._current_kept_dice.append(die)
                break

        for value in self._current_kept_dice:
            if value in self._current_dice_list:
                self._current_dice_list.remove(value)
        return self._current_dice_list

    def reroll_dice(self, dice_list):
        self._current_dice_list = [random.randint(1, 6) for die in range(0, (len(dice_list)))]
        print(f'You rolled: {self._current_dice_list} !')
        return self._current_dice_list

    def get_current_dice(self):
        return self._current_dice_list

    def get_kept_dice(self):
        return self._current_kept_dice

    # all the dices are kept on the last roll
    def forced_keep(self, dice_list):
        for die in dice_list:
            self._current_kept_dice.append(die)


# player class for keeping track of players and scores
class Player:
    def __init__(self, name):
        self.name = name
        self._scoreboard = {}
        self._top_score = 0
        self._bottom_score = 0
        self._bonus_bottom = 0
        self._total_score = 0

    def add_rolled(self, rolled_type, value):
        self._scoreboard[rolled_type] = value

    def add_top_score(self, value):
        self._top_score += value

    def get_top_score(self):
        print('TOTAL=', self._top_score)
        return self._top_score

    def print_scoreboard(self):
        for key, value in self._scoreboard.items():
            print(f'{key} : {value}')


# main function
def main():
    game_list_top = ['ACES', 'TWOS', 'THREES', 'FOURS', 'FIVES', 'SIXES']
    game_list_top_values = [1, 2, 3, 4, 5, 6]

    winner = []
    winner_points = []
    # create a player and a dice to play.
    no = int(input("How many players?"))
    player1 = []

    for i in range(no):
        player1.append(Player(input(f" Enter Name of Player{i+1}:")))
        dice1 = Roll()

    print("\n\n")

    def play():
        # first roll:
        dice1.roll_dice()
        keep1 = dice1.keep_dice()
        # second roll:
        dice1.reroll_dice(keep1)
        keep2 = dice1.keep_dice()
        # third roll:
        roll3 = dice1.reroll_dice(keep2)
        dice1.forced_keep(roll3)
        print("ALL DICE KEPT(LAST TURN)")

    # logic of thr game
    for i in player1:
        print(i.name, " TURN")
        for index, item in enumerate(game_list_top):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            # the final roll collection of dice goes in for check
            final_roll_collection = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection}')
            # check what the score is for this particular roll
            check_score = dice1.single_values(final_roll_collection, game_list_top_values[index])
            # add the total score
            i.add_rolled(item, check_score)
            i.add_top_score(check_score)

        bottom = ['PAIR']
        for index, item in enumerate(bottom):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection2 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection2}')
            check_score2 = dice1.check_pair(final_roll_collection2)
            if check_score2 == 0:
                i.add_rolled(item, 0)
                i.add_top_score(0)
                break

            i.add_rolled(item, 2*check_score2[0])
            i.add_top_score(check_score2[0]*2)

        bottom2 = ['TWO PAIR']
        for index, item in enumerate(bottom2):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection3 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection3}')
            check_score3 = dice1.check_two_pairs(final_roll_collection3)
            if check_score3 == 0:
                i.add_rolled(item, 0)
                i.add_top_score(0)
                break

            i.add_rolled(item, check_score3[0]+check_score3[1]+check_score3[2]+check_score3[3])
            i.add_top_score(check_score3[0]+check_score3[1]+check_score3[2]+check_score3[3])

        bottom3 = ['THREE OF A KIND']
        for index, item in enumerate(bottom3):
            print('-' * 40, '\n rolling for', item, '\n', '-' * 40)
            play()
            final_roll_collection4 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection4}')
            check_score4 = dice1.check_three_kind(final_roll_collection4)
            if check_score4 == 0:
                i.add_rolled(item, 0)
                i.add_top_score(0)
                break

            i.add_rolled(item, 3*check_score4[0])
            i.add_top_score(3*check_score4[0])

        bottom4 = ['FOUR OF A KIND']
        for index, item in enumerate(bottom4):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection5 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection5}')
            check_score5 = dice1.check_four_kind(final_roll_collection5)
            if check_score5 == 0:
                i.add_rolled(item, 0)
                i.add_top_score(0)
                break

            i.add_rolled(item, 4*check_score5[0])
            i.add_top_score(4*check_score5[0])

        bottom5 = ['SMALL STRAIGHT']
        for index, item in enumerate(bottom5):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection6 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection6}')
            check_score6 = dice1.check_small_straight(final_roll_collection6)
            i.add_rolled(item, check_score6)
            i.add_top_score(check_score6)

        bottom6 = ['LARGE STRAIGHT']
        for index, item in enumerate(bottom6):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection7 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection7}')
            check_score7 = dice1.check_large_straight(final_roll_collection7)
            i.add_rolled(item, check_score7)
            i.add_top_score(check_score7)

        bottom7 = ['FULL HOUSE']
        for index, item in enumerate(bottom7):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection8 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection8}')
            check_score8 = dice1.check_full_house(final_roll_collection8)
            if check_score8 == 0:
                i.add_rolled(item, 0)
                i.add_top_score(0)
                break

            i.add_rolled(item, check_score8[0]+check_score8[1]+check_score8[2]+check_score8[3]+check_score8[4])
            i.add_top_score(check_score8[0]+check_score8[1]+check_score8[2]+check_score8[3]+check_score8[4])

        bottom8 = ['YATZY']
        for index, item in enumerate(bottom8):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection9 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection9}')
            check_score9 = dice1.check_yatzy(final_roll_collection9)
            i.add_rolled(item, check_score9)
            i.add_top_score(check_score9)

        bottom9 = ['CHANCE']
        for index, item in enumerate(bottom9):
            print('-' * 40, '\n Rolling For', item, '\n', '-' * 40)
            play()
            final_roll_collection10 = dice1.get_kept_dice()
            print(f'Final Roll Collection: {final_roll_collection10}')
            check_score10 = dice1.check_chance(final_roll_collection10)
            i.add_rolled(item, check_score10)
            i.add_top_score(check_score10)
    # print current score for the player
        print("\nScoreboard For:", i.name)
        i.print_scoreboard()
        print("\n\n")
        winner.append(i.name)
        winner_points.append(i.get_top_score())
    winner.sort()
    print("FINAL SCOREBOARD:\n   Name    Points")
    for j in range(no):
        print(f"{j+1}.", winner[j], "      ", winner_points[j])


main()
