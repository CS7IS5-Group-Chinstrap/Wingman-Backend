import openai
import re
import config



openai.api_key = config.OPEN_AI_KEY


def get_response(messages):
  
  # Might be useful later
    # prompt = (f"Generate two brief icebreakers based on these key features "
    #       f"extracted from the other person's dating app bio: {topics}. "
    #       "You don't need to use all of them. ")
    # completions = openai.Completion.create(
    #     engine="text-davinci-002",
    #     prompt=prompt,
    #     max_tokens=50,
    #     n=2,
    #     stop=None,
    #     temperature=0.5,
    # )
    # icebreakers = [choice.text.strip() for choice in completions.choices]

  response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  temperature=0.5,
  messages=messages
)
  return  response['choices'][0]['message']['content']


def get_iceBreakers(topics):
    messages = [
    {"role": "user", "content": f"Generate three brief icebreakers based on these key features extracted from the other person's dating app bio: {topics}. You don't need to use all of them."}]
    try:
        response = get_response(messages=messages)
        lines = re.split(r'\d+\.\s*\"', response)[1:]
        # print(lines)
        response = [line[:-2] for line in lines]
        
    except:
       response = ["Hey there! I couldn't help but notice your love for travel. If you could go anywhere in the world, where would you go and why?",
                "Hi! Your profile caught my attention because of your love for music. What's your favorite concert or festival you've ever been to?"
                "Hello! I see that you're a foodie. What's your favorite restaurant in the city and what's the best thing on the menu?"]
    
    return response
