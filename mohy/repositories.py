from abc import ABC, abstractmethod
from typing import Dict
from threading import Lock
import random
import string


from mohy.entities import Execution, ExecutionId, Question, QuestionId, Answer, AnswerId, User, UserId


class AbstractQuestionRepository(ABC):
    @abstractmethod
    def save(self, question: Question) -> bool:
        pass

    @abstractmethod
    def find(self, question_id: QuestionId) -> Question:
        pass

    @abstractmethod
    def generate_new_question_id(self, n: int) -> QuestionId:
        pass


class AbstractAnswerRepository(ABC):
    @abstractmethod
    def save(self, answer: Answer) -> bool:
        pass

    @abstractmethod
    def find(self, id: AnswerId) -> Answer:
        pass

    @abstractmethod
    def generate_new_answer_id(self, n: int) -> AnswerId:
        pass


class AbstractUserRepository(ABC):
    @abstractmethod
    def save(self, answer: User) -> bool:
        pass

    @abstractmethod
    def find(self, id: UserId) -> User:
        pass

    @abstractmethod
    def generate_new_user_id(self, n: int) -> UserId:
        pass


class AbstractExecutionRepository(ABC):
    @abstractmethod
    def save(self, execution: Execution) -> bool:
        pass

    @abstractmethod
    def find(self, id: ExecutionId) -> Execution:
        pass

    @abstractmethod
    def generate_new_execution_id(self, n: int) -> ExecutionId:
        pass

    @abstractmethod
    def add_answer(self, execution_id: ExecutionId, answer: Answer):
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

    def find(self, question_id: QuestionId) -> Question:
        if question_id not in self.questions.keys():
            raise KeyError(f"question id {question_id} not found")

        return self.questions[question_id].copy()

    def generate_new_question_id(self, n: int = 20) -> QuestionId:
        while True:
            candidate_id = QuestionId(generate_random_string(n))
            try:
                self.find(candidate_id)
            except KeyError:
                break
        return candidate_id


class OnMemoryAnswerRepository(AbstractAnswerRepository):
    __singleton = None
    __lock = Lock()

    def __new__(cls):
        cls.__lock.acquire()
        if cls.__singleton is None:
            cls.__singleton = super(OnMemoryAnswerRepository, cls).__new__(cls)
            cls.__singleton.answers = {}
        cls.__lock.release()
        return cls.__singleton

    def save(self, answer: Answer) -> bool:
        if answer.answer_id in self.answers.keys():
            raise KeyError(f"answer id {answer.answer_id} is taken")
        self.answers[answer.answer_id] = answer
        return True

    def find(self, answer_id: AnswerId) -> Answer:
        if answer_id not in self.answers.keys():
            raise KeyError(f"answer id {answer_id} not found")
        return self.answers[answer_id].copy()

    def update(self, answer_id: AnswerId, answer: Answer):
        if answer_id not in self.answers.keys():
            raise KeyError(f"answer id {answer_id} not found")
        self.answers[answer.answer_id] = answer

    def generate_new_answer_id(self, n: int = 20) -> AnswerId:
        while True:
            candidate_id = AnswerId(generate_random_string(n))
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
        if user.user_id in self.users.keys():
            raise KeyError(f"user id {user.user_id} is taken")
        self.users[user.user_id] = user
        return True

    def find(self, user_id: UserId) -> User:
        if user_id not in self.users.keys():
            raise KeyError(f"user id {user_id} not found")
        return self.users[user_id].copy()

    def generate_new_user_id(self, n: int = 20) -> UserId:
        while True:
            candidate_id = UserId(generate_random_string(n))
            try:
                self.find(candidate_id)
            except KeyError:
                break
        return candidate_id


class OnMemoryExecutionRepository(AbstractExecutionRepository):
    __singleton = None
    __lock = Lock()

    def __new__(cls):
        cls.__lock.acquire()
        if cls.__singleton is None:
            cls.__singleton = super(OnMemoryExecutionRepository, cls).__new__(cls)
            cls.__singleton.executions = {}
        cls.__lock.release()
        return cls.__singleton

    def save(self, execution: Execution) -> bool:
        if execution.execution_id in self.executions.keys():
            raise KeyError(f"user id {execution.execution_id} is taken")
        self.executions[execution.execution_id] = execution
        return True

    def find(self, execution_id: ExecutionId) -> Execution:
        if execution_id not in self.executions.keys():
            raise KeyError(f"execution id {execution_id} not found")
        return self.executions[execution_id].copy()

    def add_answer(self, execution_id: ExecutionId, answer: Answer):
        if execution_id not in self.executions.keys():
            raise KeyError(f"execution id {execution_id} not found")
        self.executions[execution_id].answer_question(answer)

    def generate_new_execution_id(self, n: int = 20) -> ExecutionId:
        while True:
            candidate_id = ExecutionId(generate_random_string(n))
            try:
                self.find(candidate_id)
            except KeyError:
                break
        return candidate_id
