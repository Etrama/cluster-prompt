#add license lol
SYSTEM_MESSAGE_SUB_QUESTION = "You will write a Python function called 'solution' to solve math problems. You will only write executable code blocks and use comments to comment out non-executable lines."

PROMPT_SUB_QUESTION = '''
Let's use python to solve math problems. Enclose the "solution" function within backticks.
Let's answer each sub-question in a separate code block within the function and insert a comment containing the sub-question answer as- Sub-Question Answer:answer value.
Question: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?
Sub-Question 1. Determine the total cost of the bagels.
Sub-Question 2. Subtract the total cost of the bagels from Olivia's initial amount of money.
```
def solution():
    # Determine the total cost of the bagels.
    bagel_cost = 3
    num_bagels = 5
    total_cost = bagel_cost * num_bagels
    # Sub-Question Answer: 15

    # Subtract the total cost of the bagels from Olivia's initial amount of money.
    initial_amount = 23
    remaining_amount = initial_amount - total_cost
    # Sub-Question Answer: 8
    
    result = remaining_amount
    return result
```

Let's answer each sub-question in a separate code block and end with a comment containing the answer as- Sub-Question Answer:answer value.
Question: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?
Sub-Question 1. Start with the initial number of golf balls Michael had: 58.
Sub-Question 2. Determine how many golf balls Michael lost on Tuesday: 23.
Sub-Question 3. Subtract the number of golf balls lost on Tuesday from the initial number of golf balls to find out how many golf balls Michael had left after Tuesday.
Sub-Question 4. Determine how many golf balls Michael lost on Wednesday: 2.
Sub-Question 5. Subtract the number of golf balls lost on Wednesday from the number of golf balls Michael had left after Tuesday to find out how many golf balls Michael had at the end of Wednesday.
```
def solution():
    # Start with the initial number of golf balls Michael had: 58.
    initial_balls = 58
    # Sub-Question Answer: 58

    # Determine how many golf balls Michael lost on Tuesday: 23.
    tuesday_loss = 23
    # Sub-Question Answer: 23

    # Subtract the number of golf balls lost on Tuesday from the initial number of golf balls to find out how many golf balls Michael had left after Tuesday.
    balls_after_tuesday = initial_balls - tuesday_loss
    # Sub-Question Answer: 35

    # Determine how many golf balls Michael lost on Wednesday: 2.
    wednesday_loss = 2
    # Sub-Question Answer: 2

    # Subtract the number of golf balls lost on Wednesday from the number of golf balls Michael had left after Tuesday to find out how many golf balls Michael had at the end of Wednesday.
    balls_after_wednesday = balls_after_tuesday - wednesday_loss
    # Sub-Question Answer: 33
    
    result = balls_after_wednesday
    return result
```

Let's answer each sub-question in a separate code block and end with a comment containing the answer as- Sub-Question Answer:answer value.
Question: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?
Sub-Question 1. Start with the initial number of computers in the server room, which is 9.
Sub-Question 2. Determine the number of days from Monday to Thursday, which is 4.
Sub-Question 3. Determine the number of computers installed each day, which is 5.
Sub-Question 4. Calculate the total number of computers installed during those 4 days by multiplying 5 (the number of computers installed each day) by 4 (the number of days).
Sub-Question 5. Add the total number of computers installed to the initial number of computers to get the total number of computers in the server room now.
```
def solution():
    # Start with the initial number of computers in the server room, which is 9.
    initial_computers = 9
    # Sub-Question Answer: 9

    # Determine the number of days from Monday to Thursday, which is 4.
    num_days = 4
    # Sub-Question Answer: 4

    # Determine the number of computers installed each day, which is 5.
    computers_per_day = 5
    # Sub-Question Answer: 5

    # Calculate the total number of computers installed during those 4 days by multiplying 5 (the number of computers installed each day) by 4 (the number of days).
    total_new_computers = computers_per_day * num_days
    # Sub-Question Answer: 20

    # Add the total number of computers installed to the initial number of computers to get the total number of computers in the server room now.
    total_computers = initial_computers + total_new_computers
    # Sub-Question Answer: 29
    
    result = total_computers
    return result
```

Let's answer each sub-question in a separate code block and end with a comment containing the answer as- Sub-Question Answer:answer value.
Question: {question}
'''.strip()