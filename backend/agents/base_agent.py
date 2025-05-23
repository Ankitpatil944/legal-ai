from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from groq import Groq
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
import logging
from datetime import datetime

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%H:%M:%S'
)

class BaseAgent(ABC):
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.llm = ChatGroq(
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3-8b-8192"
        )
        self.memory: Dict[str, Any] = {}
        self.agent_name = self.__class__.__name__
        self.logger = logging.getLogger(self.agent_name)

    def log_activity(self, message: str, status: str = "INFO") -> None:
        """Log agent activity with timestamp and formatting."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"\n[{timestamp}] \033[1m{self.agent_name}\033[0m: {message}"
        
        if status == "SUCCESS":
            formatted_message = f"{formatted_message} \033[92m✓\033[0m"
        elif status == "ERROR":
            formatted_message = f"{formatted_message} \033[91m✗\033[0m"
        elif status == "WARNING":
            formatted_message = f"{formatted_message} \033[93m!\033[0m"
        
        print(formatted_message)
        self.logger.info(message)

    @abstractmethod
    async def process(self, document_text: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Process the document text and return results.
        Must be implemented by all subclasses.
        """
        pass

    async def _call_llm(self, prompt: str, temperature: float = 0.7) -> str:
        """
        Make a call to the Groq LLM with the given prompt.
        """
        try:
            self.log_activity(f"Calling LLM with prompt: {prompt[:100]}...")
            response = self.llm.invoke(prompt)
            self.log_activity("LLM call completed successfully", "SUCCESS")
            return response.content
        except Exception as e:
            self.log_activity(f"Error calling LLM: {str(e)}", "ERROR")
            raise Exception(f"Error calling LLM: {str(e)}")

    def store_in_memory(self, key: str, value: Any) -> None:
        """
        Store a value in the agent's memory.
        """
        self.memory[key] = value
        self.log_activity(f"Stored value in memory for key: {key}")

    def get_from_memory(self, key: str) -> Optional[Any]:
        """
        Retrieve a value from the agent's memory.
        """
        value = self.memory.get(key)
        if value is not None:
            self.log_activity(f"Retrieved value from memory for key: {key}")
        return value

    def clear_memory(self) -> None:
        """
        Clear the agent's memory.
        """
        self.memory.clear()
        self.log_activity("Memory cleared") 