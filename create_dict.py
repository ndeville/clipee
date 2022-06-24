from pandas.io.clipboard import clipboard_get
import subprocess
from datetime import date, datetime
import pprint
pp = pprint.PrettyPrinter(indent=4)

d = datetime.now()

date = d.strftime('%Y%m%d-%H%M%S')


def write_to_clipboard(output):
    process = subprocess.Popen(
        'pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


text = clipboard_get()


print()

dict_output = {}

data = text.split('\r\n')
for item in data:
  x = item.split('\t')
  dict_output[x[0]] = int(x[1])

print()
pp.pprint(dict_output)
print()

###


