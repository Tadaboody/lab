import re
from pathlib import Path
from typing import Tuple

import git
from fire import Fire
import requests


class Lab:
    def __init__(self, token: str, dir: Path):
        self.__token = token
        self.__dir = dir
        self.__repo = git.Repo(dir)
        self.__client = requests.Session()

    def __remote_link(self) -> str:
        full_url = next(self.__repo.remote(name='gitlab').urls)
        return full_url[:-len('.git')] # Strip also removes the git from the start

    def __project_id(self) -> Tuple[str, str]:
        match = re.match(r'git@gitlab.com:([^/]+)/(.+)', self.__remote_link())
        return match[1], match[2].strip('.git')

    def __api_link(self) -> str:
        namespace, project = self.__project_id()
        return f"https://gitlab.com/api/v4/projects/{namespace}%2F{project}"

    def endpoint(self, *args: Tuple[str, ...]):
        return '/'.join([self.__api_link(), *args])

    def __get(self, end, *args, **kwargs) -> requests.Response:
        params = {'private_token': self.__token, **kwargs.pop('params', dict())}
        resp = self.__client.get(end, params=params, *args, **kwargs)
        resp.raise_for_status()
        return resp

    def issue(self, limit: int = 20):
        resp = self.__get(self.endpoint('issues'), params={'state': 'opened'})
        for issue in resp.json():
            yield  f"#{issue['iid']}    {issue['title']}" 


if __name__ == '__main__':
    from os import environ
    Fire(Lab(environ.get('GITLAB_ACCESS_TOKEN', None), Path.cwd()), name='lab')
