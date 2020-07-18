import datetime

#DEBUGGING
import os
import psutil
import time


#2d-array v kerga shranmo podatke v obliki [ [matchId0, line], [matchId1, line], [matchId1, line], ...]
def data_to_array(file):
    data_array = []

    f = open(file, "r+")
    next(f)
    for line in f:
        first_part = line.split("|")[0]
        match_id_str = first_part.split(":")[2]
        match_id = int(match_id_str[:-1])
        data_array.append([match_id, line])
    f.close()

    sorted_array = sorted(data_array,key=lambda x: x[0])
    #sortedArray = data_array[data_array[:, 0].argsort()]
    return sorted_array

#2d-array zapisemo v txt
def array_to_data(array, file):
    f = open(file, "w+")
    f.write("MATCH_ID|MARKET_ID|OUTCOME_ID|SPECIFIERS\n")
    for i in array:
        f.write(i[1])
    f.close()

def merge_data(input, database, file):
    f = open(file, "w+")
    f.write("MATCH_ID|MARKET_ID|OUTCOME_ID|SPECIFIERS\n")

    #merge sort
    input_len = len(input)
    index_input = 0
    database_len = len(database)
    index_database = 0

    curr_input = input[index_input]
    curr_database = input[index_database]
    while(index_input < input_len-1 and index_database < database_len-1):
        if curr_input[0] < curr_database[0]:
            f.write(curr_input[1])
            index_input += 1
            curr_input = input[index_input]
        else:
            f.write(curr_database[1])
            index_database += 1
            curr_database = database[index_database]

    #zapišemo še preostanek tistega ki je ostalo
    while index_input < input_len-1:
        f.write(curr_input[1])  # + "|" + str(datetime.timedelta(seconds=666))
        index_input += 1
        curr_input = input[index_input]
    while index_database < database_len-1:
        f.write(curr_database[1])   #  + "|" +  str(datetime.timedelta(seconds=666)))
        index_database += 1
        curr_database = database[index_database]

    f.close()

def split_file(num_of_files, file):
    num_of_lines = len(open(file).readlines(  ))
    #naredimo prvi splitam file
    new_file_name = "fo_split" + str(0) + ".txt"
    f_split_file = open(new_file_name, "w+")
    f_split_file.write("MATCH_ID|MARKET_ID|OUTCOME_ID|SPECIFIERS\n")
    split_file_index = 0

    #odpremo original
    f_original = open(file, "r+")
    next(f_original)

    #razbijemo na fajle
    index = 1
    for line in f_original:
        if index%(int(num_of_lines/num_of_files)) == 0:
            f_split_file.close()
            split_file_index +=1
            new_file_name = "fo_split" + str(split_file_index) + ".txt"
            f_split_file = open(new_file_name, "w+")
            f_split_file.write("MATCH_ID|MARKET_ID|OUTCOME_ID|SPECIFIERS\n")
        f_split_file.write(line)
        index+=1



## MAIN
if __name__ == "__main__":

    #na začetku spraznimo bazo
    f = open("database.txt", "w+")
    f.write("MATCH_ID|MARKET_ID|OUTCOME_ID|SPECIFIERS\n")
    f.close()


    file = "hec"
    while(file != "stop"):
        print("Vpišite file z podatki ki ga zelite vnesti; če ne boste več vnašali podatkov napišite 'stop'")
        file = input()
        if file == "stop":
            break;

        start = time.time()
        data_base_array = data_to_array("database.txt")
        input_data_array = data_to_array(file)
        merged_data = merge_data(input_data_array, data_base_array, "database.txt")
        print("Vstavljanje je trajalo:" + str(time.time()-start) + " sekund.\n")



    #debugging
    #process = psutil.Process(os.getpid())
    #print("Porabljenih je:", process.memory_info()[0]/(1024*1024), " MB rama")



    #split_file(5, "fo.txt")