import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
from scipy.stats.stats import pearsonr

data = pd.read_excel('some_stat.xlsx')

print(data.dtypes)

data['hour'] = data['new_date'].dt.hour

# создание гистограммы
hist, bin_edges = np.histogram(data['hour'])

print(hist)
print(bin_edges)
## график гистограммы

# размер окна
plt.figure(figsize = [7, 5])

#create histogram bars ??
plt.bar(bin_edges[:-1], hist, width = 1.5, color = 'blue', alpha = 0.6)
#define x-axis limits
plt.xlim(min(bin_edges), max(bin_edges))
#add horizontal grid lines
plt.grid(axis = 'y', alpha = 0.7)
# подпись по оси x и по оси y
plt.xlabel('Hour of the day', fontsize = 15)
plt.ylabel('Counts', fontsize = 15)

#add tick marks on the x-axis and y-axis
plt.xticks(fontsize = 12)
plt.yticks(fontsize = 12)

#add plot title
plt.title('Distribution of publication times', fontsize = 15)
#show plot
#plt.show()

# posts that were published between 12:00 and 16:59
midday_posts = data.loc[(data['hour'] >= 12) & (data['hour'] <= 16)]
# posts that were published before 12:00 or after 16:59
other_posts = data.loc[(data['hour'] < 12) | (data['hour'] > 16)]

print('midday_posts', np.mean(midday_posts['likes']))
print('other_posts', np.mean(other_posts['likes']))

# t-test (Тест Стъюдента)
t_stat, p_val = stats.ttest_ind(midday_posts['likes'], other_posts['likes'], equal_var = False)
print('t-satistic', t_stat)
print('p-value', p_val)
# there is a 31,7 % chance that t-stats may be true

#mean number of likes
mean_likes_midday = np.mean(midday_posts['likes'])
mean_likes_other = np.mean(other_posts['likes'])

# number of posts in sample
n_midday = len(midday_posts.index)
n_other = len(other_posts.index)

# standart errors
se_midday = np.std(midday_posts['likes'] / np.sqrt(n_midday))
se_other = np.std(other_posts['likes'] / np.sqrt(n_other))

## confidence intervals (CI) using 95% confidence level
# df - degrees of freedom, df = n - 1, where n is the size of the sample
# loc = sample mean
# scale - standart error of the sample mean

ci_midday = stats.t.interval(0.95,
df = n_midday - 1,
loc = mean_likes_midday,
scale = se_midday)

ci_other = stats.t.interval(0.95,
df = n_other - 1,
loc = mean_likes_other,
scale = se_other)

print('95% conf., midday posts:', ci_midday)
print('95% conf., other posts:', ci_other)

# We have a 95% confidence that the population mean of the midday posts is
#between 14.7 and 17.9 likes, and the population mean of all other posts
#is between 12.7 and 17.1 likes. The large overlap between these intervals
#explain the fact that we could not reject  𝐻0 : it is impossible to compare
#two population means since they might be anywhere within roughly the same range
#The code below provides one of the ways to visualize confidence intervals.

#histogram of likes
plt.hist(data.likes, bins = 80)

# лимит по оси x чтобы устранитть посты с большим колличествои лайков (outliers)
plt.xlim(0, 55)

#добавление названия оси x и оси y
plt.xlabel('Number of likes')
plt.ylabel('Counts')

# select where to plot confidence interval horizontally
# these values are selcted by trial and error
# the goal is to create easily readeble visualiztion

midday_y = 10
other_y = 15

## midday posts
# plot confidence interval
plt.plot([ci_midday[0], ci_midday[1]],
[midday_y, midday_y],
'-', color = 'r', linewidth = 4,
label = 'Confiedence interval')

#add point to the line to mark the sample mean
plt.plot(np.mean(mean_likes_midday), midday_y, 'o', color = 'r', markersize = 10)

## other posts
# plot confidence interval
plt.plot([ci_other[0], ci_other[1]],
[other_y, other_y],
'-', color = 'orange', linewidth = 4,
label = 'Confiedence interval')

#add point to the line to mark the sample mean
plt.plot(np.mean(mean_likes_other), other_y,
'o', color = 'orange', markersize = 10)
plt.show()
# set the seed of random number generator
# ensures consistency
np.random.seed(100)

# create two sets of 50 random numbers
X = np.random.rand(50)
Y = np.random.rand(50)

# plot
plt.scatter(X, Y)
plt.xlabel('X Value')
plt.ylabel('Y Value')

# there are multiple functions to compute correlation in python

# here we use pearsonr() from scipy library
print(pearsonr(X, Y))

# The output contains two values: the first one is the correlation coefficient,
# the second one is the associated p-value. The p-value has the same
# interpretation as in the t-test, and it is used in the same way.
# 𝐻0 : the correlation coefficient is equal to 0

# sometimes it is useful to apply numpy's corrcoef()
print(np.corrcoef(X, Y))

# correlation between X and Y
print('r(X, Y): ', np.corrcoef(X, Y)[0, 1])
# correlation between Y and X
print('r(Y, X): ', np.corrcoef(X, Y)[1, 0])


text_l = []

# loop throught texts
for text in data['text']:
    # try to compute length
    try:
        text_l.append(len(text))
    # in case of error (text is missing) add 0
    except:
        text_l.append(0)
#create a new column and fill with text_l values
data['text_l'] = text_l

#add fraction of  Hour
data['hour'] = data['new_date'].dt.hour + (data['new_date'].dt.minute / 60)

# print(np.quantile(data.likes, [0.99])) = 57.99
# print(np.quantile(data.views, [0.99])) = 5319.62

data_clean = data.copy()[(data.likes < 57.99) &
(data.views < 5319.62) &
(data.views > 0)]

print(pearsonr(data_clean['likes'], data_clean['views']))

corr = data_clean[['likes', 'views', 'likes_to_views', 'hour', 'text_l']].corr()

# create plot
corr_plot = sns.heatmap(corr, vmin = -1, vmax = 1, center = 0,
cmap = sns.diverging_palette(20, 220, n = 200), square = True)

# adjust x-axis labels
corr_plot.set_xticklabels(corr_plot.get_xticklabels(),
rotation = 45, horizontalalignment = 'right')

# adjust y-axis labels
corr_plot.set_yticklabels(corr_plot.get_yticklabels(), rotation = 0)
plt.show()
