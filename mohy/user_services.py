from typing import List
from mohy.repositories import (
    AbstractAnswerRepository, AbstractExecutionRepository, AbstractQuestionRepository, AbstractUserRepository,
    OnMemoryAnswerRepository, OnMemoryExecutionRepository, OnMemoryQuestionRepository, OnMemoryUserRepository
)
from mohy.entities import Answer, AnswerId, Execution, ExecutionId, Question, QuestionId, QuestionType, User


class UserApplicationService:
    def __init__(self):
        self.question_repository: AbstractQuestionRepository = OnMemoryQuestionRepository()
        self.answer_repository: AbstractAnswerRepository = OnMemoryAnswerRepository()
        self.user_repository: AbstractUserRepository = OnMemoryUserRepository()
        self.execution_repository: AbstractExecutionRepository = OnMemoryExecutionRepository()

    def create_question(self, question_type: str, question_text: str, create_user_name: str) -> QuestionId:
        user = User(user_id=self.user_repository.generate_new_user_id(), name=create_user_name)
        self.user_repository.save(user)
        question = Question(text=question_text, create_user=user,
                            question_id=self.question_repository.generate_new_question_id(),
                            question_type=QuestionType.value_of(question_type))
        self.question_repository.save(question)
        return question.question_id

    def create_execution(self, question_id_str: str, create_user_name: str) -> ExecutionId:
        user = User(user_id=self.user_repository.generate_new_user_id(), name=create_user_name)
        question_id = QuestionId(question_id_str)
        question: Question = self.question_repository.find(question_id)
        execution: Execution = Execution(
            execution_id=self.execution_repository.generate_new_execution_id(), question=question, create_user=user)
        self.execution_repository.save(execution=execution)
        return execution.execution_id

    def answer_question(self, execution_id_str: str, answer_text: str, answering_user_name: str) -> AnswerId:
        execution_id = ExecutionId(execution_id_str)
        self.execution_repository.find(execution_id=execution_id)
        user = User(user_id=self.user_repository.generate_new_user_id(), name=answering_user_name)
        self.user_repository.save(user)
        answer = Answer(text=answer_text, answering_user=user,
                        answer_id=self.answer_repository.generate_new_answer_id())
        self.execution_repository.add_answer(answer)
        self.answer_repository.save(execution_id, answer)
        return answer.answer_id

    def list_question(self) -> List[Question]:
        return self.question_repository.questions.copy()

    def describe_question(self, question_id_str: str) -> Question:
        question_id = QuestionId(question_id_str)
        return self.question_repository.find(question_id).copy()
