# %%
import multiprocessing as mp
from multiprocessing import shared_memory 
import numpy as np
import random 
import string
import time
from mpi4py import MPI

# %%
def smith_waterman(seq1, seq2, match_score=1, mismatch_penalty=1, gap_penalty=1): 
    max_score = 0
    max_pos = (0,0)
    
    rows = len(seq2) + 1 #matrix size 
    cols = len(seq1) + 1 
    matrix = [[0 for _ in range(cols)] for _ in range(rows)] # Create scoring matrix filled with zeros
       
    # Score
    for i in range(1, rows): # first row/column is 0 so starts in second
        for j in range(1, cols):
            if seq1[j-1] == seq2[i-1]:
                diag = matrix[i-1][j-1] + match_score # if two align get match point
            else:
                diag = matrix[i-1][j-1] - mismatch_penalty # if two do not align, mismatch penalty

            up = matrix[i-1][j] - gap_penalty # puts gap penalty in seq1
            left = matrix[i][j-1] - gap_penalty # puts gap penalty in seq2

            matrix[i][j] = max(0, diag, up, left) # highest score 
            if matrix[i][j] > max_score:
                max_score = matrix[i][j] # keeps track of highest score
                max_pos = (i, j) # where highest score is 
    # now the matrix is scored 
    # reconstructs which two aligned make best match
    aligned_seq1 = ""
    aligned_seq2 = ""
    i, j = max_pos # start from cell with highest score 

    while matrix[i][j] != 0: # trace backwards until reach a 0 ie a stop does not match
        score_current = matrix[i][j] # score of current
        score_diag = matrix[i-1][j-1] # score of diagonal
        score_up = matrix[i-1][j] # score of above
        score_left = matrix[i][j-1] # score of left - which could have to this one

        if seq1[j-1] == seq2[i-1]:
            match = match_score
        else:
            match = -mismatch_penalty # is diagonal a match or mismatch, subtracts for mismatch 
        # how did we arrive at the cell - diagonal, left (gap in seq2), or up (gap in seq1)
        if score_current == score_diag + match:
            aligned_seq1 = seq1[j-1] + aligned_seq1
            aligned_seq2 = seq2[i-1] + aligned_seq2
            i -= 1
            j -= 1 # match was diagnoal; add to strink and move diagonally up and left 
        elif score_current == score_left - gap_penalty: # subtract for gap
            aligned_seq1 = seq1[j-1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            j -= 1 # came from left meaning seq2 has a gap, add - in a seq2 and move left 
        elif score_current == score_up - gap_penalty:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[i-1] + aligned_seq2
            i -= 1
        else: break

    # Print full matrix
    for row in matrix:
        print(row) 

    return aligned_seq1, aligned_seq2, max_score # return the aligned sequence and max score 

# %%
communicator = MPI.COMM_WORLD
rank = communicator.rank
nnode = communicator.size 

def parallel_smith_waterman(seq1, seq2, match_score=1, mismatch_penalty=1, gap_penalty=1): 
    max_score = 0
    max_pos = (0,0)
    
    rows = len(seq2) + 1 #matrix size 
    cols = len(seq1) + 1 
    matrix = [[0 for _ in range(cols)] for _ in range(rows)] # Create scoring matrix filled with zeros
    
    # one multiprocessor is in charge of half of the rows
    # anoterh is in charge of half of the columns
    # they allgather of border regions 
    # process right bottom corner 
    # backtrack their data 
    # share results compare two and pick best alignment 

    aligned_seq1 = ""
    aligned_seq2 = ""
    mid_sequence1 = len(aligned_seq1)/2 # finding midpoint of each sequence
    mid_sequence2 = len(aligned_seq2)/2

    top_half = aligned_seq2[:mid_sequence2] # assign top half 
    left_half = aligned_seq1[:mid_sequence1] # assign left half 

    data_top = comm.bcast(top_half, root=0)
    for i in range(1, rows): # first row/column is 0 so starts in second
        for j in range(1, cols):
            if seq1[j-1] == seq2[i-1]:
                diag = matrix[i-1][j-1] + match_score # if two align get match point
            else:
                diag = matrix[i-1][j-1] - mismatch_penalty # if two do not align, mismatch penalty

            up = matrix[i-1][j] - gap_penalty # puts gap penalty in seq1
            left = matrix[i][j-1] - gap_penalty # puts gap penalty in seq2

            matrix[i][j] = max(0, diag, up, left) # highest score 
            if matrix[i][j] > max_score:
                max_score = matrix[i][j] # keeps track of highest score
                max_pos = (i, j) # where highest score is 

    data_left = comm.bcast(left_half, root=1)
    for i in range(1, rows): # first row/column is 0 so starts in second
        for j in range(1, cols):
            if seq1[j-1] == seq2[i-1]:
                diag = matrix[i-1][j-1] + match_score # if two align get match point
            else:
                diag = matrix[i-1][j-1] - mismatch_penalty # if two do not align, mismatch penalty

            up = matrix[i-1][j] - gap_penalty # puts gap penalty in seq1
            left = matrix[i][j-1] - gap_penalty # puts gap penalty in seq2

            matrix[i][j] = max(0, diag, up, left) # highest score 
            if matrix[i][j] > max_score:
                max_score = matrix[i][j] # keeps track of highest score
                max_pos = (i, j) # where highest score is 
    
    #all gather border values and determine max score 

    communicator.allgather(data_top[-1], data_left[:, -1])
    for i in range(1, rows): # first row/column is 0 so starts in second
        for j in range(1, cols):
            if seq1[j-1] == seq2[i-1]:
                diag = matrix[i-1][j-1] + match_score # if two align get match point
            else:
                diag = matrix[i-1][j-1] - mismatch_penalty # if two do not align, mismatch penalty

            up = matrix[i-1][j] - gap_penalty # puts gap penalty in seq1
            left = matrix[i][j-1] - gap_penalty # puts gap penalty in seq2

            matrix[i][j] = max(0, diag, up, left) # highest score 
            if matrix[i][j] > max_score:
                max_score = matrix[i][j] # keeps track of highest score
                max_pos_last = (i, j) # where highest score is 

#only do from last matrix 
    i, j = max_pos_last # start from cell with highest score 
    while matrix[i][j] != 0: # trace backwards until reach a 0 ie a stop does not match
        score_current = matrix[i][j] # score of current
        score_diag = matrix[i-1][j-1] # score of diagonal
        score_up = matrix[i-1][j] # score of above
        score_left = matrix[i][j-1] # score of left - which could have to this one

        if seq1[j-1] == seq2[i-1]:
            match = match_score
        else:
            match = -mismatch_penalty # is diagonal a match or mismatch, subtracts for mismatch 
        # how did we arrive at the cell - diagonal, left (gap in seq2), or up (gap in seq1)
        if score_current == score_diag + match:
            aligned_seq1 = seq1[j-1] + aligned_seq1
            aligned_seq2 = seq2[i-1] + aligned_seq2
            i -= 1
            j -= 1 # match was diagnoal; add to string and move diagonally up and left 
        elif score_current == score_left - gap_penalty: # subtract for gap
            aligned_seq1 = seq1[j-1] + aligned_seq1
            aligned_seq2 = "-" + aligned_seq2
            j -= 1 # came from left meaning seq2 has a gap, add - in a seq2 and move left 
        elif score_current == score_up - gap_penalty:
            aligned_seq1 = "-" + aligned_seq1
            aligned_seq2 = seq2[i-1] + aligned_seq2
            i -= 1
        else: break

    # Print full matrix
    for row in matrix:
        print(row) 

    return aligned_seq1, aligned_seq2, max_score # return the aligned sequence and max score 

# %%
# test alignment of sequences

smith_waterman('TACA', 'TATG')

# %%
# test using examples in problem set

smith_waterman('tgcatcgagaccctacgtgac', 'actagacctagcatcgac')

# %%
# test using examples in problem set - returns a more complex matching case 

smith_waterman('tgcatcgagaccctacgtgac', 'actagacctagcatcgac', gap_penalty=2)

# %%
# testing - proves works because all match
smith_waterman('gggg', 'gggg')

# %%
# testing - proves works because none match
smith_waterman('cccc', 'gggg')

# %%
# returns simple matching case
smith_waterman('caac', 'gaag')

# %%
# testing - proves works because none match
# clarified with ChatGPT difference between gap penalty and mismatch penalty 
smith_waterman('ACGATCG', 'ACGGTCG', gap_penalty=0)

# %%
# gap penalty of 2 makes mismatches perferred to gaps 
smith_waterman('ACGATCG', 'ACGGTCG', gap_penalty=2)

# %%
smith_waterman('ACGTTGAC', 'ACGTGAC', gap_penalty=2)

# %%
# generate random sequences to test

def random_dna(n, seed):
    return ''.join(random.choice("ACGT") for _ in range(n))

seq1 = random_dna(400, seed=2)
seq2 = random_dna(400, seed=2)
H = parallel_smith_waterman(seq1, seq2)

# %%
parallel_smith_waterman('actagtact', 'gtacgtaatgca')

# %%
parallel_smith_waterman('aaagaggtaacccatatgggaccaaagattggcacccggggatatattttatgtgggaacaacaaacaaaatttgggaagggggggaagaacacccccaccaaatttgatgttctatattttgtctattccctttaaaattggggttggggtttcccccccctttaaaaaaaatattgtggtgggtggggtgggtggggaggggtggttgtgggcccccccgggcgggggcgccccgcccgcccccccccaccccacccacccccaaaacccc', 'aaagaggtaacccatatgggaccaaagattggcacccggggataggggtttaacgggaacaacaaacaattaattaattaagggggggaagaacaccgggctacgtattgatgttctattttttttaaattccctttaaaattggggttggggtttccctgcatgcatgcttgtggtgggtggggtgggtggggttttaaaacccggggtttaagttgtgggcccccccccccccgggcgccccgcccgcccccccccaccccacccatttttttttccccc')

# %%



