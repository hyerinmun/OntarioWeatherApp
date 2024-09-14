import csv

with open('on_stn_codes.csv') as stn:
    reader = csv.reader(stn)
    my_list = list(reader)

print("csv to list item 1:", my_list[0])
my_list[0] = ['CYAM']
print("csv to list item 1:", my_list[0])
print("csv to list:", my_list)
list2 = str(my_list).replace("[",'').replace("'",'').replace("]",'')
print("csv to list:", list2)
print(list2[0])

list3 = [i[0] for i in my_list]
print(list3)
print(list3[0])

# for l in list3:
#     if len(l) == 3:
#         print(l)
#         l = " " + l
#         print(l)

list4 = [" " + i for i in list3 if len(i) == 3]
list5 = [i for i in list3 if len(i) == 4]    

list4.extend(list5)
print(list4)

count = 0

header = ['STN', 'DATE','HR', 'TEMP']

with open("SCRIBE.NWCSTG.05.08.14Z.txt", "r") as file, open("current_weather.csv", "w", encoding='UTF8', newline='') as new_file:  
    
    writer = csv.writer(new_file)
    writer.writerow(header)
    
    for line in file:

        try:
            if line[5:9] in list4:
                count += 1
                print(f'Line {count}: STN {line[5:9]}', end='')
                print("")
                for x in range(26):
                    next(file)

                current = file.readline()
                print(f'Date: {current[0:8]}')
                print(f'Hour: {current[9:13]}')    
                print(f'Temp: {current[65:70]}')
                
                writer.writerow([line[5:9], current[0:8], current[9:13], current[65:70].replace(" ", "")])
                
                #print(f'temp: {file.readline[5:9]}', end='')
                
        
        except IndexError:
            for x in range(30):
                next(file)
    
    
        # count += 1
        # print(f'line {count}: {line[5:9]}', end='')
        # print("")
        # for x in range(29):
        #     next(file)
        #     #print(file.readline())