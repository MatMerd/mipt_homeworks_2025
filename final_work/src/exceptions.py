class GitHubAPIError(Exception):

    def __init__(self, message: str, status_code: int | None = None) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class GitHubRateLimitError(GitHubAPIError):

    def __init__(self, message: str = "GitHub API rate limit exceeded") -> None:
        super().__init__(message, status_code=429)


class GitHubNotFoundError(GitHubAPIError):

    def __init__(self, message: str = "Resource not found") -> None:
        super().__init__(message, status_code=404)


class GitHubAuthenticationError(GitHubAPIError):

    def __init__(self, message: str = "Authentication failed") -> None:
        super().__init__(message, status_code=401)


class GitHubServerError(GitHubAPIError):

    def __init__(self, message: str = "GitHub server error") -> None:
        super().__init__(message, status_code=500)

