import os
import csv
import operator
import random
from dateutil import parser

import Constants
import SeasonMatcher
import KaggleMatcher

num_players = 2

train_file = open('input_data/combined_final_train.csv', "w")
test_file = open('input_data/combined_final_test.csv', "w")

outputted_teams_by_team_name = {}

team_players_hash = {}
empty_teams_hash = {}
random.seed(54342)

max_games_by_team = {}

all_years = [Constants.year]
all_years.extend(Constants.other_years)

for rootdir_index, rootdir in enumerate(all_years):
    rootdir_index = rootdir
    rootdir = Constants.rootdirs[rootdir]

    march_madness_start_datetime = Constants.dates[rootdir_index]
    march_madness_end_datetime = Constants.end_dates[rootdir_index]

    records_directory = rootdir + '_records'
    
    for subdir, dirs, files in os.walk(rootdir):
        for team_file_index, team_file in enumerate(files):
            
            team_name = team_file[:-9] + "_" + rootdir
            
            if team_name[:-5] not in KaggleMatcher.final_teams_indices:
                continue
            
            #print team_name
    
            #print '\n' + team_name
            
            all_rows = []
            sorted_all_rows = []
            
            max_games_by_team[team_name] = 0.0
            
            with open(rootdir + '/' + team_file, 'rb') as f:
                
                csv_reader = csv.reader(f)
                
                metrics_by_row_index = {}
                
                column_titles = []
                for row_index, row in enumerate(csv_reader):
                    all_rows.append(row)
                    
                    if(row_index == 0):
                        column_titles = row
                        continue
                    
                    if '-' in row:
                        continue
                    
                    games_played_index = column_titles.index('G')
                    games_played = int(row[games_played_index])
                    if games_played == 0:
                        continue

                    if max_games_by_team[team_name] < games_played:
                        max_games_by_team[team_name] = games_played
                    
            
            with open(rootdir + '/' + team_file, 'rb') as f:
                
                csv_reader = csv.reader(f)
                
                metrics_by_row_index = {}
                
                column_titles = []
                for row_index, row in enumerate(csv_reader):
                    all_rows.append(row)
                    
                    if(row_index == 0):
                        column_titles = row
                        continue
                    
                    if '-' in row:
                        continue
                    
                    games_played_index = column_titles.index('G')
                    games_played = int(row[games_played_index])
                    if games_played == 0:
                        continue

                    metric = float(games_played) + float(row[16])
                                                       
                    feet_and_inches = row[4].split("-")
                    row[4] = (12.0 * int(feet_and_inches[0]) + int(feet_and_inches[1])) / 8.0
    
                    school_year_index = column_titles.index('school_year')
                    
                    if row[school_year_index] == 'Fr.':
                        row[school_year_index] = 1.0 / 4;
                    
                    if row[school_year_index] == 'So.':
                        row[school_year_index] = 2.0 / 4;
                        
                    if row[school_year_index] == 'Jr.':
                        row[school_year_index] = 3.0 / 4;
                        
                    if row[school_year_index] == 'Sr.':
                        row[school_year_index] = 4.0 / 4;
                        
                    if row[school_year_index] == '---':
                        continue

                    if row[3] == 'C':
                        row[3] = 1.0 / 3;
    
                    if row[3] == 'F':
                        row[3] = 2.0 / 3;
    
                    if row[3] == 'G':
                        row[3] = 3.0 / 3;
                        
                    #field_goal_percent_index = column_titles.index('field_goal_percent')
                    #three_pointer_percent_index = column_titles.index('three_pointer_percent_index')
                    
                    for feature_index, feature in enumerate(row):
                        if  feature_index == 6 or feature_index == 7 or feature_index == 9 or feature_index == 10 or feature_index == 12 or feature_index == 13 or feature_index == 15 or feature_index == 17 or feature_index == 19 or feature_index == 21 or feature_index == 23 or feature_index == 25:
                            row[feature_index] = float(row[feature_index]) /  (float(row[5]) + 1)

                    filtered_row = [float(item) for index, item in enumerate(row) if index >= 6]# index != 0 and index != 2 and index != 5]# index == 4 or  index == 16 or index == 8 or index == 12 or index == 14 or index == 24 or index == 25] #index != 0 and index != 2 and index != 5 and index != 6 and index != 7 and index != 9 and index != 10  and index != 12 and index != 13 and index != 15 and index != 17 and index != 19 and index != 21 and index != 23]
                    
                    #metric = float(filtered_row[1] + float(row[16]) + 1)
                        
                    filtered_row[len(filtered_row) - 1] /= games_played
                    
                    all_rows[row_index] = filtered_row
                    metrics_by_row_index[row_index] = metric
                
                sorted_x = sorted(metrics_by_row_index.iteritems(), key=operator.itemgetter(1), reverse=True)
            
            
            #print str(team_name) + "\t" + str(filtered_row)
            for item in sorted_x:
                sorted_all_rows.append(all_rows[item[0]])
            
            if len(sorted_all_rows) < 1:
                empty_teams_hash[team_name] = []
                continue
            
            all_rows_appended = []
            
            for i in xrange(0, num_players):
                if i < len(sorted_all_rows):
                    all_rows_appended.extend(sorted_all_rows[i])
                else:
                    all_rows_appended.extend([0] * len(sorted_all_rows[0]))
            
            n_stats_per_player = len(sorted_all_rows[0])

            team_players_hash[team_name] = all_rows_appended

    for subdir, dirs, files in os.walk(records_directory):
        for team_file_index, team_file in enumerate(files):
            #print team_file
            #print team_file_index
            #print team_file
            with open(records_directory + "/" + team_file, 'rbU') as f:
                team_name = team_file[:-11] 
                team_name = team_name.split('_')[1]
                team_name += "_" + rootdir
                csv_reader = csv.reader(f)
                print team_name
                for row in csv_reader:
                    competitor = row[0] + "_" + rootdir
                    
                    if competitor == 'N.C. A&T':
                        competitor = 'North Carolina St.'
                    
                    if competitor == 'Connecticut':
                        competitor = 'UConn'
                        
                    if competitor == 'Northeastern St.':
                        competitor = 'Northeastern'
                    
                    if competitor == 'Albany St. (GA)':
                        competitor = 'Albany (NY)'
    
                    if competitor == 'Ga. Southwestern':
                        competitor = "Ga. Southern"
                       
                    if competitor in empty_teams_hash:
                        continue
                    
                    date = row[1]
                    
                    time_of_match = parser.parse(date)
            
                    home_score = int(row[2])
                    competitor_score = int(row[3])
                    
                    outcome = 0
                    if home_score > competitor_score:
                        outcome = 1
                        
                    num_in_attendance = float(row[7].replace(',', '')) / 75421
            
                    if team_name not in team_players_hash:
                        continue
                    
                    if team_name in outputted_teams_by_team_name and competitor in outputted_teams_by_team_name[team_name]:
                        continue
                    
                    this_team_stats = team_players_hash[team_name][:]
                    if competitor in team_players_hash:
                        competitor_stats = team_players_hash[competitor]
                        
                        stats = []
                        stat_row_duplicate = []
                    
                        stat_start_index = 0
                        
                        for player_index in xrange(0, num_players):
                            for j in xrange(0, n_stats_per_player):
                                
                                t1_p =  this_team_stats[stat_start_index + j + player_index * n_stats_per_player]
                                t2_p =  competitor_stats[stat_start_index + j + player_index * n_stats_per_player]
                                stats.append(str(t1_p - t2_p))
                        '''
                        stats_temp = stats[:]
                        for feature_1_index, feature_1 in enumerate(stats_temp):
                            for feature_2 in stats_temp[feature_1_index:]:
                                stats.append(str(float(feature_1) * float(feature_2)))
                        '''
                                
                        if rootdir_index == Constants.year:

                            if (time_of_match.date() > march_madness_start_datetime.date()):# and time_of_match.date() < march_madness_end_datetime.date()):
                                '''
                                found = False
                                team_name_kaggle_num = KaggleMatcher.final_teams_indices[team_name[:-5]]
                                for conference in SeasonMatcher.conferences_by_year[rootdir]:
                                    if team_name_kaggle_num in SeasonMatcher.conferences_by_year[rootdir][conference]:
                                        found = True
                                    
                                found = False
                                competitor_kaggle_num = KaggleMatcher.final_teams_indices[competitor[:-5]]
                                team_name_kaggle_num = KaggleMatcher.final_teams_indices[team_name[:-5]]
                                for conference in SeasonMatcher.conferences_by_year[rootdir]:
                                    if competitor_kaggle_num in SeasonMatcher.conferences_by_year[rootdir][conference]:
                                        found = True

                                if not found:
                                    continue
                                '''

                                test_file.write(team_name + ',' + competitor + ',' +  ','.join(stats) +  ',' + str(num_in_attendance) + ',' + str(outcome) + '\n')
                            #else:
                            #    train_file.write(team_name + ',' + competitor + ',' + ','.join(stats) +  ',' + str(num_in_attendance) + ',' + str(outcome) + '\n')
                            
                        #if rootdir == '2012' or rootdir =='2011':#(rootdir == '2009' or rootdir == '2010'):# or rootdir == '2011'):# or rootdir == '2012'):# or rootdir == '2010' or rootdir == '2011' or rootdir == '2012':
                        #        train_file.write(team_name + ',' + competitor + ',' + ','.join(stats) +  ',' + str(num_in_attendance) + ',' + str(outcome) + '\n')
                        
                        if rootdir_index in Constants.other_years:# or rootdir == '2011'):# or rootdir == '2012'):# or rootdir == '2010' or rootdir == '2011' or rootdir == '2012':
                                train_file.write(team_name + ',' + competitor + ',' + ','.join(stats) +  ',' + str(num_in_attendance) + ',' + str(outcome) + '\n')

                        if competitor not in outputted_teams_by_team_name:
                            outputted_teams_by_team_name[competitor] = []
    
                        outputted_teams_by_team_name[competitor].append(team_name)

train_file.close()
test_file.close()

import BracketGenerator