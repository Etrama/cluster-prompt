# Copyright 2022 PAL Authors. All rights reserved.
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

import io
import signal
from contextlib import redirect_stdout
from typing import Any, Callable, List, Optional
from collections import Counter

from .runtime import GenericRuntime
from .backend import call_gpt, call_chat_gpt, call_chat_gpt_self_consistency

import multiprocessing.pool
import functools

def timeout(max_timeout):
    """Timeout decorator, parameter in seconds."""
    def timeout_decorator(item):
        """Wrap the original function."""
        @functools.wraps(item)
        def func_wrapper(*args, **kwargs):
            """Closure for function."""
            pool = multiprocessing.pool.ThreadPool(processes=1)
            async_result = pool.apply_async(item, args, kwargs)
            # raises a TimeoutError if execution exceeds max_timeout
            return async_result.get(max_timeout)
        return func_wrapper
    return timeout_decorator

# This is useless in Windows, so we comment it out.
# class timeout:
#     def __init__(self, seconds=1, error_message='Timeout'):
#         self.seconds = seconds
#         self.error_message = error_message
#     def timeout_handler(self, signum, frame):
#         raise TimeoutError(self.error_message)
#     def __enter__(self):
#         signal.signal(signal.SIGALRM, self.timeout_handler)
#         signal.alarm(self.seconds)
#     def __exit__(self, type, value, traceback):
#         signal.alarm(0)


class TextInterface:
    
    def __init__(
        self,
        model: str = 'code-davinci-002',
        answer_prefix: str = 'The answer is:',
        stop: str = '\n\n\n',
        extract_answer: Optional[Callable[[str], Any]] = None,
    ):
        self.history = []
        self.answer_prefix = answer_prefix
        self.extract_answer_fn = extract_answer
        self.stop = stop
        self.model = model
        
    def clear_history(self):
        self.history = []
    
    def extract_answer(self, gen: str):
        if self.extract_answer_fn:
            return self.extract_answer_fn (gen)
        last_line = gen.strip().split('\n')[-1]
        return last_line[len(self.answer_prefix):].strip()
    
    def run(self, prompt, temperature=0.0, top_p=1.0, majority_at=None, max_tokens=512):
        gen = call_gpt(prompt, model=self.model, stop=self.stop, 
            temperature=temperature, top_p=top_p, max_tokens=max_tokens, majority_at=majority_at)
        self.history.append(gen)
        return self.extract_answer(gen)
        

class ProgramInterface:
    
    def __init__(
        self,
        model: str = 'code-davinci-002',
        runtime: Optional[Any] = None,
        stop: str = '\n\n',
        get_answer_symbol: Optional[str] = None,
        get_answer_expr: Optional[str] = None,
        get_answer_from_stdout: bool = False,
        verbose: bool = False
    ) -> None:

        self.model = model
        self.runtime = runtime if runtime else GenericRuntime()
        self.history = []
        self.stop = stop
        self.answer_symbol = get_answer_symbol
        self.answer_expr = get_answer_expr
        self.get_answer_from_stdout = get_answer_from_stdout
        self.verbose = verbose
        
    def clear_history(self):
        self.history = []
    
    def process_generation_to_code(self, gens: str):
        return [g.split('\n') for g in gens]
    
    def generate(self, prompt: str, temperature: float =0.0, top_p: float =1.0, 
            max_tokens: int =512, majority_at: int =None, ):
        gens = call_gpt(prompt, model=self.model, stop=self.stop, 
            temperature=temperature, top_p=top_p, max_tokens=max_tokens, majority_at=majority_at, )
        if self.verbose:
            print(gens)
        code = self.process_generation_to_code(gens)
        self.history.append(gens)
        return code
    
    @timeout(60.0)
    def execute(self, code: Optional[List[str]] = None):
        # code = code if code else self.code
        if self.get_answer_from_stdout:
            program_io = io.StringIO()
            with redirect_stdout(program_io):
                self.runtime.exec_code('\n'.join(code))
            program_io.seek(0)
            return program_io.readlines()[-1]
        elif self.answer_symbol:
            self.runtime.exec_code('\n'.join(code))
            return self.runtime._global_vars[self.answer_symbol]
        elif self.answer_expr:
            self.runtime.exec_code('\n'.join(code))
            return self.runtime.eval_code(self.answer_expr)
        else:
            self.runtime.exec_code('\n'.join(code[:-1]))
            return self.runtime.eval_code(code[-1])
    
    # def run(self, prompt: str, time_out: float =10, temperature: float =0.0, top_p: float =1.0, 
    #         max_tokens: int =512, majority_at: int =None):
    #     code_snippets = self.generate(prompt, majority_at=majority_at, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        
    #     results = []
    #     for code in code_snippets:
    #         with timeout(time_out):
    #             try:
    #                 exec_result = self.execute(code)
    #             except Exception as e:
    #                 print(e)
    #                 continue
    #             results.append(exec_result)
    #     counter = Counter(results)
    #     return counter.most_common(1)[0][0]
    
    
SYSTEM_MESSAGES = 'You are a helpful python programmer. Use comments to comment out non-executable lines and keep code separate from text.'
class ProgramChatInterface(ProgramInterface):
    def __init__(self, *args, system_message: str = SYSTEM_MESSAGES, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_message = system_message
        
    def generate(self, prompt: str, temperature: float = 0, top_p: float = 1, max_tokens: int = 512):
        messages =[{'role': 'system', 'content': self.system_message}, {'role': 'user', 'content': prompt}]
        gen = call_chat_gpt(messages, model=self.model, stop=self.stop, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        # print(f"generated in chat interface is: {gen}")
        if self.verbose:
            print(gen)
        self.history.append(gen)
        # print(f"gen inside PCI interface is: {gen}")
        return self.process_generation_to_code(gen)
        
    def process_generation_to_code(self, gens: str):
        if '```python' in gens:
            gens = gens.split('```python')[1].split('```')[0]
        elif '```' in gens:
            gens = gens.split('```')[1].split('```')[0]
            
        return gens.split('\n')
    
    def run(self, prompt: str, time_out: float = 10, temperature: float = 0, top_p: float = 1, max_tokens: int = 512):
        code = self.generate(prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens)
        # print(f"code inside run: {code}")
        # print(f"code type inside run: {type(code)}")
        # with timeout(time_out):
        results = ""
        code_errors = ""
        try:
            exec_result = self.execute(code)
            # print(f"exec_result inside run: {exec_result}")
            results = exec_result #this has the numerical value of the result
            # code_errors.append(None)
            # return exec_result
        except TimeoutError as te:
            print(te)
            code_errors = str(te)
            # results = None
        except Exception as e:
            print(e)
            code_errors = str(e)
            # results = None
        return results, code_errors


class ProgramSelfConsitencyChatInterface(ProgramInterface):
    def __init__(self, *args, system_message: str = SYSTEM_MESSAGES, **kwargs):
        super().__init__(*args, **kwargs)
        self.system_message = system_message

    def generate(self, prompt: str, temperature: float = 0.7, top_p: float = 0.95, max_tokens: int = 512, majority_at: int =1, ):
        messages = [{'role': 'system', 'content': self.system_message}, {'role': 'user', 'content': prompt}]
        gens = call_chat_gpt_self_consistency(messages, temperature=temperature, top_p=top_p, max_tokens=max_tokens, majority_at=majority_at)
        code_snippets = [self.process_generation_to_code(gen) for gen in gens]
        self.history.append(code_snippets)
        return code_snippets

    def process_generation_to_code(self, gens: str):
        if '```python' in gens:
            gens = gens.split('```python')[1].split('```')[0]
        elif '```' in gens:
            gens = gens.split('```')[1].split('```')[0]

        return gens.split('\n')

    def run(self, prompt: str, temperature: float = 0.7, top_p: float = 0.95, max_tokens: int = 512, majority_at: int =40, ):
        code_snippets = self.generate(prompt, temperature=temperature, top_p=top_p, max_tokens=max_tokens, majority_at=majority_at)

        results = []
        code_errors = []
        for code in code_snippets:
            try:
                exec_result = self.execute(code)
                results.append(exec_result)
                code_errors.append("None")
            except TimeoutError as te:
                print(te)
                code_errors.append(str(te))
            except Exception as e:
                print(e)
                code_errors.append(str(e))

        return results, code_errors

