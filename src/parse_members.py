import pandas
import regex
# TODO:
# parse excel members
# parse txt switch output
# parse txt exceptions

# create new excel table
# combine with room number being common key
# add column member/nonmember/exception (optional: color it)

# add proper readme.md
# generate and add pip_reqs.txt via pip list
# make templates for the input files in a /templates folder
# add filenames as script arguments

# Stretch goal: get by cmd and pipe switch output to file, then parse
# Stretch goal: make script to disable inactive member interfaces
# MEGA Stretch goal: parse bank transfer info to generate valid members list

# NOTE: make values a tuple aka appendable

def main():
    print("uhh")
    print("parsing members excel")

    mymembers = pandas.read_excel('userdata/Vereinsmitgliede_Stand_7_10_24.xlsx', usecols="B:C")

    mymembersdict = mymembers.set_index('Room')['Name'].to_dict()
    print("uhh parsed")

    print("parsing switch output")
    switch_output_dict = {}

    invalid_pattern = regex.compile("Gi[3-5]") # TODO: rename, this is the valid pattern

    with open("userdata/switch_interfaces_status-20241012.txt", 'r') as f:
        for line in f:
            items = line.split()
            if (len(items) != 7 or not(invalid_pattern.match(items[0]))): # may be redundant
                continue # skip invalid lines
                # TODO: clean up regex
            elif (items[1] == "frei"):
                key, values = items[1], [items[0]] # NOTE: make values a tuple aka appendable
                # "frei" special case TODO: handle better, maybe room nr shoulda stayed strings
            else:
                key, values = int(regex.sub(r'z0*', '', items[1])), [items[0]]
                if (key in mymembersdict):
                    values.append("member")
                # key is room nr - 2nd col
                # value is interface port - 1st col
            switch_output_dict[key] = values

    print("parsing exceptions")
    special_members_dict = {}

    # TODO: repeated code below MOSTLY, maybe take out into function
    with open("userdata/exceptions.txt", 'r') as f:
        for line in f:
            items = line.split()
            if (len(items) != 7 or not(invalid_pattern.match(items[0]))): # may be redundant
                continue # skip invalid lines
                # TODO: clean up regex
            elif (items[1] == "frei"):
                key, values = items[1], [items[0], "special"] # NOTE: make values a tuple aka appendable
                # "frei" special case TODO: handle better, maybe room nr shoulda stayed strings
            else:
                key, values = int(regex.sub(r'z0*', '', items[1])), [items[0], "special"]
                # key is room nr - 2nd col
                # value is interface port - 1st col
            special_members_dict[key] = values

    # combine all dicts
    # TODO: change to list expression instead of loop
    # TODO: there are some pretty bad looking nested tuples as a result here
        # operator += fixes this for the specials
        # for the members dict it appends char by char which is wrong, so find a consistent way
    print("combining all three") # inefficiently
    for key in switch_output_dict:
        if key in mymembersdict:
            switch_output_dict[key].append(mymembersdict[key])
        if key in special_members_dict:
            switch_output_dict[key]+=special_members_dict[key]
        # print(key,"-->",switch_output_dict[key]) # DEBUG PRINT FINAL

    # map combined dict to excel
    # TODO: CLEAN UP THESE COLUMNS, THEY'RE INCONSISTENT
    switch_output_df = pandas.DataFrame.from_dict(switch_output_dict, orient='index') #, columns=["room nr", "interface", "member status", "name"])
    switch_output_df.to_excel("userdata/combined.xlsx")

if __name__ == "__main__":
    main()