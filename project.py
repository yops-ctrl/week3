"""
Author: Giannis Spyropoulos, S5657237, University of Groningen, The Netherlands
Email: i.spyropoulos.1@student.rug.nl
Usage: project.py, whales_all.str, numpy, pandas
Description: This program's task is to go in the file 'whales_all.str' and find the parent-offspring pairs in the data
looking for at least one common allele per locus (either paternal or maternal origin).
Still needs work. I didn't manage to figure out how to efficiently double the headers, so that each allele would have
the name of the locus and put the result in the output file. That means that when I feed the output file into the
function that finds parent-offspring pairs that takes into account the >= 50% similarity score per locus, it gives back
the parent-offspring pairs as well as the duplicates. I am leaving the code that is not properly working however,
because I will need to revise it for my project and get it working in the future.

"""


# First Step: Remove Duplicates


import numpy as np
import pandas as pd

# Create an intermediate file to put the data with the desired format in (locus name will be repeated so each allele
# has the locus name on the same column.
modified = 'whales_all_modified.str'

# Read the data from the 'whales_all.str' file
whales = 'whales_all.str'


with open(whales, 'r') as file:
    lines = file.readlines()

# Creating a list with an empty line in it so that it separates the locus names and the samples (join() cannot take str)
empty = ['\n']

# Modifying the header so that it repeats the loci names twice.
first_line = lines[0].strip().split()
duplicated_first_line = ['  '.join([locus, locus]) for locus in first_line]


# Putting everything together and writing them into "whales_all_modified.str".
new_lines = ['\t'.join(duplicated_first_line)] + empty + lines[1:]

with open(modified, 'w') as file:
    file.writelines(new_lines)

# Make a DataFrame out of the file
df = pd.read_csv(modified, sep='\t')

# Filter out duplicates based on all columns except the first one (sample ID)
df_no_duplicates = df.drop_duplicates(subset=df.columns[1:], keep='first')

print(len(df_no_duplicates))


# NEXT STEP: Find the pairs

# Function to calculate similarity between two alleles
def calculate_similarity(allele1, allele2):
    return allele1 == allele2


# Function to find parent-offspring pairs based on at least 50% similarity per locus
def find_parent_offspring_pairs(data):
    num_loci = data.shape[1] // 2                       # Since each locus is represented by two columns, dividing the
                                                        # total number of columns by two gives us the number of loci.
    pairs = []

    for i in range(data.shape[0] - 1):
        for j in range(i + 1, data.shape[0]):
            has_shared_allele = True  # Assume shared allele until proven otherwise

            # Check if there is at least one same allele in every pair of columns
            for k in range(num_loci):
                idx1 = 2 * k  # Index for the first column of the current locus
                idx2 = 2 * k + 1  # Index for the second column of the current locus

                if not (data[i, idx1] == data[j, idx1] or data[i, idx1] == data[j, idx2] or
                        data[i, idx2] == data[j, idx1] or data[i, idx2] == data[j, idx2]):
                    has_shared_allele = False
                    break  # No need to check further for this pair of samples

            if has_shared_allele:
                pairs.append((data[i, 0], data[j, 0]))  # Append sample IDs to the pairs list

    return pairs


# Read data from the file
data = np.genfromtxt('whales_all_modified.str', dtype=int, skip_header=1)


# Find parent-offspring pairs
parent_offspring_pairs = find_parent_offspring_pairs(data)


# Print results
print('Parent-Offspring Pairs: ')
for pair in parent_offspring_pairs:
    print(f'Sample {pair[0]} and Sample {pair[1]}')
print(len(parent_offspring_pairs))

"""

This gives back the parent-offspring pairs as well as duplicates. Based on the findings of the previous assignment
if the code is correct the parent-offspring pairs should be (229-117) = 112. Still needs work

"""
