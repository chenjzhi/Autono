from autono import (
    Agent,
    Personality,
    get_openai_model,
    ability
)
from autono.brain.hook import BeforeActionTaken, AfterActionTaken
from autono.message import BeforeActionTakenMessage, AfterActionTakenMessage
from sympy import simplify
from dotenv import load_dotenv

load_dotenv()


@ability
def calculator(expr: str) -> float:
    # this function only accepts a single math expression
    return simplify(expr)


@ability
def write_file(filename: str, content: str) -> str:
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    return f'{content} written to {filename}.'


def before_action_taken(agent: Agent, message: BeforeActionTakenMessage):
    print(f'Agent: {agent.name}, Next move: {message}')
    return message


def after_action_taken(agent: Agent, message: AfterActionTakenMessage):
    print(f'Agent: {agent.name}, Action taken: {message}')
    return message


if __name__ == '__main__':
    autono_agent = Agent(abilities=[calculator, write_file], brain=get_openai_model(), name='Autono', personality=Personality.INQUISITIVE)
    radius = '(10.01 * 10.36 * 3.33 / 2 * 16)'  # 2762.663904
    pi = 3.14159
    output_file = 'result.txt'
    request = f"Here is a sphere with radius of {radius} cm and pi here is {pi}, find the area and volume respectively then write the results into a file called '{output_file}'."
    result = autono_agent.assign(request).just_do_it(BeforeActionTaken(before_action_taken), AfterActionTaken(after_action_taken))  # area = 95910378.2949379, volume = 88322713378.13666
    print(f'Result: {result}')
