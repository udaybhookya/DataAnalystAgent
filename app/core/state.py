from typing import Dict, Any, List

class ReportState:
    """
    This class represents the state of the report generation process.
    It contains all the necessary information to generate a report.
    """
    def __init__(self, input_context: Dict[str, Any]):
        """
        Initializes the state object from a dictionary.
        
        MODIFICATION: All assignments now use `self.` to create instance attributes.
        This ensures the attributes are correctly attached to the object and can be
        accessed later, fixing the 'has no attribute' error.
        """
        self.llm_model = input_context.get("llm_model")
        self.processed_tables = input_context.get("processed_tables", {})
        self.plots_path = input_context.get("plots_path", "")
        self.pdf_path = input_context.get("pdf_path")
        
        # Initialize other state attributes with default empty values
        self.analytics_plan: Dict[str, Any] = {}
        self.analytics_code: List[Dict[str, str]] = []
        self.query_results: List[Dict[str, Any]] = []
        self.report_content: List[Dict[str, Any]] = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert the ReportState instance to a dictionary for the workflow."""
        return {
            "llm_model": self.llm_model,
            "processed_tables": self.processed_tables,
            "analytics_plan": self.analytics_plan,
            "analytics_code": self.analytics_code,
            "query_results": self.query_results,
            "report_content": self.report_content,
            "plots_path": self.plots_path,
            "pdf_path": self.pdf_path,
        }

