import pandas as pd
import random

#Filter out the invalid entries and make one-hot vectors for gender:

print("lendo arquivo...")
produtos = pd.read_json('data',lines=True)
print("arquivo lido!")

produtos = produtos[['productId','gender']]
produtos.productId.fillna('notanumber', inplace=True)
produtos = produtos[produtos.productId != 'notanumber']

produtos_dummies = pd.get_dummies(produtos['gender'])
produtos = pd.concat([produtos,produtos_dummies], axis=1)
produtos = produtos[['productId','F','M']]

print ("'produtos' dataset post-filtering:")
print (produtos)

#We already have a product dataset with one hot vectors, but there are
#duplicated entries, as one product might receive views from more than one
#user. The next thing we are going to do is creating a dict of productIds
#and the number of views from each gender.

#Example: if product 123abc received views from 5 M and 35 F:
#         product_dict['123abc'] = [5, 35]

product_dict = {}

for index, row in produtos.iterrows():
    if (row[0] not in product_dict):
        product_dict[(row[0])] = [row[2],row[1]]
    else:
        product_dict[(row[0])] = [row[2]+product_dict[row[0]][0],row[1]+product_dict[row[0]][1]]

# As the approach for this problem is calculating a probability based on a set
#of probabilities, we need to transform the gender vector from each product into
#a percentage value. I chose to simply use the percentage of males, adding 1 to
#both male and female vectors, hence products with one view will not show 100%
#probability of being male or female.

for product in product_dict.keys():
    product_dict[product] = (product_dict[product][0]+1)/(product_dict[product][0]+product_dict[product][1]+2)

# Now we have a dict of probabilities for each productId! The last step is figuring out some
#way to compute the iteration of probabilities. I chose to multiply the gender probability
#values and then recompute their final probability.

#Ex: Male probability vector: [.60, .55] (60% and 55%)
# final probability = (.60 * .55) / (.60 * .55) + (.40 * .45) = 0.647 (64,7%)

# This method maintain the original value if one of the probabilities is 50% and it converges
# to 1 if there is a sequence of values above .50, or 0 if there is a sequence os values below
# .50

def inverso(x):
    return 1-x

def multiple_probabilities(x,y):
    return ( (x*y) / ( (x*y) + (inverso(x)*inverso(y))) )

# We can finally load the target's userIds and let the script decide the user's gender.

target  = pd.read_json("target", lines=True)
target = target[['uid', 'productId']]
target.productId.fillna('notanumber', inplace=True)

uid_dict = {}

# We should also add an invalid productId probability to product_dict, equal to 50%, in case
#there is a product that appeared in target but didn't appeared in the 'data' dataset

product_dict['notanumber'] = .5

for index, row in target.iterrows():
    if (row[0] not in uid_dict):
        uid_dict[(row[0])] = product_dict[row[1]]
    else:
        uid_dict[(row[0])] = multiple_probabilities(uid_dict[row[0]],product_dict[row[1]])

# When the computing is done, all we have to do is convert the probabilities back to gender
# values and export it as a csv

for user in uid_dict.keys():
    if uid_dict[user]<.50:        
        uid_dict[user] = 'F'
    else:
        uid_dict[user] = 'M'

attempt = pd.DataFrame(list(uid_dict.items()), columns = ['userId', 'gender'])
attempt.to_csv('attempt', index=False)
