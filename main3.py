from agents import Agent, Runner, function_tool, RunContextWrapper, trace
import asyncio
from pydantic import BaseModel
from connection import config
import rich


# Bank Account model
class BankAccount(BaseModel):
    account_number: str | int
    customer_name: str
    account_balance: float
    account_type: str


# Tool to return bank account profile
@function_tool
async def bank_account_profile(wrapper: RunContextWrapper[BankAccount]):
    """
    Returns the bank account profile from the provided context.
    """
    return wrapper.context  


# Bank account object
bank = BankAccount(
    account_number="ACC-789456",
    customer_name="Fatima Khan",
    account_balance=75500.50,
    account_type="Savings"
)


# Bank Account Agent
Account_agent = Agent(
    name="Bank Account Agent",
    instructions=(
        "You are a helpful bank account assistant. "
        "You have access to a bank account's profile containing the account number, customer name, balance, and type. "
        "Always answer using the provided account profile context. "
        "If the user asks for all account details, list each detail on a separate line in the format:\n"
        "Account Number: <value>\n"
        "Customer Name: <value>\n"
        "Account Balance: <value>\n"
        "Account Type: <value>.\n"
        "Do not make up information that is not in the profile."
    ),
    tools=[bank_account_profile]
)
 

# Main function
async def main():
    with trace("Bank Account Agent"):
        result = await Runner.run(
            Account_agent,
            "Give me all account details",
            run_config=config,
            context=bank
        )
        rich.print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
