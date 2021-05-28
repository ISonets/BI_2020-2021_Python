import sys

# ANNA PART

input_list = sys.argv[1:]


def check_float(float_number):
    try:
        float(float_number)
        return True
    except TypeError:
        print('TypeError')
        return False
    except ValueError:
        print('ValueError')
        return False
    except NameError:
        print('NameError')
        return False


def check_int(int_number):
    try:
        int(int_number)
        return True
    except TypeError:
        print('TypeError')
        return False
    except ValueError:
        print('ValueError')
        return False
    except NameError:
        print('NameError')
        return False


def is_flag(x):
    if "--" in x and iter(x):
        return True
    else:
        return False


def flag_check(args_input_list):
    avail_flags = ["--output_base_name", "--min_length", "--gc_bounds", "--keep_filtered"]
    for i in args_input_list:
        if is_flag(i):
            if not any(i in s for s in avail_flags):
                raise ValueError(f'Flag is not recognized: [{i}] \n'
                                 f'Available flags: \n'
                                 f'\t --output_base_name \n'
                                 f'\t --min_length \n'
                                 f'\t --gc_bounds \n'
                                 f'\t --keep_filtered \n')

        else:
            continue

def first_arg_check(flag, args_input_list):    
    try:
        y = args_input_list.index(flag) + 1
        if flag in args_input_list:
            if (is_flag(args_input_list[y])) or (y == last_ind_in_input_list):
                raise SystemExit(f"You forgot to specify arg after flag [{flag}]!")
            else:
                return True
    except ValueError:
        return False

def second_arg_check(flag, args_input_list):
    last_ind_in_input_list = len(args_input_list) - 1
    try:
        x = flag
        y = args_input_list.index(x) + 2
        if x in args_input_list:
            if (is_flag(args_input_list[y])) or (y == last_ind_in_input_list):
                return False
            else:
                return True

    except ValueError:
        return False

def IS_FASTQ(file_format, args_input_list):
    last_ind_in_input_list = len(args_input_list) - 1
    if file_format in str(args_input_list[last_ind_in_input_list]):
        return sys.path[0], str(sys.argv[len(sys.argv) - 1]), sys.path[0] + "/" + str(sys.argv[len(sys.argv) - 1])
    else:
        raise TypeError("Last argument should be .fastq file")

if (is_flag(input_list[0]) == False) and (".fastq" not in str(input_list[0])):
    sys.exit(
        "You should specify at least 1 option and file name to start filtering!")

def OUTPUT_BASE_NAME(flag, args_input_list):
    last_ind_in_input_list = len(args_input_list) - 1
    if 1st_arg_check(flag, args_input_list):
        res = args_input_list[args_input_list.index(flag) + 1]
        return str(res)
    else:
        return args_input_list[last_ind_in_input_list].split('.')[0]


def MIN_LENGTH(flag, args_input_list):
    last_ind_in_input_list = len(args_input_list) - 1
    if 1st_arg_check(flag, args_input_list):
        res = args_input_list[args_input_list.index(flag) + 1]
        if check_float(res):
            if check_int(res):
                if int(res) < 0:
                    raise ValueError(f'Min length res can`t be negative: [{res}]')
                else:
                    return int(res)
            else:
                raise ValueError(f'Min length res must be integer number only (int): [{res}]')

        else:
            raise TypeError(f'Min length res must be non-negative real integer number only (int): [{res}]')
    else:
        return 0

def LEFT_GC_BOUND(flag, args_input_list):
    last_ind_in_input_list = len(args_input_list) - 1
    if 1st_arg_check(flag, args_input_list):
        res = args_input_list[args_input_list.index(flag) + 1]
        if check_float(res):
            if float(res) > 0:
                return float(res)
            else:
                raise ValueError(f'Lower GC bound res must be > 0: [{res}] '
                		f'\n Remember to use a ".", not "," for numbers')
        else:
            raise TypeError(f'Lower GC bound must be real number only (int or float): [{res}]')
    else:
        return 0.0


def RIGHT_GC_BOUND(flag, args_input_list):
    last_ind_in_input_list = len(args_input_list) - 1
    if second_arg_check(flag, args_input_list):
        res = args_input_list[args_input_list.index(flag) + 2]
        if check_float(res):
            if float(res) > 0:
                return float(res)
            else:
                raise ValueError(f'Upper GC bound must be > 0: [{res}]. '
                                 f'\n Remember to use use a ".", not "," for numbers')
        else:
            raise TypeError(f'Upper GC bound must be real number only (int or float): [{res}]')
    else:
        return 100.0


def GC_BOUND_GOOD(left_gc_bound, right_gc_bound):
    if left_gc_bound >= right_gc_bound:
        raise ValueError(f'Left GC bound must be < than upper GC bound. [{left_gc_bound} >= {right_gc_bound}]')


def OUTPUT_NEEDED(flag, args_input_list):
    if flag in args_input_list:
        return True
    else:
        return False

flag_check(input_list)

path_to_dir_with_files, input_fastq_file_name, path_to_input_fastq_file = IS_FASTQ(".fastq", input_list)

new_name = OUT_PUT_BASE_NAME("--output_base_name", input_list)

min_length = MIN_LENGTH("--min_length", input_list)

gc_bound_good(LEFT_GC_BOUND("--gc_bounds", input_list),
                  RIGHT_GC_BOUND("--gc_bounds", input_list))
left_gc_bound = LEFT_GC_BOUND("--gc_bounds", input_list)

right_gc_bound = RIGHT_GC_BOUND("--gc_bounds", input_list)

output_permission = OUTPUT_NEEDED("--keep_filtered", input_list)


# IGNAT PART

# GC count caculation
def gc_count(read):
    count = 0
    for base in read:
        if base == 'C' or base == 'G':
            count += 1
    return count * 100 / len(read)


# ez
# check for good reads
def passed(read, min_length, left_gc_bound, right_gc_bound, input_list):
    if "--min_length" in input_list:
        if len(read) > min_length:
            l = True
        else:
            l = False

    if "--gc_bounds" in input_list:
        if left_gc_bound < gc_count(read) < right_gc_bound:
            b = True
        else:
            b = False
    return b and l


# ez
# save in file
def file_output(readlines, file):
    file.write('\n'.join(readlines) + '\n')


# ez af
# open file
fastq_input = open(input_fastq_file_name, 'r')
# read all input lines
all_reads = fastq_input.read().splitlines()
# N of reads in file
total_reads = str(len(all_reads) // 4)
# create output blank file and creating failed .fastq if necessary
fastq_passed = open(new_name + '_passed.fastq', 'w')
if output_permission == True:
    fastq_failed = open(new_name + '_failed.fastq', 'w')

# counter for passed/failed reads and their filtration
reads_passed = 0
reads_failed = 0
for i in range(0, len(all_reads), 4):  # we need to read lines by 4, e.g. 1-4, 5-8, 9-12 etc.
    current_read = all_reads[i:i + 4]  # reading 2nd line where ATGC's are
    if i == 0:  # check if empty
        print()
    if passed(current_read[1], min_length, left_gc_bound, right_gc_bound, input_list):
        file_output(current_read, fastq_passed)
        reads_passed += 1
    else:
        if error_output_permission == True:
            file_output(current_read, fastq_failed)
        reads_failed += 1

# don't forget to close file
print('Done!')
print('Total reads number is ' + input_fastq_file_name + ': ' + total_reads)
print(str(reads_passed) + ' (' + str(round(reads_passed * 100 / int(total_reads), 2)) + '%) reads passed filtering.')
print(str(reads_failed) + ' (' + str(round(reads_failed * 100 / int(total_reads), 2)) + '%) reads failed filtering.')

fastq_passed.close()
fastq_input.close()
if error_output_permission == True:
    fastq_failed.close()
