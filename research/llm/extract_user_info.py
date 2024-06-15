from typing import List

from kor import create_extraction_chain
from kor.nodes import Object, Text, Number
# from langchain.callbacks import get_openai_callback
from langchain_openai.chat_models import ChatOpenAI


class ExtractInfo:
    llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0,
    )

    schema = Object(
        id="personal_info",
        description="Personal information about a given person.",
        attributes=[
            Text(
                id="first_name",
                description="The first name of the person",
                examples=[("John Smith went to the store", "John")],
            ),
            Text(
                id="last_name",
                description="The last name of the person",
                examples=[("John Smith went to the store", "Smith")],
            ),
            Number(
                id="age",
                description="The age of the person in years.",
                examples=[("23 years old", "23"), ("I turned three on sunday", "3")],
            ),
        ],
        examples=[
            (
                "John Smith was 23 years old. He was very tall. He knew Jane Doe. She was 5 years old.",
                [
                    {"first_name": "John", "last_name": "Smith", "age": 23},
                    {"first_name": "Jane", "last_name": "Doe", "age": 5},
                ],
            )
        ],
        many=True,
    )

    chain = create_extraction_chain(llm, schema)

    def __call__(self, text: str) -> List[dict]:
        return self.chain.predict(text=text)["data"]["personal_info"]


