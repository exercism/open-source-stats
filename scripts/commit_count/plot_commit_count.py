import os

import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import pandas as pd


def generate_plot(result_dir: str):
    commit_count_file = os.path.join(result_dir, 'commit_count.csv')

    if not os.path.exists(commit_count_file):
        print('Commit count CSV file not found for the {}'.format(result_dir))

        return

    commit_count_content = pd.read_csv(
        commit_count_file,
        sep=',',
        header=0,
        names=['date', 'commit_count']
    )

    x_pos = range(len(commit_count_content))

    plt.bar(x_pos, commit_count_content['commit_count'])

    plt.xticks(x_pos, commit_count_content['date'], rotation=90)

 #   plt.plot(commit_count_content['date'], commit_count_content['commit_count'])

    plt.ylabel('Commit Count')

    plt.xlabel('Date')

 #   plt.xticks(rotation=90)

    plt.title(os.path.split(result_dir)[-1])

    plt.rcParams["figure.figsize"] = [60, 20]

    # plt.show()

    plt.savefig(os.path.join(result_dir, 'commit_count.png'))

    plt.close()


def main():
    result_dirs = map(
        lambda dir_name: os.path.join(os.environ['RESULT_DIR'], dir_name),
        os.listdir(os.environ['RESULT_DIR'])
    )

    for dir in result_dirs:
        generate_plot(dir)


def check_envinroment_variables() -> (dict, dict):
    required_variables = {
        'RESULT_DIR': os.environ.get('RESULT_DIR'),
        'GITHUB_TOKEN': os.environ.get('GITHUB_TOKEN'),
    }

    present_variables = dict()

    missing_variables = dict()

    for name, value in required_variables.items():
        if not value:
            missing_variables[name] = value
        else:
            present_variables[name] = value

    return present_variables, missing_variables


if __name__ == '__main__':
    present_variables, missing_variables = check_envinroment_variables()

    if missing_variables:
        print(
            (
                'Some required environment variables were not set:\n{}\n\n'
                'The script is aborted.'
            ).format('\n'.join(missing_variables.keys()))
        )
    else:
        print('The following environment variables were set:')

        for k, v in present_variables.items():
            print('{}: {}'.format(k, v))

        result_dir_path = os.environ['RESULT_DIR']

        if os.path.exists(result_dir_path):
            main()
        else:
            print((
                'Result directory does not exist.'
                ' Run get_commit_count.py script to generate it.'
            ))
