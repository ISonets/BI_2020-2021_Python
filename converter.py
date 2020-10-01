#simple volume converter for buffer making
#added new unit: drop( useful for pharmacology ex tempore using
print('Hello!')
print('This program converts one volume unit into another unit, which is useful for proper buffer making')
print('Following are the available units: (nl), (mkl), (ml), (drop), (l)')
print('This converter uses functions. The syntax is: function(your number,unit to convert from, unit to convert to)')
def convert_func(val, unit_from, unit_to):
    SI = {'nl': 0.000000001, 'mkl':0.000001, 'ml':0.001, 'drop':0.00005, 'l':1.0}
    return round((val*SI[unit_from]/SI[unit_to]), 5)
