CLUSTER_SYSTEM_MESSAGE = """ You will solve math problems.\
    Produce numerical answers in the format: The answer is:answer value.\
    You do not need to mention the units of the answer value.\
    Keep in mind that the answer value should always be an integer.\
"""
#our structure is general information + cluster prompt

# GENERAL_INFORMATION_PREFIX = """ 
# Following is some general information that you should know:
# Days per month are as follows: January: 31, February: 28, March: 31, April: 30, May: 31, June: 30, July: 31, August: 31, September: 30, October: 31, November: 30, December: 31.
# In a leap year, February has 29 days but unless mentioned assume that all years are non-leap years.
# There are 7 days in a week, 24 hours in a day, 60 minutes in an hour, and 60 seconds in a minute.
# There are 16 ounces in a pound.
# 1 lb = 1 pound = 16 oz = 16 ounces = 453 g = 453 grams = 0.453 kg.
# 1 oz = 1/16 lb = 28 g = 0.028 kg. 1 kg = 1000 mg = 2.2 lb = 35 oz. 1 gm = 0.04 oz = 0.001 kg. 1 gm= 1000 mg.
# 1 teaspoon= 5 ml. 1 tablespoon= 15 ml.
# 1 meter = 100 cm = 1000 mm = 0.001 km = 39.37 inches = 3.28 feet = 1.09 yards.
# When you have a recurring decimal like 2/3, use at least 6 decimal places. So 2/3 = 0.66667.
# Keep in mind that the answer value should always be an integer.
# """

CLUSTER_PROMPT = '''
Following is some general information that you should know:
Days per month are as follows: January: 31, February: 28, March: 31, April: 30, May: 31, June: 30, July: 31, August: 31, September: 30, October: 31, November: 30, December: 31.
In a leap year, February has 29 days but unless mentioned assume that all years are non-leap years.
There are 7 days in a week, 24 hours in a day, 60 minutes in an hour, and 60 seconds in a minute.
There are 16 ounces in a pound.
1 lb = 1 pound = 16 oz = 16 ounces = 453 g = 453 grams = 0.453 kg.
1 oz = 1/16 lb = 28 g = 0.028 kg. 1 kg = 1000 mg = 2.2 lb = 35 oz. 1 gm = 0.04 oz = 0.001 kg. 1 gm= 1000 mg.
1 teaspoon= 5 ml. 1 tablespoon= 15 ml.
1 meter = 100 cm = 1000 mm = 0.001 km = 39.37 inches = 3.28 feet = 1.09 yards.
When you have a recurring decimal like 2/3, use at least 6 decimal places. So 2/3 = 0.66667.
Keep in mind that the answer value should always be an integer.

Question: Hasan is packing up his apartment because he's moving across the country for a new job. He needs to ship several boxes to his new home. The movers have asked that Hasan avoid putting more than a certain weight in pounds in any cardboard box. The moving company has helpfully provided Hasan with a digital scale that will alert him if a package is too heavy. Hasan is in the kitchen, and he fills a cardboard box with 38 dinner plates. When he checks the box, the scale reports his box is too heavy. Hasan knows each of his plates weighs 10 ounces. He removes a single plate from the box and checks the movers' scale again. The scale reports his box is still too heavy. Hasan repeats the process again and again. When he has removed enough plates, the movers' scale shows the box is now an acceptable weight for shipping. Hasan deduces that each shipping box can hold 20 pounds before the scale says the box is too heavy.  How many plates did Hasan need to remove from the shipping box?
Let's think step by step
Let x be the number of plates removed from the box.
Hasan figured out the movers' weight limit was 20 pounds. Since a pound is equal to 16 ounces, each box can hold 20 * 16, or 320 ounces.
Each plate weighs 10 ounces, so the weight of the plates in the box after Hasan removes enough plates to satisfy the movers' weight limit is (38 - x) * 10 ounces.
Since these two values are equal, we can write the equation (38 - x) * 10 = 320.
Dividing both sides by 10 leaves 38 - x = 32.
Adding x to both sides gives 38 - x + x = 32 + x, or, 38 = 32 + x.
Subtracting 32 from both sides gives the value of x, which is the number of plates removed from the box, 38 - 32 = 32 + x - 32, or, 6 = x.
The answer is 6

Question: A curry house sells curries that have varying levels of spice. Recently, a lot of the customers have been ordering very mild curries and the chefs have been having to throw away some wasted ingredients. To reduce cost and food wastage, the curry house starts monitoring how many ingredients are actually being used and changes their spending accordingly. The curry house needs 3 peppers for very spicy curries, 2 peppers for spicy curries, and only 1 pepper for mild curries. After adjusting their purchasing, the curry house now buys the exact amount of peppers they need. Previously, the curry house was buying enough peppers for 30 very spicy curries, 30 spicy curries, and 10 mild curries. They now buy enough peppers for 15 spicy curries and 90 mild curries. They no longer sell very spicy curries. How many fewer peppers does the curry house now buy?
Let's think step by step
The curry house previously bought 3 peppers per very spicy curry * 30 very spicy curries = 90 peppers for very spicy curries.
They also bought 2 peppers per spicy curry * 30 spicy curries = 60 peppers for spicy curries.
They also bought 1 pepper per mild curry * 10 mild curries = 10 peppers for mild curries.
So they were previously buying 90 + 60 + 10 = 160 peppers.
They now buy 2 peppers per spicy curry * 15 spicy curries = 30 peppers for spicy curries.
They also now buy 1 pepper per mild curry * 90 mild curries = 90 peppers for mild curries.
So they now buy 30 + 90 = 120 peppers.
This is a difference of 160 peppers bought originally - 120 peppers bought now = 40 peppers.
The answer is 40

Question: Five coworkers were talking during the lunch break. Roger, the oldest one, said that he has the same amount of experience in years as all four of the others combined and that his retirement should come when he accumulates 50 years of experience. Peter said that when he came to the company his daughter was 7 years old, and now she is 19 years old. Tom then said he has twice as many years of experience as Robert. Robert said that he has 4 years of experience less than Peter but 2 more years of experience than Mike. How many more years does Roger have to work before he retires?
Let's think step by step
Peter has 19 - 7 = 12 years of experience.
Robert has 12 - 4 = 8 years of experience.
Mike has 8 - 2 = 6 years of experience.
Tom has 2 * 8 = 16 years of experience.
Roger has 12 + 8 + 6 + 16 = 42 years of experience.
Roger has to work another 50 - 42 = 8 years before he retires.
The answer 8

Question: James decides to use tannerite to blow things up to reveal his baby's gender. The explosion ignites both his neighbors' houses and attracts a police officer, who arrests James on two count of arson, one count of manufacturing explosives, and one count of domestic terrorism. If the arson counts each carry a 6-year sentence, the explosives sentence is twice as long as the total arson sentence, and the domestic terrorism charge's sentence is 20 years, how long might James spend in jail?
Let's think step by step
First find the total sentence length for the arson: 6 years/count * 2 counts = 12 years.
hen find the total sentence length for the explosives: 12 years * 2 = 24 years.
Then add each sentence to find the total sentence length: 12 years + 24 years + 20 years = 56 years.
The answer is 56

Question: Ellie went to visit a circus with Sarah and they both got lost in the house of mirrors. They have to travel through the house of mirrors a few times before they finally get out and when they leave, they discuss how many times they've seen their own reflections. Sarah says that every time they were in the room with tall mirrors, she saw her reflection 10 times and every time they were in the room with wide mirrors, she saw her reflection 5 times. Ellie says that every time they were in the room with tall mirrors, she saw her reflection 6 times and every time they were in the room with wide mirrors she saw her reflection 3 times. They both passed through the room with tall mirrors 3 times each and they both passed through the room with wide mirrors 5 times each. In total, how many times did Sarah and Ellie see their reflections?
Let's think step by step
In the rooms with tall mirrors, Sarah saw her reflection a total of 10 reflections * 3 passes = 30 times.
In the rooms with wide mirrors, Sarah saw her reflection a total of 5 reflections * 5 passes = 25 reflections.
So Sarah saw her reflection a total of 30 + 25 = 55 times.
In the rooms with tall mirrors, Ellie saw her reflection a total of 6 reflections * 3 passes = 18 times.
In the rooms with wide mirrors, Ellie saw her reflection a total of 3 reflections * 5 passes = 15 times.
So Ellie saw her reflection a total of 18 + 15 = 33 times.
Therefore, Sarah and Ellie saw their reflections a total of 55 + 33 = 88 times.
The answer is 88

Question: Alec is running for Class President. He thinks that if he can get three-quarters of the class to vote for him then there is no chance anyone else can beat him. Half of the class have already said they will vote for him but out of the remaining students, only 5 have said they are thinking about voting for him. He surveys the students who are thinking about voting for someone else, and changes his flyers to reflect the issues these students are concerned about. This results in a fifth of these students saying they'll vote for him. If Alec's class has 60 students and everyone who said they will vote for him does so, how many more votes does Alec need to reach his goal number of votes?
Let's think step by step
To calculate Alec's goal number of votes, we need to know that 60 students / 4 = 15 students is equal to one-quarter of the class students.
Alec's goal is therefore 15 students * 3 quarters = 45 votes.
Half of the class said they will vote for him, so there are already 60 students / 2 = 30 votes.
Another 5 students are thinking about voting for him which leaves a total so far of 30 + 5 = 35 votes.
This means there are 60 students - 35 voting for Alec = 25 students not voting for Alec.
A fifth of these decided to vote, so this is a further 25 students / 5 = 5 votes.
Alec is therefore receiving a total of 35 + 5 = 40 votes.
So he has missed his goal by 45 goal votes - 40 actual votes = 5 votes.
The answer is 5

Question: Tina is working on her homework when she realizes she's having a hard time typing out her answers on her laptop because a lot of the keys are sticky. She is trying to get her homework done before dinner, though, so she needs to decide if she has time to clean her keyboard first. Tina knows her assignment will only take 10 minutes to complete. Dinner will be ready at 5:30 p.m. Tina decides to time how long it takes to remove and clean one key and will then multiply that time by how many keys she needs to fix. She counts 15 keys that are sticky and times it to take 3 minutes to clean one. After Tina has cleaned one key, there are 14 left to clean. How many minutes total will it take for Tina to both clean the remaining keys and finish her assignment?
Let's think step by step
Tina has already cleaned one key so she has 14 left which take 3 minutes each to clean, 14 x 3 = 42 minutes to clean all the keyboard keys.
Her assignment will take 10 minutes to complete, so she needs 42 minutes + 10 minutes = 52 minutes total before dinner.
The answer is 52

Question: Sam works at the Widget Factory, assembling Widgets. He can assemble 1 widget every 10 minutes. Jack from the loading dock can help assemble widgets when he doesn't have anything else to do. When he helps, they put together 2 complete widgets every 15 minutes. Recently the factory hired Tony to help assemble widgets. Being new to the job, he doesn't work as fast as Sam or Jack. Yesterday Sam worked for 6 hours before he had to leave work early for a dentist appointment. Jack was able to help out for 4 hours before he had to go back to the loading dock to unload a new shipment of widget materials. Tony worked the entire 8-hour shift. At the end of the day, they had completed 68 widgets. How long does it take Tony to assemble a Widget, in minutes?
Let's think step by step
Sam completes a widget every 10 minutes.
When Jack helps they finish 2 in 15 minutes. Sam has finished 1 widget and has begun working on another one, and Jack finishes the second one at 15 minutes. So it takes Jack 15 minutes to complete a widget.
Sam worked for 6 hours yesterday, so he was able to complete 6 hours * 60 minutes per hour / 10 minutes per widget = 36 widgets.
Jack worked for 4 hours, so he was able to complete 4 hours * 60 minutes per hour / 15 minutes per widget = 16 widgets.
Sam, Jack, and Tony were able to complete 68 widgets together. So of those, Tony personally completed 68 widgets - 36 widgets - 16 widgets = 16 widgets.
It took Tony 8 hours to complete those 16 widgets, so he takes 8 hours * 60 minutes per hour / 16 widgets = 30 minutes per widget.
The answer is 30

Question: A man is trying to maximize the amount of money he saves each month. In particular, he is trying to decide between two different apartments. The first apartment costs $800 per month in rent and will cost an additional $260 per month in utilities. The second apartment costs $900 per month and will cost an additional $200 per month in utilities. The first apartment is slightly further from the man's work, and the man would have to drive 31 miles per day to get to work. The second apartment is closer, and the man would only have to drive 21 miles to get to work. According to the IRS, each mile a person drives has an average cost of 58 cents. If the man must drive to work 20 days each month, what is the difference between the total monthly costs of these two apartments after factoring in utility and driving-related costs (to the nearest whole dollar)?
Let's think step by step
The mileage cost for the first apartment will be 31*20*0.58 = $359.60
This makes the total monthly cost of the first apartment 359.60 + 800 + 260 = $1419.60
Similarly, the mileage cost for the second apartment will be 21*20*0.58 = $243.60
Thus, the total monthly cost of the second apartment is 243.60 + 900 + 200 = 1343.60
Therefore, the difference in total monthly costs is 1419.60 - 1343.60 = $76
The answer is 76

Question: On Saturday morning, Renata had $10 to spend. She first went and made a $4 donation in exchange for a ticket to the local charity draw. When the draw was done, she was declared the winner of the 5th prize of $90. Excited, she quickly dashed to play slots at one of the casinos in Atlantic City. Unfortunately, she lost $50 at the first slot machine, $10 at the second and $5 at the last one.  Dejected, she decided to take a long walk. She soon grew thirsty and entered the first gas station she saw. She picked a $1 bottle of water and while paying for it, she bought a $1 lottery ticket. To her utter delight, she won an instant prize of $65. How much money did Renata end up having?
Let's think step by step
After the charity ticket purchase on Saturday morning, Renata remained with 10 - 4 = 6 dollars.
Adding the prize money give her 6 + 90 = 96 dollars.
At the casino, she lost 50 + 10 + 5 = 65 dollars.
Thus far, Renata remained with 96 - 65 = 31 dollars.
The amount she spent on the bottle of water and lottery ticket is 1 + 1 = 2 dollars.
This means that she remained with 31 - 2 = 29 dollars.
Since she won 65 dollars, Renata's ended up having 29 + 65 = 94 dollars.
The answer is 94

Question: {question}
Let's think step by step
'''.strip()