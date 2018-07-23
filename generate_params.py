import sys
import csv
import numpy as np
import itertools as it

def load_tile_list(fname):
    tile_list = []
    with open(fname, 'r', newline='') as csvfile:
        csv_r = csv.reader(csvfile, delimiter=' ')
        for row in csv_r:
            tile_list.append(row)
    return tile_list

def write_params(params, fname, prd_done=None):
    if prd_done is not None:
        prd_list = np.genfromtxt(prd_done, dtype='str')
    done_count = 0
    rest_count = 0
    with open(fname, 'w', newline='') as csvfile:
            csv_w = csv.writer(csvfile, delimiter=' ')
            for p in params:
                flat_list = []
                has_prd = False
                for sublist in p:
                    if isinstance(sublist, list):
                        for item in sublist:
                            flat_list.append(item)
                    else:
                        flat_list.append(sublist)
                if prd_done is not None:
                    prd_string = '_'+flat_list[1]+'_'+flat_list[2]+'_'+str(flat_list[0])+'0101'
                    for e in prd_list:
                        if prd_string in e:
                            done_count += 1
                            has_prd = True
                            break
                if has_prd is False:
                    csv_w.writerow(flat_list)
                    rest_count += 1

def main(argv):
    print(argv)
    year_list = np.arange(int(argv[0]), int(argv[1]), -1)
    print(year_list)
    tile_list = load_tile_list(argv[2])
    params = it.product(year_list, tile_list)
    if len(argv) < 5:
        write_params(list(params), argv[3])
    else:
        write_params(list(params), argv[3], argv[4])

if __name__ == '__main__':
    main(sys.argv[1:])

