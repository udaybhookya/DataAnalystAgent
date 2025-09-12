from ..state import ReportState
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

with open("prompts/data_understanding_prompt.txt", "r") as f:
        data_understanding_template = f.read()

def data_understanding_node(state: ReportState) -> ReportState:

    """
    This node is responsible for understanding the data.
    It will load the data, analyze its schema, and prepare it for further processing.
    """
    
    print("\n==========================================")
    print("I am in the data understanding node ... ")
    print("============================================")

    print(state)
    llm_model = state['llm_model']
    processed_tables = state['processed_tables'] 

    tables_list = processed_tables.keys()

    input_table_schema = ""

    for one_table in tables_list:

        one_table_schema = processed_tables[one_table].schema

        input_table_schema += f"Table name: {one_table}\n"
        input_table_schema += f"Table Description: {one_table_schema['table_description'].unique()[0]}\n\n"
        input_table_schema += f"Columns description of table {one_table}:\n"

        for idx, one_row in one_table_schema.iterrows():
            input_table_schema += f"Column name: {one_row['column_name']}\n"
            input_table_schema += f"Column description: {one_row['column_description']}\n"
            input_table_schema += f"Column type: {one_row['data_type']}\n\n"

        input_table_schema += "\n\n"

    # print(input_table_schema)

    data_understanding_prompt = PromptTemplate(
        input_variables=["input_table_schema"],
        template =  data_understanding_template)

    parser = JsonOutputParser()
    print(data_understanding_prompt.template)
    print(input_table_schema)
    analytics_plan_chain = data_understanding_prompt | llm_model | parser
    analytics_plan_json = analytics_plan_chain.invoke({"input_table_schema": input_table_schema})

    state["analytics_plan"] = analytics_plan_json 

    print("Analytics plan generated successfully.")

    # Display the analytics plan
    print("Chain of thought:")
    print(analytics_plan_json['chain_of_thought'])

    for one_plan in analytics_plan_json['analytics_suggested']:
        
        _extracted_from_data_understanding_node_58(one_plan)
        
    return state

def _extracted_from_data_understanding_node_58(one_plan):
    """
    Prints the details of a single analytics plan in a formatted manner.
    Displays the analysis type, name, table, columns, and description for the provided plan.

    Args:
        one_plan (dict): A dictionary containing details of an analytics plan, including analysis type, name, table, columns, and description.
    """
    print(f"Analytics Type: {one_plan['analysis_type']}")
    print(f"Analytics Name: {one_plan['analysis_name']}")
    print(f"Table: {one_plan['table_name']}")
    print(f"Columns: {', '.join(one_plan['column_names'])}")
    print(f"Description: {one_plan['description']}")
    print("--------------------------------------------------")