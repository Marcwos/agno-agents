from agno.agent import Agent
from agno.models.groq import Groq
from agno.playground import Playground
from agno.storage.sqlite import SqliteStorage
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.yfinance import YFinanceTools
from fastapi.middleware.cors import CORSMiddleware

agent_storage: str = "tmp/agents.db"
GROQ_APIKEY = "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"


web_agent = Agent(
    name="Marcwos Agent",
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_APIKEY),
    tools=[DuckDuckGoTools()],
    instructions=["Always include sources"],
    # Store the agent sessions in a sqlite database
    storage=SqliteStorage(table_name="web_agent", db_file=agent_storage),
    # Adds the current date and time to the instructions
    add_datetime_to_instructions=True,
    # Adds the history of the conversation to the messages
    add_history_to_messages=True,
    # Number of history responses to add to the messages
    num_history_responses=5,
    # Adds markdown formatting to the messages
    markdown=True,
)

finance_agent = Agent(
    name="Josue Agent",
    model=Groq(id="llama-3.3-70b-versatile", api_key=GROQ_APIKEY),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True, company_news=True)],
    instructions=["Always use tables to display data"],
    storage=SqliteStorage(table_name="finance_agent", db_file=agent_storage),
    add_datetime_to_instructions=True,
    add_history_to_messages=True,
    num_history_responses=5,
    markdown=True,
)

playground_app = Playground(agents=[web_agent, finance_agent])
app = playground_app.get_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins="https://frontagentexam-585785395737.europe-west1.run.app/",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)