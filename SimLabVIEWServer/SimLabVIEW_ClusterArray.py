class flatten:
    '''
    Assign the pattern of list, then unflatten binary string to list.
    Equals to the function fo Unflatten to String in LabVIEW.
    Data type definition:
    
    'sa' = string array,
    's' = string,
    '2ub' = 2bytes unsigned,
    '''

    def stringtobytes(self, string):
        # string to bytes. first 4bytes = string length; rest bytes = string in ascii
        len_str = len(string).to_bytes(4, byteorder='big')
        return len_str + bytes(string, encoding='ascii')

    def str_ary_tobytes(self, arystring):
        # string array to bytes. first 4bytes = array length; followed by string format
        len_strary = len(arystring).to_bytes(4, byteorder='big')
        result_bstring = len_strary
        for i in arystring:
            result_bstring += self.stringtobytes(i)
        return result_bstring

    def clustertobytes(self, cluster, place_order, concate=False):
        '''input cluster and return it with bytes. Cluster is the summation of all data.
        EX=>
        original: string + string + number + array
        bytes   : b'len(string) + b'string' + ....

        place_order: 's', 'sa', '2b'
        '''
        result_bstring = b''
        for index, value in enumerate(cluster):
            elem = place_order[index]
            if elem=='s':
                result_bstring += self.stringtobytes(value)

            elif elem=='sa':
                result_bstring += self.str_ary_tobytes(value)

            elif elem=='2ub':
                result_bstring += value.to_bytes(2, byteorder='big')

            elif elem=='2b':
                result_bstring += value.to_bytes(2, byteorder='big', signed=True)

            elif elem=='4b':
                result_bstring += value.to_bytes(4, byteorder='big', signed=True)

            elif elem=='1ub':
                result_bstring += value.to_bytes(1, byteorder='big')

        if concate == True:
            result_bstring = len(result_bstring).to_bytes(4, byteorder='big')+ result_bstring
            # concatenate length of binary string in front
        return result_bstring




class unflatten:
    '''
    Assign the pattern of list, then unflatten binary string to list.
    Equals to the function fo Unflatten to String in LabVIEW.
    
    Data type definition:
    'c' = cluster array(must be define in the first element),
    'sa' = string array,
    's' = string,
    '4b' = 4bytes signed,
    '2b' = 2bytes signed,
    '1ub' = 1byte unsigned
    '''

    def __init__(self, bytes_string, place_order):
        self.obs = bytes_string     # original bytes string (b'\x_ _\x_ _\x_ _...') which is saved
        self.bs = bytes_string      # original bytes string which is going to edited
        self.pr = place_order       # define the data type in i_th element in list

    def obs(self):
        return self.obs

    def bs(self):
        return self.bs

    def pr(self):
        return self.pr

    def bytes_decnum(self, bytes_num=4, signed=False):  # translate bytes in to decimal number
        len_string = int.from_bytes(self.bs[0:bytes_num], byteorder='big', signed=signed)
        self.bs = self.bs[bytes_num:]       # erase the first 4 bytes in self.bs
        return  len_string


    def unflatten_string(self):                         # unflatten string
        len_string = self.bytes_decnum()
        temp = self.bs[:len_string]
        string = temp.decode('ascii')
        self.bs = self.bs[len_string:]      # erase the string in self.bs
        return string

    def unflatten_stringarray(self):
        len_array = self.bytes_decnum()
        output_array = []
        for _ in range(len_array):
            temp = self.unflatten_string()
            output_array.append(temp)
        return output_array

    def unflatten(self):
        output_list = []
        if self.pr[0] == 'c':
            cycle = self.bytes_decnum()
        else:
            cycle = 1
        for _ in range(cycle):
            sub_list = []
            for datatype in self.pr:
                if datatype=='s':
                    string = self.unflatten_string()
                    sub_list.append(string)

                elif datatype=='sa':
                    array = self.unflatten_stringarray()
                    sub_list.append(array)

                elif datatype=='4b':
                    four_snum = self.bytes_decnum(4, True)
                    sub_list.append(four_snum)

                elif datatype=='2b':
                    two_snum = self.bytes_decnum(2, True)
                    sub_list.append(two_snum)

                elif datatype=='1ub':
                    one_snum = self.bytes_decnum(1, False)
                    sub_list.append(one_snum)

            output_list.append(sub_list)

        return output_list
    
# if __name__ == '__main__':
#     place_order = ['s', 's', '2ub', 's']
#     cluster = ['', '', 5, 'F0']
#     ttt = flatten()
#     ttr = ttt.clustertobytes(cluster, place_order, concate=True)
#     print(ttr)