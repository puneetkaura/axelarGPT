from fastapi import FastAPI, Request

from NER import do_NER

app = FastAPI()

ACCESS_OPENAI = True

DEFAULT_DICT = {'srcChain': 'Filecoin', 'destinationChain': 'Arbitrum', 'amount': 200, 'token': 'aUSDC'}

from fastapi.middleware.cors import CORSMiddleware

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Default root endpoint
@app.get("/")
async def root():
	return {"message": "Hello world"}


# Example path parameter
@app.get("/name/{name}")
async def name(name: str):
	return {"message": f"Hello {name}"}


@app.post("/extract")
async def extract(info: Request):
	req_info = await info.json()
	user_msg = req_info["user_msg"]
	if ACCESS_OPENAI :
		ner_dict =  do_NER(user_msg=user_msg)
		return {"user_msg" : user_msg, "ner": ner_dict}
	else :
		return {"user_msg" : user_msg, "ner": DEFAULT_DICT}
