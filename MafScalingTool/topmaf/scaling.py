'''----------PARSING DATA----------'''
def parse(fd):
    data = open(fd).readlines()
    for i in range(len(data)):
        data[i] = data[i].replace("\n","").split(",")
    for i in range(len(data)):
        data[i] = [x for x in data[i] if x!=""] 
    load = []
    rpm = []
    target = {} 
    #initialize load values
    for i in range(len(data[0])):
        #first value is a title
        if (i != 0):
            load.append(float(data[0][i]))
    data.remove(data[0])
    #initialize rpm values
    for i in range(len(data)):
        rpm.append(float(data[i][0]))
        data[i].remove(data[i][0])
    #fill target
    for i in range(len(data)):
        for j in range(len(data[i])):
            target[(load[j],rpm[i])] = float(data[i][j]) 
    return load,rpm,target
def parse_log(fd):
    #expected format:
    # MafSensorVoltage | Engine Speed | Engine Load | Wideband Reading
    data = open(fd).readlines()
    data.remove(data[0])
    for i in range(len(data)):
        data[i] = data[i].replace("\n","").split(",")
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return data
def parse_maf(fd):
    data = open(fd).readlines()
    for i in range(len(data)):
        data[i] = float(data[i])
    return data
'''----------END PARSING DATA----------'''
def lookup(num,lst):
    #input: num
    #matches num to closest val in lst
    #return list val
    difference = abs(lst[0] - num)
    index = 0
    tar_index = 0
    while(index < len(lst)):
        tmp_difference = abs(lst[index] - num)    
        if (difference == 0):
            return lst[index]
        elif (difference > tmp_difference):
            difference = tmp_difference
            tar_index = index
        index += 1
    return lst[tar_index]
def calc_match(load,rpm,target,mafv,
               data_mafv,data_rpm,
               data_load,data_afr):
    #action: - lookup corresponding target afr & mafv
    #        - calculate correction %
    #return: mafv,correction
    #lookups
    target_load = lookup(data_load,load)
    target_rpm = lookup(data_rpm, rpm)
    target_mafv = lookup(data_mafv, mafv)
    target_afr =  target[(target_load,target_rpm)]
    correction = ((data_afr - target_afr)/target_afr)*100
    
    print(f"Rpm: {target_rpm}, Load: {target_load}, AFR: {target_afr} Wideband: {data_afr} MAF_reading: {data_mafv}")

    return target_mafv,correction
def calc(load,rpm,target,mafv,log):
    #res = { mafv:->corr }
    res = {}

    for i in range(len(log)):
        data_mafv = log[i][0]
        data_rpm = log[i][1]
        data_load = log[i][2]
        data_afr = log[i][3]
        tmp = calc_match(load,rpm,target,mafv,
                         data_mafv,data_rpm,
                         data_load,data_afr)
        res[tmp[0]] = tmp[1]
    return res
    
def main():
    print(''' Please format your log file in the following way:         
    MafSensorVoltage | Engine Speed | Engine Load | Wideband Reading 
    Note: Any other columns of data can be deleted

    ''')
    #fd = input("Enter targetafr file: ")
    fd = "afr.csv"
    load,rpm,target = parse(fd)
    #fd = input("Enter log file: ")
    fd = "log.csv"
    log = parse_log(fd)
    #fd = input("Enter maf voltages file: ")
    fd = "maf.csv"
    mafv = parse_maf(fd)
    res = calc(load,rpm,target,mafv,log)
    print(res)
if __name__ == "__main__":
    main()
