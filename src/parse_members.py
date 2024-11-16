import pandas
import openpyxl
# TODO:
# parse excel members
# parse txt switch output
# parse txt exceptions

# create new excel table
# combine with room number being common key
# add column member/nonmember/exception (optional: color it)

# generate and add pip_reqs.txt via pip list

# Stretch goal: get by cmd and pipe switch output to file, then parse
# Stretch goal: make script to disable inactive member interfaces
# MEGA Stretch goal: parse bank transfer info to generate valid members list

def main():
    print("uhh")
    print("parsing members excel")
    # df = pandas.DataFrame([[1, 2, 3], [4, 5, 6]], columns=['A', 'B', 'C'])
    # df.to_excel('userdata/experimental.xlsx')
    file = pandas.ExcelFile('userdata/Vereinsmitgliede_Stand_7_10_24.xlsx')
    mymembers = file.parse()
    # print(df)
    print("uhh parsed")
    print(mymembers)

    print("parsing switch output")
    switch_output = {}

    with open("userdata/switch_interfaces_status-20241012.txt", 'r') as f:
        for line in f:
            items = line.split()
            if (len(items) < 7):
                continue # skip invalid lines
            key, values = items[1], items[2:] # key is room nr - 2nd col
            switch_output[key] = values


    print(switch_output['z0101'])

    print("parsing exceptions")
    special_members = {}

    with open("userdata/exceptions.txt", 'r') as f:
        for line in f:
            items = line.split()
            if (len(items) < 7):
                continue # skip invalid lines
            key, values = items[1], items[2:] # key is room nr - 2nd col
            special_members[key] = values


    print(special_members['z1101'])

if __name__ == "__main__":
    main()