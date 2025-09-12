import pandas as pd
import io
import sys
from ..state import ReportState
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re

with open("prompts/code_correction_prompt_template.txt", "r") as f:
        code_correction_prompt_template = f.read()

def clean_python_code(code_string: str) -> str:
    """
    Cleans a string to ensure it's valid Python code by removing markdown fences
    and other non-code text.
    """
    # Remove markdown code blocks
    code_string = re.sub(r'```python\n', '', code_string)
    code_string = re.sub(r'```', '', code_string)
    
    # Strip leading/trailing whitespace
    return code_string.strip()

def code_execution_node(state: ReportState) -> dict:
    """
    Executes the generated python code for each analytic.
    If an error occurs, it attempts to correct the code and rerun it.
    """
    print("\n==========================================")
    print("I am in the code execution node ... ")
    print("============================================")

    llm_model = state['llm_model']
    analytics_code = state['analytics_code']
    processed_tables = state['processed_tables']
    query_results = []
    
    # # Prompt template for code correction
    # code_correction_prompt_template = """
    # You are an expert python programmer. The following python code, designed for data analysis with pandas, resulted in an error.
    
    # Original Code:
    # ```python
    # {code}
    # ```
    
    # Error Message:
    # {error}
    
    # Please correct the code to fix the error. The corrected code should be a single Python function.
    # - The function must be named `analyze_data`.
    # - It must take a pandas DataFrame `df` as input.
    # - It should return the result of the analysis (e.g., a string, a number, a DataFrame, or a plot file path).
    # - If you create a plot, save it to a file (e.g., 'plot.png') and return the filename. Use matplotlib for plotting.
    
    # Provide only the corrected Python code, without any explanations or markdown formatting.
    # """
    
    code_correction_prompt = PromptTemplate(
        input_variables=["code", "error"],
        template=code_correction_prompt_template
    )
    
    correction_chain = code_correction_prompt | llm_model | StrOutputParser()
    
    max_retries = 4
    for idx, analytic in enumerate(analytics_code):
        # Clean the initial code before the first attempt
        code_to_execute = clean_python_code(analytic['code'])
        analysis_name = analytic['analysis_name']
        
        for attempt in range(max_retries):
            print(f"Executing code for '{analysis_name}' (Attempt {attempt + 1}/{max_retries})")

            try:
                # Get the dataframe for the analysis
                # Assuming the table name is consistent across analytics for now
                table_name = state['analytics_plan']['analytics_suggested'][idx]['table_name']
                df = processed_tables[table_name].df.copy()

                # Prepare a dictionary for the execution context
                local_scope = {'df': df}

                # Execute the function definition
                exec(code_to_execute, globals(), local_scope)

                # Call the function
                result = local_scope['analyze_data'](df)
                
                query_results.append({
                    "analysis_name": analysis_name,
                    "result": result
                })
                print(f"Successfully executed code for: {analysis_name}")
                break # Exit retry loop on success

            except Exception as e:
                error_message = str(e)
                print(f"Error executing code for {analysis_name}: {error_message}")
                
                if attempt < max_retries - 1:
                    print("Attempting to correct the code...")
                    corrected_code_raw = correction_chain.invoke({
                        "code": code_to_execute,
                        "error": error_message
                    })
                    # Clean the corrected code before the next attempt
                    code_to_execute = clean_python_code(corrected_code_raw)
                    # Update the code in the state for the next attempt
                    state['analytics_code'][idx]['code'] = code_to_execute
                    print("Corrected Code:")
                    print(code_to_execute)
                else:
                    print(f"All {max_retries} attempts failed for {analysis_name}.")
                    query_results.append({
                        "analysis_name": analysis_name,
                        "result": f"Error after {max_retries} attempts: {error_message}"
                    })

    state['query_results'] = query_results

    return state
