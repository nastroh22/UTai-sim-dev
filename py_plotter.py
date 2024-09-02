import matplotlib.pyplot as plt

# Example data
time = [0, 1, 2, 3, 4, 5]
series1 = [-0.5, -0.2, 0.1, 0.4, 0.8, 1.0]  # Range between -1 and 1
series2 = [50, 100, 150, 200, 250, 300]     # Range between 0 and 300

# Create figure and primary axis
fig, ax1 = plt.subplots()

# Plot the first time series on the primary y-axis
ax1.plot(time, series1, 'b-', label='Series 1')
ax1.set_xlabel('Time')
ax1.set_ylabel('Series 1', color='b')
# ax1.set_ylim(-1, 1)  # Set y-axis limits for Series 1

# Create a secondary y-axis
ax2 = ax1.twinx()
ax2.plot(time, series2, 'r-', label='Series 2')
ax2.set_ylabel('Series 2', color='r')
# ax2.set_ylim(0, 300)  # Set y-axis limits for Series 2

# Optionally, adjust the second y-axis scale to match the visual trends
# This is a simple linear scaling, adjust as needed to fit your data
ax2.set_ylim(ax1.get_ylim()[0] * 150, ax1.get_ylim()[1] * 150)

# Display the plot
plt.show()