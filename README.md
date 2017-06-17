# ml-challenge

Code used to solve Chaordic's ML Challenge
 
Given the simplicity of the problem, I decided to try not using a pre-built model from sklearn. Instead, I made a probabilistic model using only pandas as a dependency.
 
To make it work, I had to substitute NaN values of the "data" dataset with "NaN" between quotation marks, otherwise pandas wouldn't read the file. The main script is fully commented, explaining each step of the program, from loading the dataset to saving the final guess csv file


# How it works:

The approach used to solve the problem was taking only the products viewed by each user into account. Each product carry a gender probability based on the dataset, and then the target's genders are computed by iterating through these probabilities.
 
To iterate through multiple probabilities, I used the following function:
 
f(a,b) = (a * b) / ((1-a) * (1-b) + (a * b))
 
where "a" and "b" are values between 0 and 1, representing a probability of one user being a male.
 
For example, if one user visited 4 products with (0.5, 0.6, 0.7, 0.55) probability vectors, his final probability of being male will be:
 
f(f(f(0.5,0.6),0.7),0.55) = 0.8105 (about 81%)


# Next Steps:
 
Moving the program to a framework could greatly increase performance. As I didn't use anything to make the process of iterating through rows and dicts faster, the program takes nearly 5 minutes to complete.
 
Using a Jupyter notebook instead of the stock shell will make the code easier to understand and will make the coding process faster.
 
This program is somewhat blind as it only cares about the products each user visited. It might achieve better results if it analyzed more aspects of user's shopping habits. Besides that, automating the process of choosing the parameters could also improve the results and productivity.


# How to run the code

First, unpack "target" and "data". Then, execute "main.py". When the program is over, you should see an "attempt" file inside your folder, which is the final guess csv file.
