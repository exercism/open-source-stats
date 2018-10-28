import os
import csv
from datetime import datetime, timedelta

from dateutil import rrule
from github import Github
from github.PaginatedList import PaginatedList
from github.Repository import Repository



def prompt_user() -> (str, str):
    user = input('Enter user: ').strip()

    password = input('Enter password: ').strip()

    return user, password


def get_repos() -> PaginatedList:
    user, password = prompt_user()

    github_client = Github(user, password)

    exercism_org = github_client.get_organization('Exercism')

    return exercism_org.get_repos()


def get_repo_data(repo: Repository):
    now = datetime.now()

    start_point = now - timedelta(days=31*6)

    for day in rrule.rrule(rrule.DAILY, dtstart=start_point, until=now):
        prev_day = day - timedelta(days=1)

        commits = repo.get_commits(since=prev_day, until=day)

        yield (day.strftime('%d.%m.%Y'), commits.totalCount)


def generate_result(repo: Repository):
    #FIXME: Relative paths are bad. Change this later
    result_dir_path = '../../results/commits_count'

    if not os.path.exists(result_dir_path):
        os.makedirs(result_dir_path)

    result_path = os.path.join(
        result_dir_path,
        '{}.csv'.format(repo.name)
    )

    fields = ['date', 'commit_count']

    repo_data = get_repo_data(repo)

    with open(result_path, 'w') as result_file:
        csv_writer = csv.writer(result_file)

        csv_writer.writerow(fields)

        for data_line in repo_data:
            csv_writer.writerow(data_line)


def count_commits():
    repos = get_repos()

    for repo in repos:
        generate_result(repo)


if __name__ == '__main__':
    count_commits()
