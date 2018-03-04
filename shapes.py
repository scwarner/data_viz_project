from bokeh.plotting import figure, output_file, show
from bokeh.layouts import row

output_file('shapes.html')

plot = figure(plot_width=400, plot_height=400, title="Shape")

plot_multi = figure(plot_width=400, plot_height=400, title="Multiple Shapes")

plot.patch([1, 2, 3, 4],[7, 12, 9, 3], color="#2B5B84", alpha=0.7, line_width=2)

plot_multi.patches([[1, 1, 4, 4], [3, 5, 9]],
                    [[1, 4, 4, 1], [1, 9, 3]],
                    color=["#5FCF80", "#637A91"],
                    alpha=[0.7, 0.3],
                    line_width=[2,3])


show(row(plot, plot_multi))