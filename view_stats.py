import pstats

# Create a pstats.Stats object
p = pstats.Stats('output.pstats')

# Sort the statistics by the cumulative time spent in the function
p.sort_stats('cumulative')

# Print the statistics
p.print_stats()