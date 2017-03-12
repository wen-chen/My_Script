def fafile_2_seq_dict(FileName):
    name_list = list()
    sequence_list = list()
    i = -1
    with open(FileName, "r") as infile:
        for line in infile:
            line = line.strip()
            if line[0] == '>':
                name = line[1:]
                name_list.append(name)
                sequence_list.append(list())
                i = i + 1
            else:
                line = line.upper()
                sequence_list[i].append(line)
    sequence_dict = dict()
    for i in range(len(name_list)):
        sequence_dict[name_list[i]] = ''.join(sequence_list[i])
    return sequence_dict
    