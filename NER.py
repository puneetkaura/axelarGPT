import json

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator

from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI


class AxelarInput(BaseModel):
	srcChain: str
	destinationChain: str
	token: str
	amount: int


USER_MSG = "Transfer 200 USDC from Filecoin to Arbitrum."


def do_NER(user_msg=None):

	if not user_msg:
		user_msg = USER_MSG

	system_msg = """
	Entity Definition:\n
	
	    "1. srcChain: Short name of the source chain or the from chain, can be from Filecoin, Ethereum, Base, Arbitrum\n"
	    "2. destChain: Short name of the source chain or the from chain, can be from Filecoin, Ethereum, Base, Arbitrum\n"
	    "3. amount: This is a whole number\n"
	    "4. token: Name the token to be transferred can be from aUSDC,wMATIC, wAVAX\n"
	
	"Output Format is json converted to string in the following format, no other thing should be printed, also remove the "Output: " from the start of the response:\n."
	    {{ "srcChain":  , "destChain" : , "amount":  , "token": , "reason": }}    
	
	\n Match each key in Json to the values available above, incase no value matches leave the field blank
	
	\n
	"Examples:\n"
	    "\n"
	    "1. Sentence: Lets move 300 USDC from Ethereum to Base.\n"
	    "Output: {{"srcChain": "Ethereum", "destinationChain": "Base", "amount": 300,"token":"aUSDC"}}\n"
	    "\n"
	    "12. Sentence: Lets move 200 USDC from Base to Ethereum.\n"
	    "Output: {{"srcChain": "Base", "destinationChain": "Ethereum", "amount": 200,"token":"aUSDC"}}\n"
	    "3. Sentence: {{}}\n"
	    "Output: {{"srcChain": , "destinationChain": , "amount": ,"token": }}"\n
		{format_instructions}\n
	\n Use the above information to give the output for the following text - {user_msg}
	
	"""

	print("REACHED 1")

	model_name = 'text-davinci-003'
	temperature = 0.0
	model = OpenAI(model_name=model_name, temperature=temperature)

	parser = PydanticOutputParser(pydantic_object=AxelarInput)

	prompt = PromptTemplate(
	 template=system_msg,
	 input_variables=["user_msg"],
	 partial_variables={"format_instructions": parser.get_format_instructions()})

	_input = prompt.format_prompt(user_msg=user_msg)
	output = model(_input.to_string())

	json_output = json.loads(output.split(":", 1)[1].strip())
	return json_output


# Run it as main to test print the response
if __name__ == '__main__':
	a = do_NER()
	print(a)
