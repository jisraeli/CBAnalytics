import csv
import itertools
import copy

def performCombs():
    current_combination_number = 1
    
    for k in xrange(MIN_CORRECT_PREDICTED_UPSETS, min(MAX_UPSETS_TOTAL, MAX_CORRECT_PREDICTED_UPSETS)):  
    
        k_combs = itertools.combinations(predicted_upsets, k)
        for k_comb in k_combs:
            
            current_k_combination = []
            
            for row in predicted_upsets:
                copy_of_row = copy.deepcopy(row)
                # We add the selected predicted upsets to current_combination.
                if row not in k_comb:
                    # We add the other predicted_upsets upsets to current_combination but change them to non-upsets!
                    copy_of_row[8] = '0'
                    copy_of_row[2] = str(abs(int(copy_of_row[2]) - 1))
                
                current_k_combination.append(copy_of_row)
                

            for n in xrange(0,1):#MIN_UPSETS - k, MAX_UPSETS_TOTAL - k):
                
                n_combs = itertools.combinations(predicted_not_upsets, n)
                for n_comb in n_combs:
                    if current_combination_number > 5000:
                        return
                    
                    current_combination = copy.deepcopy(current_k_combination)

                    for row in predicted_not_upsets:
                        copy_of_row = copy.deepcopy(row)
                        # Since these are NOT upsets already, we make them upsets by flipping their bit, we also
                        # flip the bit of the game outcome.
                        if row in n_comb:
                            # We add the other predicted_upsets upsets to current_combination but change them to non-upsets!
                            copy_of_row[8] = '1'
                            copy_of_row[2] = str(abs(int(copy_of_row[2]) - 1))
                        
                        current_combination.append(copy_of_row)
                        
                    # Add the 16-1 games:
                    for row in bracket_data:
                        if int(row[6]) == 15 or int(row[6]) == -15:
                            current_combination.append(copy.deepcopy(row))

                    print "\nCombination: " + str(current_combination_number) + "\t\tNumber of upsets: " + str(len(current_combination)) + "\n"

                    for row in current_combination:
                        print row
                    
                    current_combination_number += 1

bracket_filename = "2013_bracket_final.csv"

MIN_UPSETS = 9
MIN_PREDICTED_UPSETS = 9
MIN_CORRECT_PREDICTED_UPSETS = 4

MAX_CORRECT_PREDICTED_UPSETS = 7
MAX_UPSETS_TOTAL = 11

with open(bracket_filename, 'rbU') as bracket_file:
    csv_reader = csv.reader(bracket_file)
    bracket_data = [row for row in csv_reader]

predicted_upsets = [row for row in bracket_data if int(row[8]) == 1]
predicted_not_upsets = [row for row in bracket_data if int(row[8]) == 0 and int(row[6]) != 15 and int(row[6]) != -15]

# We need to reverse the order of predicted_non_upsets.
predicted_not_upsets = sorted(predicted_not_upsets, key = lambda x: float(x[4]), reverse=False)

performCombs()