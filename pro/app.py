from flask import Flask, render_template, request
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def calculate_statistics(data):
    mean = statistics.mean(data)
    median = statistics.median(data)
    modes = statistics.multimode(data)
    if len(modes) == len(data):
        mode = "No unique mode"
    else:
        mode = ', '.join(map(str, modes))
    stddev = statistics.stdev(data)
    sorted_data = sorted(data)
    q1 = statistics.median(sorted_data[:len(sorted_data)//2])
    q3 = statistics.median(sorted_data[len(sorted_data)//2:])
    quartile_deviation = (q3 - q1) / 2
    return mean, median, mode, stddev, quartile_deviation

def check_control(data, ucl, lcl):
    out_of_control = any(x > ucl or x < lcl for x in data)
    return "Out of Control" if out_of_control else "In Control"

def create_plots(data):
    if not os.path.exists('static'):
        os.makedirs('static')
    
    plt.figure()
    plt.bar(range(len(data)), data)
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Bar Chart of Data')
    plt.savefig('static/bar_chart.png')
    plt.close()

    plt.figure()
    sns.lineplot(x=range(len(data)), y=data)
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Line Chart of Data')
    plt.savefig('static/line_chart.png')
    plt.close()

    plt.figure()
    plt.hist(data, bins=10)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Data')
    plt.savefig('static/histogram.png')
    plt.close()

    plt.figure()
    plt.scatter(range(len(data)), data)
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title('Scatter Plot of Data')
    plt.savefig('static/scatter_plot.png')
    plt.close()

    plt.figure()
    sns.boxplot(data=data, orient='h')
    plt.xlabel('Value')
    plt.title('Box Plot of Data')
    plt.savefig('static/box_plot.png')
    plt.close()

    plt.figure()
    plt.pie(data, labels=range(len(data)), autopct='%1.1f%%')
    plt.title('Pie Chart of Data')
    plt.savefig('static/pie_chart.png')
    plt.close()

    plt.figure()
    data_matrix = np.array(data).reshape(-1, 1)
    df = pd.DataFrame(data_matrix, columns=['Data'])
    corr = df.corr()
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title('Heatmap of Data')
    plt.savefig('static/heatmap.png')
    plt.close()

    plt.figure()
    sns.pairplot(df)
    plt.savefig('static/pair_plot.png')
    plt.close()

    # X-Chart (Individuals Chart)
    plt.figure()
    mean = np.mean(data)
    stddev = np.std(data)
    ucl = mean + 3 * stddev
    lcl = mean - 3 * stddev
    control_status = check_control(data, ucl, lcl)
    plt.plot(data, marker='o', linestyle='-', color='b')
    plt.axhline(mean, color='g', linestyle='--')
    plt.axhline(ucl, color='r', linestyle='--')
    plt.axhline(lcl, color='r', linestyle='--')
    plt.xlabel('Index')
    plt.ylabel('Value')
    plt.title(f'X-Chart ({control_status})')
    plt.savefig('static/x_chart.png')
    plt.close()

    # P-Chart (Proportion of Defectives)
    plt.figure()
    p_bar = np.mean(data)
    n = len(data)
    ucl = p_bar + 3 * np.sqrt((p_bar * (1 - p_bar)) / n)
    lcl = p_bar - 3 * np.sqrt((p_bar * (1 - p_bar)) / n)
    control_status = check_control(data, ucl, lcl)
    plt.plot(data, marker='o', linestyle='-', color='b')
    plt.axhline(p_bar, color='g', linestyle='--')
    plt.axhline(ucl, color='r', linestyle='--')
    plt.axhline(lcl, color='r', linestyle='--')
    plt.xlabel('Index')
    plt.ylabel('Proportion Defective')
    plt.title(f'P-Chart ({control_status})')
    plt.savefig('static/p_chart.png')
    plt.close()

    # R-Chart (Range Chart)
    plt.figure()
    ranges = [max(data[i:i+2]) - min(data[i:i+2]) for i in range(0, len(data), 2)]
    mean_range = np.mean(ranges)
    ucl = mean_range + 3 * np.std(ranges)
    lcl = mean_range - 3 * np.std(ranges)
    control_status = check_control(ranges, ucl, lcl)
    plt.plot(ranges, marker='o', linestyle='-', color='b')
    plt.axhline(mean_range, color='g', linestyle='--')
    plt.axhline(ucl, color='r', linestyle='--')
    plt.axhline(lcl, color='r', linestyle='--')
    plt.xlabel('Index')
    plt.ylabel('Range')
    plt.title(f'R-Chart ({control_status})')
    plt.savefig('static/r_chart.png')
    plt.close()

    # C-Chart (Count of Defects)
    plt.figure()
    c_bar = np.mean(data)
    ucl = c_bar + 3 * np.sqrt(c_bar)
    lcl = c_bar - 3 * np.sqrt(c_bar)
    control_status = check_control(data, ucl, lcl)
    plt.plot(data, marker='o', linestyle='-', color='b')
    plt.axhline(c_bar, color='g', linestyle='--')
    plt.axhline(ucl, color='r', linestyle='--')
    plt.axhline(lcl, color='r', linestyle='--')
    plt.xlabel('Index')
    plt.ylabel('Count of Defects')
    plt.title(f'C-Chart ({control_status})')
    plt.savefig('static/c_chart.png')
    plt.close()

@app.route('/results', methods=['POST'])
def results():
    try:
        data_input = request.form.get('data')
        grouped_data_input = request.form.get('grouped_data')
        data = []
        
        if data_input:
            data = [float(x) for x in data_input.split(',')]
        
        if grouped_data_input:
            grouped_data = grouped_data_input.split(';')
            for group in grouped_data:
                try:
                    interval, frequency = group.split(':')
                    interval_start, interval_end = map(float, interval.split('-'))
                    frequency = int(frequency)
                    midpoint = (interval_start + interval_end) / 2
                    data.extend([midpoint] * frequency)
                except ValueError:
                    return f"Invalid format in grouped data: {group}. Expected format is interval:frequency (e.g., 1-2:3)."
        
        mean, median, mode, stddev, quartile_deviation = calculate_statistics(data)
        create_plots(data)

        return render_template('results.html', mean=mean, median=median, mode=mode, stddev=stddev, quartile_deviation=quartile_deviation)
    except Exception as e:
        print("Error:", e)
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
