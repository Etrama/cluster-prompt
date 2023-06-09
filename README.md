Setup your OpenAI key as an environment variable called: OPENAI_API_KEY (variable name), the variable value will be your API key.


## Installation
Clone this repo and install with `pip`.
```
git clone https://github.com/Etrama/PAL_v2.git
pip install -e ./pal
```

Before running the scripts, set the OpenAI key,
```export OPENAI_API_KEY='sk-...'```
## Interactive Usage
The core components of the `pal` package are the Interface classes. Specifically, `ProgramInterface` connects the LLM backend, a Python backend and user prompts.
```
import pal
from pal.prompt import math_prompts

interface = pal.interface.ProgramInterface(
  model='code-davinci-002',
  stop='\n\n\n', # stop generation str for Codex API
  get_answer_expr='solution()' # python expression evaluated after generated code to obtain answer 
)

question = 'xxxxx'
prompt = math_prompts.MATH_PROMPT.format(question=question)
answer = interface.run(prompt)
```
Here, the `interface` 's `run`  method will run generation with the OpenAI API, run the generated snippet and then evaluate `get_answer_expr` (here `solution()`) to obtain the final answer.  

User should set `get_answer_expr` based on the prompt.

## Inference Loop
We provide simple inference loops in the `scripts/` folder.
```
mkdir eval_results
python scripts/{colored_objects|gsm|date_understanding|penguin}_eval.py
``` 

We have a beta release of a **ChatGPT** dedicated script for math reasoning.
```
python scripts/gsm_chatgpt.py
``` 

For running bulk inference, we used the generic prompting library [prompt-lib](https://github.com/madaan/prompt-lib) and recommend it for running CoT inferenence on all tasks used in our work.

## Results

<img width="831" alt="image" src="https://user-images.githubusercontent.com/15002544/202954755-bf89aab6-6467-436e-98d6-2ca378a20116.png">

<img width="1166" alt="image" src="https://user-images.githubusercontent.com/15002544/202954780-7e1221f1-3008-46d9-877b-b26df9f98d66.png">

<img width="597" alt="image" src="https://user-images.githubusercontent.com/15002544/202954797-68e8d45d-3435-4abf-96e4-f10371b55e38.png">

For the complete details of the results, see the [paper](https://arxiv.org/pdf/2211.10435.pdf) .

## Citation
```
@article{gao2022pal,
  title={PAL: Program-aided Language Models},
  author={Gao, Luyu and Madaan, Aman and Zhou, Shuyan and Alon, Uri and Liu, Pengfei and Yang, Yiming and Callan, Jamie and Neubig, Graham},
  journal={arXiv preprint arXiv:2211.10435},
  year={2022}
}
```
# PAL_v2
