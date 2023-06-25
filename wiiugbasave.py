# This converts data_008_0000.bin from GBA VC on Wii U to a .sav file
import sys, tkinter
from tkinter import filedialog

# Get the input path
if not len(sys.argv) > 1:
    root = tkinter.Tk()
    root.withdraw()
    path = filedialog.askopenfilename()
else:
    path = sys.argv[1]

# Open the files
inputf = open(path, 'rb')
output = open(path + '.sav', 'xb')

# Write output to file
output.write(inputf.read()[int('4080', 16):])

# Close files
inputf.close()
output.close()

# Get filename
if path.count('/') != 0:
    filename = path.split('/')[-1]
else:
    filename = path.split('\\')[-1] # thanks windows

print('Converted successfully!')
print('Saved to ' + filename + '.sav')
