
# import libraries
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from Bio import SeqIO # use it for .fastq

# line plot
x = np.arange(1, 101, 2) # 
y = np.arange(0, 100, 2) # 45 in total

plt.xticks(np.arange(0, 100, 5))
plt.yticks(np.arange(0, 100, 5))
plt.xlim(1, 101)
plt.ylim(1,101)
plt.plot(x, y)

plt.xlabel('Odd numbers')
plt.ylabel('Even numbers')
plt.title('Sample line plot')
plt.savefig('lineplot.png')

# fasta reads length distribution
# same task could be done with Jellyfish, FYI
def fastq_read_lentgh_distribution(fasta_file):
    read_lengths = [len(read) for read in SeqIO.parse(fasta_file, 'fasta')]
    plt.hist(read_lengths, edgecolor = 'blue')
    plt.title('%i sequences\nLengths %i to %i' % (len(read_lengths), min(read_lengths), max(read_lengths)))
    plt.xlabel('Read length, bp')
    plt.ylabel('Count')
    plt.savefig(fasta_file + '.png')

# checking code using DM chr6 full RNA(https://www.ncbi.nlm.nih.gov/assembly/GCF_000001215.4/)
# works just fine
fastq_read_lentgh_distribution('GCF_000001215.4_Release_6_plus_ISO1_MT_rna.fasta')


# best plots ever--3D surface plot with gradient
# I found this plot kinda cool(like PC games from 00's with this CGI)
# and gradient...smth hypnotyzing in that
# we need another module
from mpl_toolkits import mplot3d

# generate the Laplacian of Gaussian matrix(LoG)
def LoG(x, y, sigma):
    temp = (x ** 2 + y ** 2) / (2 * sigma ** 2)
    return -1 / (np.pi * sigma ** 4) * (1 - temp) * np.exp(-temp)


# some test data
N = 15
half_N = N // 2
X2, Y2 = np.meshgrid(range(N), range(N))
Z2 = -LoG(X2 - half_N, Y2 - half_N, sigma=4)
ax = plt.axes(projection='3d')
ax.plot_surface(X2, Y2, Z2, cmap='jet')
plt.title('3D surface plot is amazing!')
plt.savefig('3D_surface.png')

