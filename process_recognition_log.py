import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

o = 'f'
n = 'k'
s = 'j'

def calculate_response_ratios(table):
    response_old = table['Response'] == o
    olds = len(table[response_old].index) / len(table)
    response_similar = table['Response'] == s
    similars = len(table[response_similar].index) / len(table)
    response_new = table['Response'] == n
    news = len(table[response_new].index) / len(table)

    return [olds, similars, news]

def calculate_false_alarm_rate(table):
    alarms = table['Response'] == o
    false_alarms = (table['StimType'] != 'TARGET') & alarms
    fa_rate = len(table[false_alarms])/len(table[alarms])
    return fa_rate

# '106894', '136569', '200050', '422889', '808337', '943684'
subjects = ['106894', '136569', '200050', '422889', '808337', '943684','148465', '079723', '202193', '349560']
fname = '_recognition_TerKepEsz.csv'
n_subjects= len(subjects)

o_olds = []
o_similars = []
o_news = []

l_olds = []
l_similars = []
l_news = []

responses_obj_targets = []
responses_obj_lures = []
responses_obj_foils = []

responses_loc_targets = []
responses_loc_lures = []
responses_loc_foils = []

fa_rates = []

for subject in subjects:
    print('\n', subject)
    subj_file = subject + fname
    response_table = pd.read_csv(subj_file, sep=',', lineterminator='\n')
    location_trials = response_table['TrialType'] == 'LOC'
    object_trials = response_table['TrialType'] == 'OBJ'
    target_trials = response_table['StimType'] == 'TARGET'
    lure_trials = response_table['StimType'] == 'LURE'
    foil_trials = response_table['StimType'] == 'FOIL'
    o_old = []
    o_similar = []
    o_new = []

    l_old = []
    l_similar = []
    l_new = []

    fa_rate = calculate_false_alarm_rate(response_table)
    print('False Alarm Rate: ', fa_rate)
    # Object Trials
    # targets
    obj_targets = object_trials & target_trials
    obj_target_responses = calculate_response_ratios(response_table[obj_targets])
    responses_obj_targets.append(obj_target_responses)
    o_old.append(obj_target_responses[0])
    o_similar.append(obj_target_responses[1])
    o_new.append(obj_target_responses[2])
    #lures
    obj_lures = object_trials & lure_trials
    obj_lure_responses = calculate_response_ratios(response_table[obj_lures])
    responses_obj_lures.append(obj_lure_responses)
    o_old.append(obj_lure_responses[0])
    o_similar.append(obj_lure_responses[1])
    o_new.append(obj_lure_responses[2])
    #foils
    obj_foils = object_trials & foil_trials
    obj_foil_responses = calculate_response_ratios(response_table[obj_foils])
    responses_obj_foils.append(obj_foil_responses)
    o_old.append(obj_foil_responses[0])
    o_similar.append(obj_foil_responses[1])
    o_new.append(obj_foil_responses[2])

    # Location Trials
    # targets
    loc_targets = location_trials & target_trials
    loc_target_responses = calculate_response_ratios(response_table[loc_targets])
    responses_loc_targets.append(loc_target_responses)
    l_old.append(loc_target_responses[0])
    l_similar.append(loc_target_responses[1])
    l_new.append(loc_target_responses[2])
    #lures
    loc_lures = location_trials & lure_trials
    loc_lure_responses = calculate_response_ratios(response_table[loc_lures])
    responses_loc_lures.append(loc_lure_responses)
    l_old.append(loc_lure_responses[0])
    l_similar.append(loc_lure_responses[1])
    l_new.append(loc_lure_responses[2])
    #foils
    loc_foils = location_trials & foil_trials
    loc_foil_responses = calculate_response_ratios(response_table[loc_foils])
    responses_loc_foils.append(loc_foil_responses)
    l_old.append(loc_foil_responses[0])
    l_similar.append(loc_foil_responses[1])
    l_new.append(loc_foil_responses[2])

    print(obj_target_responses, obj_lure_responses, obj_foil_responses) # print for debugging
    print(loc_target_responses, loc_lure_responses, loc_foil_responses)

    # add individual lists to global lists
    o_olds.append(o_old)
    o_similars.append(o_similar)
    o_news.append(o_new)

    l_olds.append(l_old)
    l_similars.append(l_similar)
    l_news.append(l_new)

    fa_rates.append(fa_rate)

# convert lists to numpy array for easier handling
o_olds = np.array(o_olds)
o_similars = np.array(o_similars)
o_news = np.array(o_news)

l_olds = np.array(l_olds)
l_similars = np.array(l_similars)
l_news = np.array(l_news)

responses_obj_targets = np.array(responses_obj_targets)
responses_obj_lures = np.array(responses_obj_lures)
responses_obj_foils = np.array(responses_obj_foils)
responses_loc_targets = np.array(responses_loc_targets)
responses_loc_lures = np.array(responses_loc_lures)
responses_loc_foils = np.array(responses_loc_foils)
responses_obj = [responses_obj_targets, responses_obj_lures, responses_obj_foils]
responses_loc = [responses_loc_targets, responses_loc_lures, responses_loc_foils]
resp_per_ttype = [responses_obj, responses_loc]

# calculate average
av_o_olds = np.mean(o_olds, axis = 0)
av_o_similars = np.mean(o_similars, axis = 0)
av_o_news = np.mean(o_news, axis = 0)

av_l_olds = np.mean(l_olds, axis = 0)
av_l_similars = np.mean(l_similars, axis = 0)
av_l_news = np.mean(l_news, axis = 0)

av_fa_rate = sum(fa_rates)/len(fa_rates)

print(o_olds.shape)
# Plot
# Bar plott with average
fig, axs = plt.subplots(nrows=2)
fig.suptitle('Average across {} participants\nMean False Alarm Rate: {:0.3f}'.format(n_subjects, av_fa_rate))
labels = ['TARGET', 'LURE', 'FOIL']
x = np.arange(len(labels))  # the label locations
width = 0.2  # the width of the bars

resp_o_old = axs[0].bar(x - width, av_o_olds, width, edgecolor = 'blue', color = 'white', alpha = 0.6, linewidth = 3, label='Old')
resp_o_similar = axs[0].bar(x, av_o_similars, width, edgecolor = 'orange', color = 'white', alpha = 0.6, linewidth = 3,label='Similar')
resp_o_new = axs[0].bar(x + width, av_o_news, width, edgecolor = 'green', color = 'white', alpha = 0.6, linewidth = 3,label='New')

# Add some text for labels, title and custom x-axis tick labels, etc.
axs[0].set_ylim(top=1.0)
axs[0].set_ylabel('Ratio')
axs[0].set_title('Object Trials')
axs[0].set_xticks(x)
axs[0].set_xticklabels(labels)
axs[0].legend()

resp_l_old = axs[1].bar(x - width, av_l_olds, width, edgecolor = 'blue', color = 'white', alpha = 0.6, linewidth = 3,label='Old')
resp_l_similar = axs[1].bar(x, av_l_similars, width, edgecolor = 'orange', color = 'white', alpha = 0.6, linewidth = 3,label='Similar')
resp_l_new = axs[1].bar(x + width, av_l_news, width, edgecolor = 'green', color = 'white', alpha = 0.6, linewidth = 3,label='New')

resp_o = [resp_o_old, resp_o_similar, resp_o_new]
resp_l = [resp_l_old, resp_l_similar, resp_l_new]
resp = [resp_o, resp_l]

axs[1].set_ylim(top=1.0)
axs[1].set_ylabel('Ratio')
axs[1].set_title('Location Trials')
axs[1].set_xticks(x)
axs[1].set_xticklabels(labels)
axs[1].legend()

def autolabel(rects):
    """Attach a text label above each bar in *rects*, displaying its height."""
    for rect in rects:
        height = rect.get_height()
        ax.annotate('{:0.3f}'.format(height),
                     xy=(rect.get_x() + rect.get_width() / 2, height/8),
                     xytext=(0, 0),  # 3 points vertical offset
                     textcoords="offset points",
                     ha='center', va='bottom')

for i,ax in enumerate(axs):
    for rect in resp[i]:
        autolabel(rect)

# plt.show()
# del fig, axs

# Scatter plot with individual results
# fig, axs = plt.subplots(nrows=2)
# fig.suptitle('Individual performance of {} participants\n Mean False Alarm Rate: {:0.3f}'.format(n_subjects, av_fa_rate))
marker_size = 12

old_x = np.full((n_subjects,3), x-width)
similar_x = np.full((n_subjects,3), x)
new_x = np.full((n_subjects,3), x + width)

resp_o_old = axs[0].scatter(old_x, o_olds, marker_size)
resp_o_similar = axs[0].scatter(similar_x, o_similars, marker_size)
resp_o_new = axs[0].scatter(new_x, o_news, marker_size)

palette = plt.get_cmap('tab20')

for a, r in enumerate(resp_per_ttype):
    for row in range(n_subjects):
        for i, trial_type in enumerate(r):
            axs[a].plot([x[i]-width, x[i],x[i]+width], trial_type[row], color=palette(row), linewidth=1.5, alpha=0.8)

# Add some text for labels, title and custom x-axis tick labels, etc.
axs[0].set_ylim(top=1.0)
axs[0].set_ylabel('Ratio')
axs[0].set_title('Object Trials')
axs[0].set_xticks(x)
axs[0].set_xticklabels(labels)
axs[0].legend()

resp_l_old = axs[1].scatter(old_x, l_olds, marker_size)
resp_l_similar = axs[1].scatter(similar_x, l_similars, marker_size)
resp_l_new = axs[1].scatter(new_x, l_news, marker_size)

axs[1].set_ylim(top=1.0)
axs[1].set_ylabel('Ratio')
axs[1].set_title('Location Trials')
axs[1].set_xticks(x)
axs[1].set_xticklabels(labels)
axs[1].legend()

fig.tight_layout()
plt.show()