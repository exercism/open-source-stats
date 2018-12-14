import os


def generate_plot(result_dir: str):
    commit_count_file = os.path.join(result_dir, 'commit_count.csv')

    if not os.path.exists(commit_count_file):
        print('Commit count CSV file not found for the {}'.format(result_dir))

        return


def main():
    result_dirs = map(
        lambda dir_name: os.path.join(os.environ['RESULT_DIR'], dir_name),
        os.listdir(os.environ['RESULT_DIR'])
    )

    for dir in result_dirs:
        print(dir)

        generate_plot(dir)

        break


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
