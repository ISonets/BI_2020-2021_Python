# simple volume converter for buffer making
# new_version
print('Hello!')
print('This program converts one volume unit into another.')
print('It is useful for proper buffer making')
print('Following are the available units: (nl), (mkl), (ml), (l)')
print('This converter uses functions')
print('The syntax is: function(your number,unit to convert from, unit to convert to)'
def convert_func(val, unit_from, unit_to):
    SI = {'nl': 0.000000001, 'mkl': 0.000001, 'ml': 0.001, 'l': 1.0,}
    return round((val * SI[unit_from] / SI[unit_to]), 5)
