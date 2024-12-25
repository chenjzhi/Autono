import json
import logging

from langchain_core.language_models import BaseChatModel

from ceo.ability.ability import Ability
from ceo.prompt.prompt import Prompt

log = logging.getLogger('ceo.prompt')


class AnalyserPrompt(Prompt):
    def __init__(self, query: str, prev_results: list, action: Ability, ext_context: str = ''):
        self.action = action
        prev_results_str = str()
        if len(prev_results) > 0:
            prev_results_str += '\n'
        for result in prev_results:
            prev_results_str += f'{result};\n'
        prompt = {
            "precondition": "Below is the <tool(ability)> you can use (you can only use this tool(ability)). "
                            f'And there is a user query: "{query}"',
            "objective": "What you need to do is to generate values of parameters of the <tool(ability)> "
                         "to achieve <user query>",
            "hints": {
                "to_generate_parameters": "Parameters are described in <tool(ability)>, "
                                          "values of params are supposed to be generated by you, "
                                          "strictly abide by the parameter name and type.",
                "no_nonexistent_parameters": "You must not generate any nonexistent parameter, "
                                             "look carefully at parameters "
                                             "which are only described in <tool(ability)>.",
                "no_redundant_info": "With no any redundant information, only a json which provides parameters."
            },
            "tool(ability)": action.to_dict(),
            "output_format": "json",
            "output_example": '{"param_1.name": "value_for_param_1", "param_2.name": "value_for_param_2"}'
        }
        if len(prev_results_str) != 0:
            prompt['action_history (previous actions)'] = prev_results_str
            prompt['instruction_for_action_history'] = ("Generate response according to previous actions "
                                                        "performed by you.")
            prompt['hint_for_action_history'] = ("What <action_history> has shown is what you have done until now."
                                                 "What you need to do now is to think seriously "
                                                 "what you have not done yet "
                                                 "according to the <action_history> and <user query>."
                                                 "You are going to plan your next moves after <action_history>.")
        else:
            prompt['hint_for_first_move'] = 'This is your first step, you are starting to think.'
        prompt = json.dumps(prompt, ensure_ascii=False)
        super().__init__(prompt, ext_context)
        log.debug(f'AnalyserPrompt: {self.prompt}')

    def invoke(self, model: BaseChatModel) -> tuple[Ability, dict]:
        result = model.invoke(self.prompt).content
        if not result.startswith('{'):
            result = result[result.find('{'):]
        if not result.endswith('}'):
            result = result[:result.rfind('}') + 1]
        param = json.loads(result)
        return self.action, param
