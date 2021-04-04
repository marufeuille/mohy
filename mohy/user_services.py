from typing import List
from mohy.repositories import (
    AbstractVoteRepository, AbstractQuestionRepository, AbstractUserRepository,
    OnMemoryVoteRepository, OnMemoryQuestionRepository, OnMemoryUserRepository
)
from mohy.entities import Question, QuestionType, QuestionId, Vote, VoteId, User


class UserApplicationService:
    def __init__(self):
        self.question_repository: AbstractQuestionRepository = OnMemoryQuestionRepository()
        self.vote_repository: AbstractVoteRepository = OnMemoryVoteRepository()
        self.user_repository: AbstractUserRepository = OnMemoryUserRepository()

    def create_question(self, question_type: str, question_text: str, user_id: str, username: str, team_id: str, team_domain: str) -> QuestionId:
        user = User(team_id=team_id, team_domain=team_domain, user_id=user_id, username=username)
        question = Question(text=question_text, create_user=user,
                            question_id=self.question_repository.generate_new_question_id(),
                            question_type=QuestionType.value_of(question_type))
        self.user_repository.save(user)
        self.question_repository.save(question)
        return question.question_id

    def vote_question(self, question_id: str, answer_text: str, user_id: str, username: str, team_id: str, team_domain: str) -> VoteId:
        user = User(team_id=team_id, team_domain=team_domain, user_id=user_id, username=username)
        vote = Vote(vote_id=self.vote_repository.generate_new_vote_id(), text=answer_text, vote_user=User)
        self.user_repository.save(user)
        self.vote_repository.save(vote)
        return vote.vote_id

    def get_questions(self, user_id: str, team_id: str) -> List[Question]:
        user = self.user_repository.find(team_id, user_id)
        return self.question_repository.find_by_user(user)

    def get_question(self, question_id: QuestionId) -> Question:
        return self.question_repository.find(question_id=question_id)
