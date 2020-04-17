import os
import sys

import pytest

from stograde.common import chdir
from stograde.student import clone_url
from stograde.toolkit.__main__ import main
from test.common.test_find_unmerged_branches_in_cwd import touch

_dir = os.path.dirname(os.path.realpath(__file__))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_clone(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    argv = sys.argv
    sys.argv = [argv[0]] + ['repo', 'clone', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']
    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)

        try:
            main()
        except SystemExit:
            pass

        assert os.path.exists(student_path)


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_update(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    argv = sys.argv
    sys.argv = [argv[0]] + ['repo', 'update', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']
    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)

        try:
            main()
        except SystemExit:
            pass

        assert os.path.exists(student_path)


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_clean(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    argv = sys.argv
    sys.argv = [argv[0]] + ['repo', 'clean', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']
    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)
        clone_url('https://github.com/StoDevX/cs251-specs', student_path)
        touch(os.path.join(student_path, 'a_file'))
        assert os.path.exists(os.path.join(student_path, 'a_file'))

        try:
            main()
        except SystemExit:
            pass

        assert os.path.exists(student_path)
        assert not os.path.exists(os.path.join(student_path, 'a_file'))


@pytest.mark.datafiles(os.path.join(_dir, 'fixtures', 'repo_tests'))
def test_repo_reclone(datafiles):
    student_path = os.path.join(datafiles, 'students', 'cs251-specs')

    argv = sys.argv
    sys.argv = [argv[0]] + ['repo', 'reclone', '--stogit', 'https://github.com/StoDevX', '--course', 'sd',
                            '--skip-version-check', '--skip-dependency-check']
    with chdir(str(datafiles)):
        assert not os.path.exists(student_path)
        clone_url('https://github.com/StoDevX/cs251-specs', student_path)
        touch(os.path.join(student_path, 'a_file'))
        assert os.path.exists(os.path.join(student_path, 'a_file'))

        try:
            main()
        except SystemExit:
            pass

        assert os.path.exists(student_path)
        assert not os.path.exists(os.path.join(student_path, 'a_file'))
