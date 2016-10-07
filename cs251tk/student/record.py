from os import path
from cs251tk.common import chdir
from cs251tk.student.markdownify import markdownify


def record(student, specs, to_record, basedir, debug):
    recordings = []
    if not to_record:
        return recordings

    with chdir(student):
        for one_to_record in to_record:
            if debug:
                print('recording', one_to_record)
            if path.exists(one_to_record):
                with chdir(one_to_record):
                    recording = markdownify(one_to_record, student, specs[one_to_record], basedir, debug)
            else:
                recording = {
                    'spec': one_to_record,
                    'student': student,
                    'warnings': {'no submission': True},
                }

            recordings.append(recording)

    return recordings
