import logging
import os
from typing import List

from stograde.common import chdir
from stograde.common import find_unmerged_branches_in_cwd
from stograde.process_assignment.assignment_status import AssignmentStatus
from stograde.process_assignment.assignment_type import AssignmentType, get_assignment_type
from stograde.specs import get_filenames, Spec
from stograde.student.student_result import StudentResult


def analyze(student: StudentResult, specs: List[Spec], check_for_branches: bool, ci: bool):
    logging.debug("Analyzing {}'s assignments".format(student.name))

    if check_for_branches and not ci:
        student.unmerged_branches = find_unmerged_branches_in_cwd()

    directory = student.name if not ci else '.'
    analyses = {}
    with chdir(directory):
        for spec in specs:
            analyses[spec.id] = analyze_assignment(spec)

    for name, analysis in analyses.items():
        a_type = get_assignment_type(name)
        if a_type is AssignmentType.HOMEWORK:
            student.homeworks[name] = analysis
        elif a_type is AssignmentType.LAB:
            student.labs[name] = analysis
        elif a_type is AssignmentType.WORKSHEET:
            student.worksheets[name] = analysis


def analyze_assignment(spec: Spec) -> AssignmentStatus:
    if not os.path.exists(spec.folder):
        return AssignmentStatus.MISSING

    with chdir(spec.folder):
        files_that_do_exist = set(os.listdir('.'))
        files_which_should_exist = set(get_filenames(spec))
        intersection_of = files_that_do_exist.intersection(files_which_should_exist)

        if intersection_of == files_which_should_exist:
            # if every file that should exist, does: we're good.
            return AssignmentStatus.SUCCESS
        elif intersection_of:
            # if some files that should exist, do: it's a partial assignment
            return AssignmentStatus.PARTIAL
        else:
            # otherwise, none of the required files are there
            return AssignmentStatus.MISSING
