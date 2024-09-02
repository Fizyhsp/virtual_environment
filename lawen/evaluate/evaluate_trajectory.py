import json

from langchain import PromptTemplate

from typing import Any
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain


class LLMAgentEvaluator:
    """利用LLM评分"""

    def __init__(self, model_name, temperature, api_base="https://api.chatanywhere.cn/v1",
                 api_key="sk-kJdjn5gp7aCpofbFQJdqL4GKE153kc13URPePANT0OU1Ukft") -> None:

        self.llm = ChatOpenAI(openai_api_base=api_base, temperature=temperature,
                              openai_api_key=api_key,
                              model_name=model_name)
        with open('prompts/templates/evaluate.txt', 'r') as f:
            template = f.read()
        prompt = PromptTemplate(template=template, input_variables=["task", "trajectory", "reflection", "previous_reflection"],
                                template_format="jinja2")
        self.evaluation_chain = LLMChain(prompt=prompt, llm=self.llm)

    def _evaluate(
            self,
            task,
            trajectory,
            memory,
            **kwargs: Any,
    ) -> dict:
        try:
            response = self.evaluation_chain.run(dict(trajectory=trajectory, task=task, reflection = memory[-1], previous_reflection=memory[:-1]), **kwargs)
        except Exception as e:
            try:
                print(e)
                trajectory = trajectory[:int(len(trajectory) * 0.5)]
                memory = memory[:int(len(memory) * 0.5)]
                response = self.evaluation_chain.run(dict(trajectory=trajectory, task=task, reflection = memory[-1], previous_reflection=memory[:-1]), **kwargs)
            except Exception as e:
                print(e)
                trajectory = trajectory[:int(len(trajectory) * 0.2)]
                memory = memory[:int(len(memory) * 0.5)]
                response = self.evaluation_chain.run(dict(trajectory=trajectory, task=task, reflection = memory[-1], previous_reflection=memory[:-1]), **kwargs)
        try:
            res = json.loads(response)
        except Exception as e:
            print(e)
            res = self.reformat(response)
        return res

    def reformat(self, input):
        template = """
            Please reformat the [Input] to follow json [Format]:

            [Input]
            {{ input }}

            [Format]
            {
            "task_achieving":
            {
                "i": {"score": "score", "reason": "reason},
                "ii": {"score": "score", "reason": "reason},
                ...
            }
           "similarity":
            {
                "i": {"score": "score", "reason": "reason},
                ...
            },
            "quality":
            {
                "i": {"score": "score", "reason": "reason},
                ...
            }
            [Reformat]
        }
        """
        prompt = PromptTemplate(template=template, input_variables=["input"], template_format="jinja2")
        llm_chain = LLMChain(prompt=prompt, llm=self.llm)
        response = llm_chain.predict(input=input)
        json_res = json.loads(response)
        return json_res


class MetricEvaluator:
    """利用最长公共子序列(LCSS)，计算轨迹相似度"""

    def __init__(self):
        self.list_lcss = []

    def lcs(self, traj1, traj2):
        len1 = len(traj1)
        len2 = len(traj2)
        res = [[0 for i in range(len2 + 1)] for j in range(len1 + 1)]
        flag = [[0 for i in range(len2 + 1)] for j in range(len1 + 1)]
        for i in range(len1):
            for j in range(len2):
                if traj1[i] == traj2[j]:
                    res[i + 1][j + 1] = res[i][j] + 1
                    flag[i + 1][j + 1] = 's1'
                elif res[i + 1][j] > res[i][j + 1]:
                    res[i + 1][j + 1] = res[i + 1][j]
                    flag[i + 1][j + 1] = 's2'
                else:
                    res[i + 1][j + 1] = res[i][j + 1]
                    flag[i + 1][j + 1] = 's3'
        return flag

    def printLcs(self, flag, traj, len1, len2):
        if len1 == 0 or len2 == 0:
            return
        if flag[len1][len2] == 's1':
            self.printLcs(flag, traj, len1 - 1, len2 - 1)
            self.list_lcss.append(traj[len1-1])
        elif flag[len1][len2] == 's2':
            self.printLcs(flag, traj, len1, len2 - 1)
        else:
            self.printLcs(flag, traj, len1 - 1, len2)

    def _evaluate_agent_trajectory(self, trajectory, gt_trajectory):
        flag = self.lcs(trajectory, gt_trajectory)
        self.printLcs(flag, trajectory, len(trajectory), len(gt_trajectory))

        return len(self.list_lcss)/min(len(trajectory), len(gt_trajectory))