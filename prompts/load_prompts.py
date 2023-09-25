# init overall rules
with open('./prompts/rules.txt', 'r') as fp:
    rules_prompt = fp.readlines()
rules_prompt = ''.join(rules_prompt)
RULES = ('system', rules_prompt)

# init background story
with open('./prompts/background.txt', 'r') as fp:
    background_prompt = fp.readlines()
background_prompt = ''.join(background_prompt)
BACKGROUND = ('system', background_prompt)

# init events
with open('./prompts/events.txt', 'r') as fp:
    events_prompt = fp.readlines()
events_prompt = ''.join(events_prompt)
EVENTS = ('system', events_prompt)