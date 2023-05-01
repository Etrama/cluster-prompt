# Copyright 2023 PAL Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import copy
import json
import argparse
import tqdm
import os
import re

from pal import interface
from pal.prompt import math_prompts
from datetime import datetime
from pal.core.backend import call_chat_gpt


parser = argparse.ArgumentParser()
parser.add_argument('--append', action='store_true')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--dataset', default='reduced_gsm', type=str)
parser.add_argument('--model', default='gpt-3.5-turbo', type=str)
parser.add_argument('--temperature', default=0.0, type=float)
parser.add_argument('--top_p', default=1.0, type=float)
parser.add_argument('--max_tokens', default=512, type=int)
args = parser.parse_args()

DATA_PATH = f'datasets/{args.dataset}.jsonl'
FILE_NAME = datetime.now().strftime("%d-%m-%Y_%H%M%S") + "_" + os.getlogin() + "_" + args.dataset
OUTPUT_PATH = f'eval_results/{FILE_NAME}.chat.jsonl'
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)


examples = list(map(json.loads, open(DATA_PATH)))


if args.append:
    lines = open(OUTPUT_PATH).readlines()
    num_skip_exps = len(lines)
    scores = [x['score'] for x in map(json.loads, lines)]
else:
    num_skip_exps = 0
    scores = []

with open(OUTPUT_PATH, 'a' if args.append else 'w') as f:
    pbar = tqdm.tqdm(examples[num_skip_exps:], initial=num_skip_exps, total=len(examples))
    for x in pbar:
        question = x['input']
        result = copy.copy(x)
        type_error = ''
        try:
            #prompt = math_prompts.COMPLEX_COT.format(question=question)
            prompt1 = math_prompts.LEAST_TO_MOST_STAGE1.format(question=question)
            messages = [{'role': 'system', 'content': math_prompts.SYSTEM_L2M_STAGE1_MESSAGE},
                        {'role': 'user', 'content': prompt1}]
            chain1 = call_chat_gpt(messages, max_tokens=512)

            subquestions = re.findall("(?<= \")(.*?)(?=\")", chain1)
            subquestions.append(subquestions.pop(0))
            prompt = math_prompts.LEAST_TO_MOST_STAGE2_V2.format(question=question)
            for q in subquestions:
                prompt = prompt + f"\n{q}"

            prompt = prompt + f"\n\nQ:"
            messages = [{'role': 'system', 'content': math_prompts.SYSTEM_L2M_STAGE2_MESSAGE},
                        {'role': 'user', 'content': prompt}]
            chain = call_chat_gpt(messages, max_tokens=512)

            ans = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", chain)[-1] # extracts number
            ans = re.sub("[^\d\.\-]", "", ans) #removes commas ex: 8,000,234.1234

            ans = float(ans)
            score = 1 if abs(ans - x['target']) < 1e-3 else 0
        except Exception as e:
            print(e)
            ans = ''
            score = 0
            type_error = str(e)
        scores.append(score)
        
        result['answer'] = ans
        result['score'] = score
        result['generation'] = chain
        result["type_error"] = type_error if type_error else ""
        f.write(json.dumps(result) + '\n')
        f.flush()


acc = sum(scores) / len(scores)
print(f'Accuracy - {acc}')

os.rename(OUTPUT_PATH, f'eval_results/{FILE_NAME}_acc{round(acc*100, 2)}.chat.jsonl')

