from common.dealerState import DealerHand
from common.deck import Deck
from common.playerState import PlayerHand
from copy import deepcopy

import config.gameConfig as game_config


class Calculator:
    def __init__(self) -> None:
        self.memo = {}
        self.dealer_memo = {}
        return

    def evaluate(self, player_hand: PlayerHand, dealer_hand: DealerHand, calc_deck, depth=1):
        if ((player_hand.hand), (dealer_hand.hand),  tuple(calc_deck)) in self.memo:
            return self.memo[((player_hand.hand), (dealer_hand.hand),  tuple(calc_deck))]

        results_dict = {}

        results_dict["STAND"] = self.getEVForStanding(
            player_hand, dealer_hand, calc_deck)
        results_dict["HIT"] = self.getEVForHitting(
            player_hand, dealer_hand, calc_deck, depth)

        move = max(results_dict, key=results_dict.get)

        self.memo[((player_hand.hand), (dealer_hand.hand),  tuple(calc_deck))] = (
            move, results_dict[move], results_dict)

        if depth == 1:
            print(results_dict)
        return move, results_dict[move], results_dict

    def getEVForStanding(self, player_hand: PlayerHand, dealer_hand: DealerHand, calc_deck):
        player_hand_val, player_hand_num_aces = player_hand.hand

        if player_hand_num_aces > 0 and player_hand_val <= 11:
            player_hand_val += 10

        # If the player got blackjack
        if (player_hand_num_aces == 1 and player_hand_val == 11):
            return game_config.BLACKJACK_SCORE_MULTIPLIER

        new_res = self.calcDealerPercentages(dealer_hand.hand, calc_deck)

        evIfHappens = self.getEvFromWeightedArray(player_hand_val, new_res)
        return evIfHappens

    def getEVForHitting(self, player_hand: PlayerHand, dealer_hand: DealerHand, calc_deck, depth):
        player_hand_val, player_hand_num_aces = player_hand.hand
        num_cards_in_deck = sum(calc_deck)

        ev_array = []

        # for each card type, deal and get EV
        for ind, num_cards in enumerate(calc_deck):
            new_deck = deepcopy(calc_deck)

            if new_deck[ind] <= 0:
                continue
            else:
                #  remove drawn card from deck and give it to the player
                prob_i_get_here = num_cards / num_cards_in_deck
                new_deck[ind] -= 1

                new_player_val = player_hand_val + ind + 1
                new_num_aces = player_hand_num_aces

                if ind == 0:
                    new_num_aces += 1

                if new_player_val >= 22:
                    ev_array.append((prob_i_get_here, -1))

                elif new_player_val == 21 or (player_hand_num_aces == 1 and player_hand_val == 11):
                    new_res = self.calcDealerPercentages(
                        dealer_hand.hand, new_deck)
                    ev_if_happens = self.getEvFromWeightedArray(
                        new_player_val, new_res)
                    ev_array.append((prob_i_get_here, ev_if_happens))

                else:
                    new_player_hand = deepcopy(player_hand)
                    new_player_hand.addCard(str(ind + 1) + "_" + "any")
                    action, ev_if_happens, results_dict = self.evaluate(
                        new_player_hand, dealer_hand, new_deck, depth + 1)
                    ev_array.append((prob_i_get_here, ev_if_happens))

        ev_for_hitting = 0

        for i in range(len(ev_array)):
            prob, indv_ev_val = ev_array[i]
            ev_for_hitting += (prob * indv_ev_val)

        return ev_for_hitting

    def calcDealerPercentages(self, dealer_hand, calc_deck):
        if (((dealer_hand), tuple(calc_deck))) in self.dealer_memo:
            return self.dealer_memo[((dealer_hand), tuple(calc_deck))]

        val, num_aces = dealer_hand
        should_stop, final_val = self.getShouldStop(dealer_hand)
        # under these conditions we use softstop
        if (should_stop):
            res = [0] * 22
            res[final_val] = 1
            self.dealer_memo[((dealer_hand), tuple(calc_deck))] = res
            return res

        else:
            bust_ind, bust_prob = self.getBustProbAndInd(
                dealer_hand, calc_deck)
            if bust_ind == -1:
                slice_of_deck = calc_deck
            else:
                slice_of_deck = calc_deck[0: bust_ind]
            deck_sum = sum(calc_deck)
            accum_array = []

            # handle immediate bust case
            res = [0] * 22
            res[0] = 1
            accum_array.append((bust_prob, res))

            for ind, num_cards in enumerate(slice_of_deck):
                new_deck = deepcopy(calc_deck)
                if new_deck[ind] <= 0:
                    continue
                else:
                    new_val = val + ind + 1
                    new_num_aces = num_aces
                    if ind == 0:
                        new_num_aces += 1
                    new_res = self.calcDealerPercentages(
                        (new_val, new_num_aces), new_deck)
                    prob_i_get_here = num_cards / deck_sum
                    accum_array.append((prob_i_get_here, new_res))

            final_res_array = [0] * 22

            for i in range(len(accum_array)):
                prob, indiv_accum_array = accum_array[i]
                for ind, indvProb in enumerate(indiv_accum_array):
                    final_res_array[ind] += indvProb * prob

            self.dealer_memo[((dealer_hand), tuple(calc_deck))
                             ] = final_res_array
            return final_res_array

    def getShouldStop(self, dealer_hand):
        val, num_aces = dealer_hand

        if val > 21:
            return (True, 0)

        else:
            return (val >= game_config.DEALER_STOP, val)

    def getBustProbAndInd(self, hand, deck):
        val, num_aces = hand

        if val < 12:
            return (-1, 0)

        bustVal = 22 - val
        index = bustVal - 1
        return (index, sum(deck[index:]) / sum(deck))

    def getEvFromWeightedArray(self, given_hand_num, weighted_array):
        # ind == 0 if dealer busts, and if not its the value of the dealer's hand
        # So the EV is Prob Loss * -1 + prob win * 1
        runningEv = 0
        for ind, prob in enumerate(weighted_array):
            # dealerBusts
            if (ind == 0):
                runningEv += (prob * 1)
            else:
                # player hand higher than user
                if ind > given_hand_num:
                    runningEv += (prob * -1)
                # dealer better hand than player
                elif ind < given_hand_num:
                    runningEv += (prob * 1)

        return runningEv
