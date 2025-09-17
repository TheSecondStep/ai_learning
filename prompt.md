- [1. Guidelines for Prompting](#1-guidelines-for-prompting)
  - [1.1. Prompting Principles](#11-prompting-principles)
    - [1.1.1. Principle 1: Write clear and specific instructions](#111-principle-1-write-clear-and-specific-instructions)
      - [1.1.1.1. Tactic 1: Use delimiters to clearly indicate distinct parts of the input](#1111-tactic-1-use-delimiters-to-clearly-indicate-distinct-parts-of-the-input)
      - [1.1.1.2. Tactic 2: Ask for a structured output](#1112-tactic-2-ask-for-a-structured-output)
      - [1.1.1.3. Tactic 3: Ask the model to check whether conditions are satisfied](#1113-tactic-3-ask-the-model-to-check-whether-conditions-are-satisfied)
      - [1.1.1.4. Tactic 4: "Few-shot" prompting](#1114-tactic-4-few-shot-prompting)
    - [1.1.2. Principle 2: Give the model time to “think”](#112-principle-2-give-the-model-time-to-think)
      - [1.1.2.1. Tactic 1: Specify the steps required to complete a task](#1121-tactic-1-specify-the-steps-required-to-complete-a-task)
      - [1.1.2.2. Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion](#1122-tactic-2-instruct-the-model-to-work-out-its-own-solution-before-rushing-to-a-conclusion)
  - [1.2. Model Limitations: Hallucinations](#12-model-limitations-hallucinations)
- [2. Iterative Prompt Development](#2-iterative-prompt-development)
- [3. Summarizing](#3-summarizing)
  - [3.1. Summarize Text](#31-summarize-text)
  - [3.2. Try "extract" instead of "summarize"](#32-try-extract-instead-of-summarize)
- [4. Inferring](#4-inferring)
  - [4.1. Sentiment (positive/negative)](#41-sentiment-positivenegative)
  - [4.2. Identify types of emotions](#42-identify-types-of-emotions)
  - [4.3. Doing multiple tasks at once](#43-doing-multiple-tasks-at-once)
  - [4.4. Inferring topics](#44-inferring-topics)
- [5. Transforming](#5-transforming)
  - [5.1. Translation](#51-translation)
    - [5.1.1. Universal Translator](#511-universal-translator)
  - [5.2. Tone Transformation](#52-tone-transformation)
  - [5.3. Format Conversion](#53-format-conversion)
  - [5.4. Spellcheck/Grammar check](#54-spellcheckgrammar-check)
- [6. Expanding](#6-expanding)
  - [6.1. Customize the automated reply to a customer email](#61-customize-the-automated-reply-to-a-customer-email)


# 1. Guidelines for Prompting
## 1.1. Prompting Principles
- **Principle 1: Write clear and specific instructions**
- **Principle 2: Give the model time to "think"**
### 1.1.1. Principle 1: Write clear and specific instructions
#### 1.1.1.1. Tactic 1: Use delimiters to clearly indicate distinct parts of the input
- Delimiters can be anything like: ```, """, < >, `<tag> </tag>`, `:`
<details>
    <summary>Example</summary>
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""
</details>

#### 1.1.1.2. Tactic 2: Ask for a structured output
- JSON, HTML

<details/>
    <summary>Example</summary>
prompt = f"""
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
"""
</details>

#### 1.1.1.3. Tactic 3: Ask the model to check whether conditions are satisfied

<details/>
    <summary>Example</summary>
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""
</details>

#### 1.1.1.4. Tactic 4: "Few-shot" prompting

<details/>
    <summary>Example</summary>
prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
</details>

### 1.1.2. Principle 2: Give the model time to “think” 

#### 1.1.2.1. Tactic 1: Specify the steps required to complete a task

<details>
    <summary>Example</summary>
prompt = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""
</details>

#### 1.1.2.2. Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion

<details>
    <summary>Example</summary>
prompt = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem including the final total. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution \
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
"""
</details>

## 1.2. Model Limitations: Hallucinations

# 2. Iterative Prompt Development

Iterative Process
- Try something
- Analyze where the result does not give what you want
- Clarify instructions, give more time to think
- Refine prompts with a batch of examples

# 3. Summarizing
## 3.1. Summarize Text
<details>
    <summary>Text to summarize</summary>
prod_review = """
Got this panda plush toy for my daughter's birthday, \
who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
"""
</details>

<details>
    <summary>Summarize with a focus on price and value</summary>
prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site to give feedback to the \
pricing deparmtment, responsible for determining the \
price of the product.  

Summarize the review below, delimited by triple 
backticks, in at most 30 words, and focusing on any aspects \
that are relevant to the price and perceived value. 

Review: ```{prod_review}```
"""
</details>

<details>
    <summary>LLM response</summary>
The panda plush toy is loved for its softness and cuteness, but some customers feel it's a bit small for the price.
</details>

<details>
    <summary>Comment</summary>
Summaries include topics that are not related to the topic of focus.
</details>

## 3.2. Try "extract" instead of "summarize"

<details>
    <summary>Example</summary>
prompt = f"""
Your task is to extract relevant information from \ 
a product review from an ecommerce site to give \
feedback to the Shipping department. 

From the review below, delimited by triple quotes \
extract the information relevant to shipping and \ 
delivery. Limit to 30 words. 

Review: ```{prod_review}```
"""
</details>

# 4. Inferring
## 4.1. Sentiment (positive/negative)

<details>
    <summary>Sentiment Example</summary>
prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text: '''{lamp_review}'''
"""
</details>

## 4.2. Identify types of emotions
<details>
    <summary>Identify emotions Example</summary>
prompt = f"""
Identify a list of emotions that the writer of the \
following review is expressing. Include no more than \
five items in the list. Format your answer as a list of \
lower-case words separated by commas.

Review text: '''{lamp_review}'''
"""
</details>

<details>
    <summary>Identify anger Example</summary>
prompt = f"""
Is the writer of the following review expressing anger?\
The review is delimited with triple backticks. \
Give your answer as either yes or no.

Review text: '''{lamp_review}'''
"""
</details>

## 4.3. Doing multiple tasks at once
<details>
    <summary>Doing multiple tasks Example</summary>
prompt = f"""
Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: '''{lamp_review}'''
"""
</details>

## 4.4. Inferring topics
<details>
    <summary>Inferring topics Example</summary>
prompt = f"""
Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample: '''{story}'''
"""
</details>

# 5. Transforming

## 5.1. Translation

<details>
    <summary>Example</summary>
prompt = f"""
Translate the following English text to Spanish: \ 
```Hi, I would like to order a blender```
"""

prompt = f"""
Tell me which language this is: 
```Combien coûte le lampadaire?```
"""

prompt = f"""
Translate the following  text to French and Spanish
and English pirate: \
```I want to order a basketball```
"""

prompt = f"""
Translate the following text to Spanish in both the \
formal and informal forms: 
'Would you like to order a pillow?'
"""
</details>

### 5.1.1. Universal Translator

<details>
    <summary>Example</summary>
for issue in user_messages:
    prompt = f"Tell me what language this is: ```{issue}```"
    lang = get_completion(prompt)
    print(f"Original message ({lang}): {issue}")

    prompt = f"""
    Translate the following  text to English \
    and Korean: ```{issue}```
    """
</details>

## 5.2. Tone Transformation

<details>
    <summary>Example</summary>
prompt = f"""
Translate the following from slang to a business letter: 
'Dude, This is Joe, check out this spec on this standing lamp.'
"""
</details>

## 5.3. Format Conversion

<details>
    <summary>Example</summary>
prompt = f"""
Translate the following python dictionary from JSON to an HTML \
table with column headers and title: {data_json}
"""
</details>

## 5.4. Spellcheck/Grammar check

<details>
    <summary>Example</summary>
for t in text:
    prompt = f"""Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```{t}```"""

prompt = f"""
proofread and correct this review. Make it more compelling. 
Ensure it follows APA style guide and targets an advanced reader. 
Output in markdown format.
Text: ```{text}```
"""
</details>

# 6. Expanding
## 6.1. Customize the automated reply to a customer email

<details>
    <summary>Example</summary>
prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""
</details>