from langchain_google_genai import ChatGoogleGenerativeAI

class LLMLoader:
    def __init__(self, google_api_key: str):
        self.google_api_key = google_api_key

    def load_google_model_pro(self, temperature=0):
        """_summary_

        Args:
            temperature (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=temperature,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            google_api_key=self.google_api_key
        )

    def load_google_model_flash(self, temperature=0):
        """_summary_

        Args:
            temperature (int, optional): _description_. Defaults to 0.

        Returns:
            _type_: _description_
        """
        
        return ChatGoogleGenerativeAI(
            model="models/gemini-2.0-flash",
            temperature=temperature,
            max_tokens=None,
            timeout=None,
            max_retries=2,
            google_api_key=self.google_api_key
        )