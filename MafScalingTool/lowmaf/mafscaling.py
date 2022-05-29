#Opens the target file and converts the text file into a list of each line in the file
#Each line in the list will follow this format for the values:
#[time(ms),Feedback Knock Correction (Degrees),A/F Correction #1(%), A/F Learning #1(%), CL/OL Fueling, Intake Air Temperature (C), Mass Airflow Sensor (V)]
#Abbreviated:
'''[T , FKC , STFT, LTFT, CL/OL, IAT, MAF, DmafDt, Corr]'''
''' 0   1     2     3     4      5    6    7       8    '''
def formatInputFile():
    file = open("inputfile.csv")
    file = file.readlines()
    for i in range(len(file)):
        file[i] = file[i].replace("\n","").split(",")
        for j in range(len(file[i])):
            try:
                file[i][j] = float(file[i][j])
            except Exception:
                print(f"row:{i} column {j}")
                return
    return file
    

#automates the process of maf scaling in these steps:
#list of lists "data" stores all of the raw data
'''
    1) creates a new column: dmaf/dt
    2) removes all values with dmaf/dt >.3
    3) removes all values with CL/OL = 10
    4) returns a range and a mean of IAT values and allows the user to choose a threshold for deletion
    5) creates a new column: overall correction (STFT + LTFT)
    6) matches up the data with cooresponding MAF values found in ecu flash
    7) determines the mean,median,mode,1st quartile and 3rd quartile values for each MAF value 
    8) gives a reccomended % increase or decrease for each MAF value

'''
def automate(data):
    ''' Step 1 : dmaf/dt '''
    
    index = 1
    while index < len(data):
        time1 = data[index-1][0]
        time2 = data[index][0]
        maf1 = data[index-1][6]
        maf2 = data[index][6]

        dmafDt = ((1000)*(maf2-maf1))/(time2-time1)
        data[index].append(dmafDt)

        index += 1
    
    '''Step 2: >.3 removal'''
    
    preMafLength = len(data)
    del data[0]
    for i in range(len(data)): 
        try:
            if (data[i][7] > .3):
                del data[i]
        except IndexError:
            break
    postMafLength = len(data)
    print((preMafLength-postMafLength), "/" , preMafLength, "of the maf values were too large")
    
    ''' Step 3: remove OL values'''    
    
    preOLLength = len(data)
    for i in range(len(data)): 
        try:
            if (data[i][4] == 10):
                del data[i]
        except IndexError:
            break
    CLLength = len(data)
    print((preOLLength-CLLength), "/" , preOLLength, "of the values were in OL")

    ''' Step 4: IAT spikes removal '''
    #TODO: Currently only removes values >= 40
    preIATLength = len(data)
    for i in range(len(data)): 
        try:
            if (data[i][5] >= 40):
                del data[i]
        except IndexError:
            break
    IATLength = len(data)
    print((preIATLength-IATLength), "/" , preIATLength, "of the IAT values were too big")

    '''Step 5: overall Correction'''
    for i in range(len(data)):
        data[i].append(data[i][2] + data[i][3])

    '''Step 6 "Cheat Sheet" '''
    #TODO CheatSheet only goes from 0.00 - 3.12 currently
    
    CheatSheet = [
                    [0.00],
                    [0.94],
                    [0.98],
                    [1.02],
                    [1.05],
                    [1.09],
                    [1.13],
                    [1.17],
                    [1.21],
                    [1.25],
                    [1.29],
                    [1.33],
                    [1.37],
                    [1.41],
                    [1.48],
                    [1.56],
                    [1.64],
                    [1.72],
                    [1.80],
                    [1.87],
                    [1.95],
                    [2.03],
                    [2.11],
                    [2.19],
                    [2.27],
                    [2.34],
                    [2.42],
                    [2.54],
                    [2.66],
                    [2.77],
                    [2.89],
                    [3.01],
                    [3.12]
                 ]
    
    ''' Step 7 : find statistics for corrections for each value in cheat sheet'''
    #TODO: Currently only finds the mean and num of values
    i = 1
    while (i < (len(CheatSheet)-1)):
        sum = 0
        count = 0
        
        lower = ((CheatSheet[i][0] - CheatSheet[i-1][0])/2)+ CheatSheet[i-1][0]
        upper = ((CheatSheet[i+1][0] - CheatSheet[i][0])/2)+ CheatSheet[i][0]
        
        for j in range(len(data)):
            corr = data[j][8]
            mafv = data[j][6]

            if (mafv >= lower and mafv <= upper):
                sum += corr
                count += 1
        try:
            CheatSheet[i].append(sum/count)
        except:
            CheatSheet[i].append(0)
        CheatSheet[i].append(count)
        print ("MafV:", CheatSheet[i][0], "Mean:", CheatSheet[i][1], "Count:", CheatSheet[i][2]) 
        i += 1

    ''' Step 8: Give reccomended adjustments '''
    #TODO

    


if __name__ == "__main__":
    data = formatInputFile()
    automate(data)
