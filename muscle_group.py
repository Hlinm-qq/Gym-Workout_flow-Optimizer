from openai import OpenAI

client = OpenAI()


def getMuscleGroup(equipment):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messa
    )
