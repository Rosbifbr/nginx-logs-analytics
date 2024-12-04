import pandas as pd
import matplotlib.pyplot as plt

file = pd.read_csv('proc.csv')
# >>> file.columns
# Index(['IP', 'Date', 'Time', 'Hour', 'Method', 'Status', 'Bytes', 'PathName',
#        'RootPath', 'SubPath'],
#       dtype='object')


# Set date as date type
# file['Date'] = pd.to_datetime(file['Date'])

# Norm others
file['Bytes'] = pd.to_numeric(file['Bytes'], errors='coerce').fillna(0).astype(int)
# Create a new column 'hourofday' by extracting the last two characters from 'Hour'
file['hourofday'] = file['Hour'].str[-2:].astype(int)

#################################### Byte histogram
plt.figure(figsize=(10, 6))
plt.hist(file['Bytes'], bins=200, edgecolor='black')
plt.title('Histogram of Bytes')
plt.xlabel('Bytes')
plt.ylabel('Frequency')
plt.xlim(0, 200000)  # Limit X-axis to 200KB
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.savefig('bytes_histogram.png', dpi=300)
plt.close()

###################################### Count occurrences of RootPaths and order by occurrence
rootpath_counts = file['RootPath'].value_counts()

# Get the top 5 most frequent RootPaths
top_5_rootpaths = rootpath_counts.head(5).index

# Calculate median Bytes for these top RootPaths
median_bytes_top_5 = file[file['RootPath'].isin(top_5_rootpaths)].groupby('RootPath')['Bytes'].median()

# Sort by occurrence again for consistent ordering
median_bytes_top_5 = median_bytes_top_5.loc[top_5_rootpaths]

# Plot the results
plt.figure(figsize=(10, 6))
median_bytes_top_5.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Median Bytes for Top 5 RootPaths by Occurrence')
plt.xlabel('RootPath')
plt.ylabel('Median Bytes')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('median_bytes_top_5.png', dpi=300)

##################################### Request by hour histogram

# Count requests per hour
requests_per_hour = file['hourofday'].value_counts().sort_index()

# Plot the histogram
plt.figure(figsize=(10, 6))
requests_per_hour.plot(kind='bar', color='green', edgecolor='black')
plt.title('Requests by Hour')
plt.xlabel('Hour')
plt.ylabel('Number of Requests')
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('requests_by_hour.png', dpi=300)
plt.close()

