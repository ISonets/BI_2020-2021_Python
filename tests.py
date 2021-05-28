import pytest
from new_filtator import check_float, check_int, is_flag, gc_count, passed, flag_check, first_arg_check, second_arg_check


# 1. Parsing tests
@pytest.mark.parametrize("a, result", [(1, True),
                                       ('one', False),
                                       ([1], False),
                                       ({1, 1, 1}, False)])
def test_numbers_check(a, result):
    assert check_float(a) == result
    assert check_int(a) == result


def test_flag_check():
    with pytest.raises(ValueError):
        flag_check(["--output_bse_name", "0-o" "--min-length", "10", "--gc_bunds", "fifty", "--keep_filtered"])


# arg_check
@pytest.mark.parametrize("flag, input_list, result", [
    ('--min_length',
     ['--min_length', '15', '--gc_bounds', '40', '41', '--keep_filtered', '--output_base_name', 'new_name',
      'file.fastq'], True),
    ('--gc_bounds',
     ['--min_length', '15', '--gc_bounds', '40', '41', '--keep_filtered', '--output_base_name', 'new_name',
      'file.fastq'], True),
    ('--output_base_name',
     ['--min_length', '15', '--gc_bounds', '40', '41', '--keep_filtered', '--output_base_name', 'new_name',
      'file.fastq'], True),
])
def test_args(flag, input_list, result):
    assert first_arg_check(flag, input_list) == result


# arg check for GC bound(in case both are specified)
def test_exit_first_arg_check():
    with pytest.raises(SystemExit):
        first_arg_check('--min_length', ['--min_length', '--gc_bounds', '40', '41', '--keep_filtered',
                                             '--output_base_name', 'new_name', 'file.fastq'])
        first_arg_check('--gc_bounds',
                            ['--min_length', '8', '--gc_bounds', '--keep_filtered', '--output_base_name',
                             'new_name', 'file.fastq'])
        first_arg_check('--output_base_name',
                            ['--min_length', '8', '--gc_bounds', '40', '41', '--keep_filtered', '--output_base_name',
                             'file.fastq'])



@pytest.mark.parametrize("flag, input_list, result", [
    # different order
    ('--gc_bounds', ['--min_length', '40', '--keep_filtered', '--output_base_name', 'new_name', '--gc_bounds', '40', '50',
      'file.fastq'], True),
    ('--gc_bounds', ['--min_length', '40', '--keep_filtered', '--gc_bounds', '40', '50', '--output_base_name', 'new_name',
      'file.fastq'], True),
    ('--gc_bounds', ['--gc_bounds', '40', '50', '--min_length', '40',  '--keep_filtered', '--output_base_name', 'new_name',
      'file.fastq'], True),
    # without flag
    ('--gc_bounds', ['--min_length', '40', '--keep_filtered', '--output_base_name', 'new_name', '40',
      'file.fastq'], False),
    # without second value in different places
    ('--gc_bounds', ['--gc_bounds', '40', '--keep_filtered', '--gc_bounds', '40', '--output_base_name', 'new_name',
      'file.fastq'], False),
    ('---gc_bounds', ['--gc_bounds', '40', '--min_length', '40', '--keep_filtered', '--output_base_name', 'new_name',
      'file.fastq'], False),
    ('---gc_bounds', ['--gc_bounds', '--min_length', '40', '--keep_filtered', '--output_base_name', 'new_name',
      'file.fastq'], False),
])
def test_second_arg_check(flag, input_list, result):
    assert second_arg_check(flag, input_list) == result


# 2. Filtering part
@pytest.mark.parametrize("read, result_gc_count", [('AAAAAGGGGG', 50.0),
                                                   ('AAAAAA', 0.0),
                                                   ('CCCCGGG', 100.0),
                                                   ('GGGGGGGGG',100.0)])
def test_gc_count(read, result_gc_count):
    assert gc_count(read) == result_gc_count


@pytest.mark.parametrize(
    "read, min_length, left_gc_bound, right_gc_bound, input_list, result",
    [('AAAAAGGGGG', 5, 40.0, 45.0, ["--min_length", "--gc_bounds"], False),
     ('AAAAAGGGGG', 5, 60.0, 75.0, ["--min_length", "--gc_bounds"], False),
     ('AAAAAGGGGG', 5, 40.0, 55.0, ["--min_length", "--gc_bounds"], True),
     ('AAAAAGGGGG', 11, 40.0, 45.0, ["--min_length", "--gc_bounds"], False),
     ('AAAAAGGGGG', 1, 40, 45, ["--min_length", "--gc_bounds"], False),
     ])
def test_passed(read, min_length, left_gc_bound, right_gc_bound, input_list, result):
    assert passed(read, min_length, left_gc_bound, right_gc_bound,
                  input_list) == result
