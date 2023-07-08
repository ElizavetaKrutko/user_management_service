from fastapi import Depends

from app.db.dependencies.database import get_async_session


# Repo dependency
def setup_repository(repo_class):
    """Returns specified repository seeded with an async database session."""

    def get_repo(
        db=Depends(get_async_session),
    ):
        return repo_class(db=db)

    return get_repo
