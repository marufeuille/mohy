import dataclasses
from dataclasses import dataclass
from typing import List
import datetime

from enum import Enum, unique, auto


@dataclass
class UserId:
    user_id: str

    def __hash__(self) -> int:
        return hash(self.user_id)

    def copy(self) -> "UserId":
        return UserId(self.user_id)


@dataclass
class User:
    user_id: UserId
    name: str

    def copy(self) -> "User":
        return User(user_id=self.user_id, name=self.name)


@dataclass
class AnswerId:
    answer_id: str

    def __hash__(self) -> int:
        return hash(self.answer_id)

    def copy(self) -> "AnswerId":
        return AnswerId(answer_id=self.answer_id)


@dataclass
class Answer:
    text: str
    answering_user: User
    answer_id: AnswerId
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    last_modified_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    deleted_at: datetime.datetime = None

    def delete_answer(self):
        self.deleted_at = datetime.datetime.now()

    def is_valid(self) -> bool:
        return self.deleted_at is None

    def copy(self) -> "Answer":
        return Answer(
            text=self.text, answering_user=self.answering_user, answer_id=self.answer_id,
            created_at=self.created_at, last_modified_at=self.last_modified_at, deleted_at=self.deleted_at
        )


@dataclass
class QuestionId:
    question_id: str

    def __hash__(self) -> int:
        return hash(self.question_id)

    def copy(self) -> "QuestionId":
        return QuestionId(self.question_id)


@unique
class QuestionType(Enum):
    FREE_TEXT = "FREE_TEXT"
    MULTIPLE_CHOICE = "MULTIPLE_CHIOICE"
    SINGLE_SELECT = "SINGLE_SELECT"

    @classmethod
    def value_of(cls, target_value):
        for e in QuestionType:
            if e.value == target_value:
                return e
        raise ValueError(f"{target_value} is invalid id")


@dataclass
class Question:
    text: str
    create_user: User
    question_id: QuestionId
    question_type: QuestionType
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    last_modified_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)
    deleted_at: datetime.datetime = None
    valid_choice: List[Answer] = dataclasses.field(default_factory=list)

    def delete_question(self):
        self.deleted_at = datetime.datetime.now()

    def is_valid(self) -> bool:
        return self.deleted_at is None

    def copy(self) -> "Question":
        return Question(
            text=self.text, create_user=self.create_user, question_id=self.question_id,
            question_type=self.question_type, created_at=self.created_at,
            last_modified_at=self.last_modified_at, deleted_at=self.deleted_at,
            valid_choice=self.valid_choice
        )


@dataclass
class ExecutionId:
    execution_id: str

    def __hash__(self) -> int:
        return hash(self.execution_id)

    def copy(self) -> "ExecutionId":
        return ExecutionId(self.execution_id)


@dataclass
class Execution:
    execution_id: ExecutionId
    question: Question
    create_user: User
    answers: List[Answer] = dataclasses.field(default_factory=list)
    created_at: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)

    def copy(self) -> "Execution":
        return Execution(
            execution_id=self.execution_id,
            question=self.question, create_user=self.create_user,
            answers=self.answers, created_at=self.created_at
        )

    def answer_question(self, answer: Answer):
        if self.question.question_type in (QuestionType.MULTIPLE_CHOICE, QuestionType.SINGLE_SELECT):
            if answer not in self.question.valid_choice:
                raise ValueError(f"invalid answer {answer} to this question")

        self.answers.append(answer)
