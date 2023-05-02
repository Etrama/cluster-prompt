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
from pal.core.backend import call_chat_gpt, call_chat_gpt_self_consistency
from collections import Counter


parser = argparse.ArgumentParser()
parser.add_argument('--append', action='store_true')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--dataset', default='reduced_gsm', type=str)
parser.add_argument('--model', default='gpt-4', type=str)
parser.add_argument('--temperature', default=0.7, type=float)
parser.add_argument('--top_p', default=0.95, type=float)
parser.add_argument('--max_tokens', default=512, type=int)
parser.add_argument('--majority_at', default=20, type=int)
args = parser.parse_args()

DATA_PATH = f'datasets/{args.dataset}.jsonl'
FILE_NAME = datetime.now().strftime("%d-%m-%Y_%H%M%S") + "_" + os.getlogin() + "_" + args.dataset
OUTPUT_PATH = f'eval_results/{FILE_NAME}.chat.jsonl'
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)


examples = list(map(json.loads, open(DATA_PATH)))

itf = interface.ProgramSelfConsitencyChatInterface(
    stop=None,
    get_answer_expr='solution()',
    model=args.model,
    verbose=args.verbose,
    system_message=math_prompts.MATH_CHAT_BETA_SYSTEM_MESSAGE,
)

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

        cp_gens = []
        pal_results = []
        cp_results = []
        code_errors = []
        type_error = ""
        try:
            prompt = math_prompts.COMPLEX_COT.format(question=question)
            messages =[{'role': 'system', 'content': math_prompts.SYSTEM_COMPLEX_COT_MESSAGE}, {'role': 'user', 'content': prompt}]
            cp_gens = call_chat_gpt_self_consistency(
                messages,
                model=args.model,
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens,
                majority_at=args.majority_at
            )

            cp_results = [re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", gen)[-1] for gen in cp_gens]
            cp_results = [re.sub("[^\d\.\-]", "", gen) for gen in cp_results]

            pal_results, code_errors = itf.run(
                math_prompts.MATH_CHAT_BETA_PROMPT.format(question=question),
                temperature=args.temperature,
                top_p=args.top_p,
                max_tokens=args.max_tokens,
                majority_at=args.majority_at
            )

            raw_results = []
            for answer in pal_results + cp_results:
                try:
                    raw_results.append(float(answer))
                except:
                    pass

            results = Counter(raw_results)
            ans = results.most_common(1)[0][0]
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
        result['pal_generation'] = itf.history
        result["pal_code_error"] = code_errors
        result['cp_generation'] = cp_gens
        result['pal_results'] = pal_results
        result['cp_results'] = cp_results
        result['final_result_list'] = raw_results
        result["type_error"] = type_error
        f.write(json.dumps(result) + '\n')
        
        itf.clear_history()
        f.flush()


acc = sum(scores) / len(scores)
print(f'Accuracy - {acc}')

os.rename(OUTPUT_PATH, f'eval_results/{FILE_NAME}_acc{round(acc*100, 2)}.chat.jsonl')

