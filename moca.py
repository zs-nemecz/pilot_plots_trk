import pandas as pd
import matplotlib.pyplot as plt
import numpy as np



df = pd.read_excel('questionnare_evaluation_non_native_excl.xlsx')

# define group (only old)
old_a = df[df['Age_Group'] == 1]
jitter_old = np.random.uniform(low=0.82, high=1.18, size=len(old_a))
n_subjects = old_a['MoCa'].count()

# get mean and print for convenience
old_mean = old_a['MoCa'].mean()
old_std = old_a['MoCa'].std()
print('Average scores across groups: {:0.3f}\nStandard deviation across groups: {:0.3f}'.format(old_mean, old_std))

# ...and plot
plt.style.use('ggplot')
fig, ax = plt.subplots(nrows=1)
fig.suptitle('MOCA Scores of {} participants'.format(n_subjects))
# some style elements
labels = ['Old']
marker_size = 22
bar_line_width = 3
bar_width = 0.6

# bar plots
error_kw = dict(capsize = 4, alpha = 0.2, elinewidth = 0.6, color = 'grey')
bar_old = ax.bar(old_a['Age_Group'], old_mean, bar_width, edgecolor = 'plum', fill=False, linewidth = bar_line_width, yerr=old_std, error_kw = error_kw)

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('average: {:0.1f}'.format(height),
                     xy=(rect.get_x() + rect.get_width() / 2, height/10),
                     textcoords="offset points",
                     xytext=(0, 0),
                     ha='center', va='bottom')

autolabel(bar_old) # add average value label to the bottom of the bar

# scatter plots
scatter_old = ax.scatter(jitter_old, old_a['MoCa'], marker_size, marker = 'x', color = 'darkorchid')

# format axes
ax.set_xticks([1])
ax.set_ylim(top=33)
# ax.set_xlabel('Groups')
ax.set_ylabel('Raw Score')
ax.set_xticklabels(labels)
ax.set_yticks([5,15,25], minor = True)

fig.tight_layout() # this reduces white space around the figure
plt.show() # finally, show figure
