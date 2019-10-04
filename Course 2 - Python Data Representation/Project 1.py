'''
Project: File differences
'''

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    line1 = line1.strip('\n')
    line2 = line2.strip('\n')
    
    len_line1 = len(line1)
    len_line2 = len(line2)
    
    if len_line1 == len_line2:
        if line1.split() == line2.split():
            return IDENTICAL
        else:
            for index_break, (c_line1, c_line2) in enumerate(zip(line1, line2)):
                if c_line1 == c_line2:
                    pass
                else:
                    # index at which the two lines (strings) are not equal
                    index = index_break
                    # break the loop as we just need the first index at which it is not equal
                    break
            return index
        
    elif len_line1 != len_line2:
        min_len = min(len_line1, len_line2)
        
        u_str_line1 = line1[:min_len]
        u_str_line2 = line2[:min_len]
        
        if u_str_line1 == u_str_line2:
            return min_len
        else:
            for index_break, (c_u_line1, c_u_line2) in enumerate(zip(u_str_line1, u_str_line2)):
                if c_u_line1 == c_u_line2:
                    pass
                else:
                    index = index_break
                    break
            return index
    
    else:
        pass
    
def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    index = singleline_diff(line1, line2)
    line1_n = line1+'\n'
    line2_n = line2+'\n'
    
    if idx == 0:
        str_carrot = '^'+'\n'
        format_str = line1_n + str_carrot + line2_n
        return format_str
    elif len(line1) == len(line2):
        if (idx == -1) or (('\n' or '\r') in (line1, line2)):
            return ''
        # Don't check if the index passed is valid or not
        else:
            line2_copy = line2
            line2_substr = line2_copy[:idx]
            line2_replace_eq = line2_copy.replace(line2_substr, '='*len(line2_substr))
            line2_replace_ueq = line2_replace_eq.replace(line2_replace_eq[idx], '^', 1)
            line2_matched_str = line2_replace_ueq[:(line2_replace_ueq.index('^'))+1]
            format_str = line1_n + line2_matched_str+'\n' + line2_n
            return format_str
    elif len(line1) != len(line2):
        if (('\n' or '\r') in (line1, line2)):
            return ''
        elif len(line1) < len(line2):
            if (idx > len(line1)) and (idx != index):
                return ''
            else:
                line2_copy = line2
                line2_substr = line2_copy[:idx]
                line2_replace_eq = line2_copy.replace(line2_substr, '='*len(line2_substr))
                line2_replace_ueq = line2_replace_eq.replace(line2_replace_eq[idx], '^', 1)
                line2_matched_str = line2_replace_ueq[:(line2_replace_ueq.index('^'))+1]
                format_str = line1_n + line2_matched_str+'\n' + line2_n
                return format_str
        elif len(line2) < len(line1):
            if (idx > len(line2)) and (idx != index):
                return ''
            # The following else condition also works if (idx != index)
            else:
                line1_copy = line1
                line1_substr = line1_copy[:idx]
                line1_replace_eq = line1_copy.replace(line1_substr, '='*len(line1_substr))
                line1_replace_ueq = line1_replace_eq.replace(line1_replace_eq[idx], '^', 1)
                line1_matched_str = line1_replace_ueq[:(line1_replace_ueq.index('^'))+1]
                format_str = line1_n + line1_matched_str+'\n' + line2_n
                return format_str

def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    if lines1 == lines2:
        return (IDENTICAL, IDENTICAL)
    elif len(lines1) != len(lines2):
        return (max(len(lines1),len(lines2))-1,0)
    else:
        for line_index, (line1, line2) in enumerate(zip(lines1, lines2)):
            idx = singleline_diff(line1, line2)
            if idx != -1:
                break
            else:
                pass
        return (line_index, idx)

def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lines_list = []
    file_handle = open(filename, 'r')
    file_content = file_handle.readlines()
    for lines in file_content:
        lines_list.append(lines.strip())
    return lines_list

def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file1_lines = get_file_lines(filename1)
    file2_lines = get_file_lines(filename2)
    
    if file1_lines == file2_lines:
        return 'No differences\n'
    else:
        for index_l, (line1, line2) in enumerate(zip(file1_lines, file2_lines)):
            l_num = multiline_diff(file1_lines, file2_lines)[0]
            diff_index = multiline_diff(file1_lines, file2_lines)[1]
            str_diff = singleline_diff_format(file1_lines[l_num], file2_lines[l_num], diff_index)
            formatted_str = 'Line '+str(l_num)+':\n'+str_diff
        return formatted_str
    

