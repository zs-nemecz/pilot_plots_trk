import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# read excel sheet and count number of participant with WAIS data (non-NaN)
df = pd.read_excel('questionnare_evaluation_non_native_excl.xlsx')
n_subjects = df['WAIS'].count()

# define groups
old_a = df[df['Age_Group'] == 1]
young_a = df[df['Age_Group'] == 2]
jitter_old = np.random.uniform(low=0.82, high=1.18, size=len(old_a))
jitter_young = np.random.uniform(low=1.82, high=2.18, size=len(young_a))

# calculate mean and standard deviation for both groups and across groups (only printed)
cross_group_mean = df['WAIS'].mean()
cross_group_std = df['WAIS'].std()
print('Average scores across groups: {:0.3f}\nStandard deviation across groups: {:0.3f}'.format(cross_group_mean, cross_group_std))
old_mean = old_a['WAIS'].mean()
old_std = old_a['WAIS'].std()
young_mean = young_a['WAIS'].mean()
young_std = young_a['WAIS'].std()

# plot
plt.style.use('ggplot') # use R 'ggplot' style (grey background with white grid)
fig, ax = plt.subplots(nrows=1)
fig.suptitle('{} résztvevő WAIS Alteszt pontszáma'.format(n_subjects))
# some formatting values
labels = ['Idős', 'Fiatal']
marker_size = 22
bar_line_width = 3
bar_width = 0.6

# bar plots
error_kw = dict(capsize = 4, alpha = 0.2, elinewidth = 0.6, color = 'grey') # error bar attributes
bar_old = ax.bar(old_a['Age_Group'], old_mean, bar_width, edgecolor = 'plum', fill=False, linewidth = bar_line_width, yerr=old_std, error_kw = error_kw)
bar_young = ax.bar(young_a['Age_Group'], young_mean, bar_width, edgecolor = 'lightgreen', fill=False, linewidth = bar_line_width, yerr=young_std, error_kw = error_kw)
def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('átlag: {:0.1f}'.format(height),
                     xy=(rect.get_x() + rect.get_width() / 2, height/10),
                     textcoords="offset points",
                     xytext=(0, 0),
                     ha='center', va='bottom')
# add average value as label to the bottom of the bars
autolabel(bar_old)
autolabel(bar_young)

# scatter plots
scatter_old = ax.scatter(jitter_old, old_a['WAIS'], marker_size, marker = 'x', color = 'darkorchid')
scatter_young = ax.scatter(jitter_young, young_a['WAIS'], marker_size, marker='x', color = 'forestgreen')

# format axes
ax.set_xticks([1,2])
ax.set_xlabel('Csoportok')
ax.set_xticklabels(labels)
ax.set_ylim(top=55)
ax.set_ylabel('Nyers pontszám')
ax.set_yticks([5,15,25,35,45,55], minor = True)

# fig.tight_layout() # this reduces white space around the figure
plt.show() # finally, show figure
