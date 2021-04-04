import dataclasses
from dataclasses import dataclass
from typing import List
import datetime

from enum import Enum, unique, auto

VoteId = str
QuestionId = str


@dataclass
class User:
    team_domain: str
    team_id: str
    user_id: str
    username: str

    def copy(self) -> "User":
        return User(team_domain=self.team_domain, team_id=self.team_id, user_id=self.user_id, username=self.username)

    def create_user_link(self) -> str:
        return f"https://{self.team_domain}.slack.com/team/{self.user_id}"

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return self.team_domain == other.team_domain and self.team_id == other.team_id \
            and self.user_id == other.user_id and self.username == other.username


@dataclass
class Vote:
    vote_id: VoteId
    text: str
    vote_user: User

    def copy(self) -> "Vote":
        return Vote(vote_id=self.vote_id, text=self.text, vote_user=self.vote_user)


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
    valid_votes: List[Vote] = dataclasses.field(default_factory=list)

    def delete_question(self):
        self.deleted_at = datetime.datetime.now()

    def is_valid(self) -> bool:
        return self.deleted_at is None

    def copy(self) -> "Question":
        return Question(
            text=self.text, create_user=self.create_user, question_id=self.question_id,
            question_type=self.question_type, created_at=self.created_at,
            last_modified_at=self.last_modified_at, deleted_at=self.deleted_at,
            valid_votes=self.valid_votes
        )
