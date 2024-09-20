import os
from datetime import datetime
from typing import Dict, List

from langchain.output_parsers import PydanticOutputParser
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from models import QueryAnalysisOutput
from utils import read_prompt


class DatabaseChatbot:
    def __init__(self, db_url):
        """
        Initialize the DatabaseChatbot with a SQLite database path.

        Args:
            db_url (str): Database connection url
        """
        self.debug = True if os.getenv("DEBUG") == "1" else False
        llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"), temperature=0)
        self.conversation_parser = PydanticOutputParser(
            pydantic_object=QueryAnalysisOutput
        )
        conversation_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    read_prompt("conversation_query"),
                ),
                (
                    "human",
                    "Analyze this conversation and provide the results in the specified format:\n\n{conversation}\n\n{format_instructions}",
                ),
            ]
        )

        self.conversation_chain = conversation_prompt | llm | self.conversation_parser

        ro_db_url = (
            db_url + "?mode=ro"
            if "mode=ro" not in db_url and "sqlite" in db_url
            else db_url
        )
        db = SQLDatabase.from_uri(ro_db_url)
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        system_message = SystemMessage(content=read_prompt("database_chat"))
        tools = toolkit.get_tools()

        self.agent = create_react_agent(
            llm, tools, state_modifier=system_message, debug=self.debug
        )

    def query(self, user_query: str):
        """
        Executes the user query and returns the final response

        Args:
            user_query (str): Question from the user
        """

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_added_query = user_query + f"\n Current Date and Time: {timestamp}"
        r = self.agent.invoke(
            {"messages": [HumanMessage(content=timestamp_added_query)]},
            {"recursion_limit": 100},
        )
        return r["messages"][-1].content

    def extract_user_query(self, messages=List[Dict[str, str]]) -> QueryAnalysisOutput:
        """
        Extracts the user query from the conversation

        Args:
            messages: Conversation History
        """

        conversation_str = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in messages]
        )

        r = self.conversation_chain.invoke(
            {
                "conversation": conversation_str,
                "format_instructions": self.conversation_parser.get_format_instructions(),
            }
        )
        return r
