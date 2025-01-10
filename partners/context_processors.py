import subprocess

def git_branch(request):
    try:
        branch = subprocess.check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).strip().decode('utf-8')
        return {'branch_name': branch}
    except subprocess.CalledProcessError:
        return {'branch_name': "Unknown"}
