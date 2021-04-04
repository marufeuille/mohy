from abc import ABC, abstractmethod
from typing import Dict, List
from threading import Lock
import random
import string


from mohy.entities import Question, Vote, User


class AbstractQuestionRepository(ABC):
    @abstractmethod
    def save(self, question: Question) -> bool:
        pass

    @abstractmethod
    def find(self, question_id: str) -> Question:
        pass

    @abstractmethod
    def find_by_user(self, user: User) -> List[Question]:
        pass

    @abstractmethod
    def generate_new_question_id(self, n: int) -> str:
        pass


class AbstractVoteRepository(ABC):
    @abstractmethod
    def save(self, vote: Vote) -> bool:
        pass

    @abstractmethod
    def find(self, id: str) -> Vote:
        pass

    @abstractmethod
    def generate_new_vote_id(self, n: int) -> str:
        pass


class AbstractUserRepository(ABC):
    @abstractmethod
    def save(self, answer: User) -> bool:
        pass

    @abstractmethod
    def find(self, team_id: str, user_id: str) -> User:
        pass


def generate_random_string(n: int = 20):
    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst)


class OnMemoryQuestionRepository(AbstractQuestionRepository):
    __singleton = None
    __lock = Lock()

    def __new__(cls):
        cls.__lock.acquire()
        if cls.__singleton is None:
            cls.__singleton = super(OnMemoryQuestionRepository, cls).__new__(cls)
            cls.__singleton.questions = {}
        cls.__lock.release()
        return cls.__singleton

    def save(self, question: Question) -> bool:
        question_id = question.question_id
        if question_id in self.questions.keys():
            raise KeyError(f"question id {question_id} is already taken")
        self.questions[question_id] = question
        return True

    def find(self, question_id: str) -> Question:
        if question_id not in self.questions.keys():
            raise KeyError(f"question id {question_id} not found")

        return self.questions[question_id].copy()

    def find_by_user(self, user: User) -> List[Question]:
        questions_by_user = [q for q in self.questions.values() if q.create_user == user]
        return questions_by_user

    def generate_new_question_id(self, n: int = 20) -> str:
        while True:
            candidate_id = generate_random_string(n)
            try:
                self.find(candidate_id)
            except KeyError:
                break
        return candidate_id


class OnMemoryVoteRepository(AbstractVoteRepository):
    __singleton = None
    __lock = Lock()

    def __new__(cls):
        cls.__lock.acquire()
        if cls.__singleton is None:
            cls.__singleton = super(OnMemoryVoteRepository, cls).__new__(cls)
            cls.__singleton.votes = {}
        cls.__lock.release()
        return cls.__singleton

    def save(self, vote: Vote) -> bool:
        if vote.vote_id in self.votes.keys():
            raise KeyError(f"vote id {vote.vote_id} is taken")
        self.votes[vote.vote_id] = vote
        return True

    def find(self, vote_id: str) -> Vote:
        if vote_id not in self.votes.keys():
            raise KeyError(f"vote id {vote_id} not found")
        return self.votes[vote_id].copy()

    def generate_new_vote_id(self, n: int = 20) -> str:
        while True:
            candidate_id = generate_random_string(n)
            try:
                self.find(candidate_id)
            except KeyError:
                break
        return candidate_id


class OnMemoryUserRepository(AbstractUserRepository):
    __singleton = None
    __lock = Lock()

    def __new__(cls):
        cls.__lock.acquire()
        if cls.__singleton is None:
            cls.__singleton = super(OnMemoryUserRepository, cls).__new__(cls)
            cls.__singleton.users = {}
        cls.__lock.release()
        return cls.__singleton

    def save(self, user: User) -> bool:
        if user.team_id not in self.users.keys():
            self.users[user.team_id] = {}
        if user.user_id not in self.users[user.team_id].keys():
            self.users[user.team_id][user.user_id] = user
        return True

    def find(self, team_id: str, user_id: str) -> User:
        if team_id not in self.users.keys():
            raise KeyError(f"team id {team_id} not found")
        if user_id not in self.users[team_id].keys():
            raise KeyError(f"user id {user_id} not found")
        return self.users[team_id][user_id]
