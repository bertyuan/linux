#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-2.0

"""
This script helps track the translation status of the documentation
in different locales, e.g., zh_CN. It uses explicit baseline markers
from the translation's Git history when available, with author-date
inference as a fallback. If the English file has changed since the
baseline, it reports the commits that need to be translated.

The usage is as follows:
- tools/docs/checktransupdate.py -l zh_CN
This will print all the files that need to be updated or translated in the zh_CN locale.
- tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools/testing-overview.rst
This will only print the status of the specified file.
- tools/docs/checktransupdate.py Documentation/translations/zh_CN/dev-tools
This will print the status of all files under the directory.

The output is something like:
Documentation/dev-tools/kfence.rst
No translation in the locale of zh_CN

Documentation/translations/zh_CN/dev-tools/testing-overview.rst
commit 42fb9cfd5b18 ("Documentation: dev-tools: Add link to RV docs")
1 commits needs resolving in total
"""

import os
import re
import sys
import time
import logging
from argparse import ArgumentParser, ArgumentTypeError, BooleanOptionalAction


class GitCommandError(RuntimeError):
    """An error reported by a Git command."""


class BaselineError(RuntimeError):
    """An error which prevents a translation baseline from being used."""


def run_git_command(command, expected_exit_codes=(0,)):
    """Run a Git command and return its output and exit status."""
    logging.debug(command)
    pipe = os.popen(f"{command} 2>&1")
    result = pipe.read()
    status = pipe.close()
    exit_code = 0 if status is None else os.waitstatus_to_exitcode(status)
    if exit_code not in expected_exit_codes:
        details = result.strip()
        if details:
            raise GitCommandError(
                f"Git command failed with exit code {exit_code}: {details}"
            )
        raise GitCommandError(
            f"Git command failed with exit code {exit_code}: {command}"
        )
    return result, exit_code


def get_origin_path(file_path):
    """Get the origin path from the translation path"""
    paths = os.path.normpath(file_path).split(os.sep)
    if len(paths) < 4 or paths[:2] != ["Documentation", "translations"]:
        return None
    return os.path.join("Documentation", *paths[3:])


def is_translation_path(file_path):
    """Return whether a path is within a documentation translation locale."""
    paths = os.path.normpath(file_path).split(os.sep)
    return len(paths) >= 3 and paths[:2] == ["Documentation", "translations"]


def parse_commit(result):
    """Parse the machine-readable output describing one commit."""
    if not result:
        return None
    fields = result.split("\0")
    if len(fields) != 2:
        raise GitCommandError("Git returned malformed commit information")
    return {
        "hash": fields[0],
        "author_date": int(fields[1]),
    }


def get_latest_commit_from(file_path, commit):
    """Get the latest commit from the specified commit for the specified file"""
    command = f"git log --format='%H%x00%at' {commit} -1 -- {file_path}"
    result, _ = run_git_command(command)
    parsed = parse_commit(result)
    if parsed is not None:
        logging.debug("Result: %s", parsed["hash"])
    return parsed


def get_commit(commit):
    """Get information about exactly the specified commit."""
    command = f"git show -s --format='%H%x00%at' {commit}"
    result, _ = run_git_command(command)
    return parse_commit(result)


def get_translation_history(file_path):
    """Get commits and messages touching a translation, newest first."""
    command = f"git log -z --format='%H%x00%B' HEAD -- {file_path}"
    result, _ = run_git_command(command)
    if not result:
        return []

    fields = result.split("\0")
    if fields[-1] == "":
        fields.pop()
    if len(fields) % 2:
        raise GitCommandError("Git returned malformed translation history")

    history = []
    for index in range(0, len(fields), 2):
        history.append({
            "hash": fields[index],
            "message": fields[index + 1].splitlines(),
        })
    return history


def get_origin_from_trans_by_date(origin_path, t_from_head):
    """Get the latest origin commit from the translation commit"""
    command = (
        f"git log -z --format='%H%x00%at' "
        f"{t_from_head['hash']} -- {origin_path}"
    )
    result, _ = run_git_command(command)
    fields = result.split("\0")
    if fields[-1] == "":
        fields.pop()
    if len(fields) % 2:
        raise GitCommandError("Git returned malformed origin history")

    for index in range(0, len(fields), 2):
        if int(fields[index + 1]) <= t_from_head["author_date"]:
            logging.debug("tracked origin commit id: %s", fields[index])
            return {
                "hash": fields[index],
                "author_date": int(fields[index + 1]),
            }
    return None


BASELINE_RE = re.compile(
    r"\b(?:update\s+to(?:\s+the)?\s+commit|"
    r"update\s+the\s+translation\s+through\s+commit)\s+"
    # Four is Git's minimum abbreviation length; Git resolves ambiguity below.
    r"([0-9a-f]{4,64})\b",
    re.IGNORECASE,
)


def extract_baseline_candidates(message):
    """Return every baseline object name recorded in a commit message."""
    return BASELINE_RE.findall("\n".join(message))


def resolve_commit(candidate):
    """Resolve an abbreviated or full object name to a commit."""
    result, _ = run_git_command(f"git rev-parse --verify {candidate}^{{commit}}")
    return result.strip()


def candidate_modifies_origin(candidate, origin_path):
    """Return whether the candidate commit itself modifies origin_path."""
    command = (
        "git diff-tree --root -m --no-commit-id --name-only -r "
        f"{candidate} -- {origin_path}"
    )
    result, _ = run_git_command(command)
    return bool(result.strip())


def is_ancestor(commit1, commit2):
    """Return whether commit1 is an ancestor of commit2."""
    command = f"git merge-base --is-ancestor {commit1} {commit2}"
    _, exit_code = run_git_command(command, expected_exit_codes=(0, 1))
    return exit_code == 0


def select_latest_baseline(candidates, translation_commit, origin_path):
    """Select the descendant of all other valid baseline candidates."""
    if len(candidates) == 1:
        return candidates[0]

    latest = [
        candidate
        for candidate in candidates
        if all(
            other == candidate or is_ancestor(other, candidate)
            for other in candidates
        )
    ]
    if len(latest) != 1:
        raise BaselineError(
            f"ambiguous English baselines in translation commit "
            f"{translation_commit} for {origin_path}: {', '.join(candidates)}"
        )
    return latest[0]


def get_origin_from_translation_history(origin_path, translation_path):
    """Find the newest valid explicit baseline in translation history."""
    for translation_commit in get_translation_history(translation_path):
        candidates = extract_baseline_candidates(translation_commit["message"])
        if not candidates:
            continue

        valid_candidates = []
        for candidate in candidates:
            try:
                resolved = resolve_commit(candidate)
            except GitCommandError as error:
                logging.warning(
                    "Rejecting baseline %s from translation commit %s: %s",
                    candidate, translation_commit["hash"], error,
                )
                continue
            if not candidate_modifies_origin(resolved, origin_path):
                logging.debug(
                    "Rejecting baseline %s from translation commit %s: "
                    "it did not modify %s",
                    candidate, translation_commit["hash"], origin_path,
                )
                continue
            if resolved not in valid_candidates:
                valid_candidates.append(resolved)

        if not valid_candidates:
            continue

        baseline = select_latest_baseline(
            valid_candidates, translation_commit["hash"], origin_path
        )
        logging.debug("tracked explicit origin commit id: %s", baseline)
        return get_commit(baseline)
    return None


def get_commits_count_between(opath, commit1, commit2):
    """Get the commits count between two commits for the specified file"""
    command = f"git log --pretty=format:%H {commit1}...{commit2} -- {opath}"
    output, _ = run_git_command(command)
    result = output.split("\n")
    # filter out empty lines
    result = list(filter(lambda x: x != "", result))
    return result


def pretty_output(commit):
    """Pretty print the commit message"""
    command = f"git log --pretty='format:%h (\"%s\")' -1 {commit}"
    result, _ = run_git_command(command)
    return result


def valid_commit(commit):
    """Check if the commit is valid or not"""
    msg = pretty_output(commit)
    return "Merge tag" not in msg

def check_per_file(file_path):
    """Check the translation status for the specified file"""
    opath = get_origin_path(file_path)

    if opath is None:
        logging.error(
            "Invalid translation path: %s "
            "(expected Documentation/translations/<locale>/...)",
            file_path,
        )
        return

    if not os.path.isfile(opath):
        logging.error("Cannot find the origin path for %s", file_path)
        return

    o_from_head = get_latest_commit_from(opath, "HEAD")
    t_from_head = get_latest_commit_from(file_path, "HEAD")

    if o_from_head is None or t_from_head is None:
        logging.error("Cannot find the latest commit for %s", file_path)
        return

    o_from_t = get_origin_from_translation_history(opath, file_path)
    if o_from_t is None:
        o_from_t = get_origin_from_trans_by_date(opath, t_from_head)

    if o_from_t is None:
        logging.error("Error: Cannot find the latest origin commit for %s", file_path)
        return

    if o_from_head["hash"] == o_from_t["hash"]:
        logging.debug("No update needed for %s", file_path)
    else:
        logging.info(file_path)
        commits = get_commits_count_between(
            opath, o_from_t["hash"], o_from_head["hash"]
        )
        count = 0
        for commit in commits:
            if valid_commit(commit):
                logging.info("commit %s", pretty_output(commit))
                count += 1
        logging.info("%d commits needs resolving in total\n", count)


def valid_locales(locale):
    """Check if the locale is valid or not"""
    script_path = os.path.dirname(os.path.abspath(__file__))
    linux_path = os.path.join(script_path, "../..")
    if not os.path.isdir(f"{linux_path}/Documentation/translations/{locale}"):
        raise ArgumentTypeError(f"Invalid locale: {locale}")
    return locale


def list_files_with_excluding_folders(folder, exclude_folders, include_suffix):
    """List all files with the specified suffix in the folder and its subfolders"""
    files = []
    stack = [folder]

    while stack:
        pwd = stack.pop()
        # filter out the exclude folders
        if os.path.basename(pwd) in exclude_folders:
            continue
        # list all files and folders
        for item in os.listdir(pwd):
            ab_item = os.path.join(pwd, item)
            if os.path.isdir(ab_item):
                stack.append(ab_item)
            else:
                if ab_item.endswith(include_suffix):
                    files.append(ab_item)

    return files


class DmesgFormatter(logging.Formatter):
    """Custom dmesg logging formatter"""
    def format(self, record):
        timestamp = time.time()
        formatted_time = f"[{timestamp:>10.6f}]"
        log_message = f"{formatted_time} {record.getMessage()}"
        return log_message


def config_logging(log_level, log_file="checktransupdate.log"):
    """configure logging based on the log level"""
    # set up the root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)

    # Create file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)

    # Create formatter and add it to the handlers
    formatter = DmesgFormatter()
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handler to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


def main():
    """Main function of the script"""
    script_path = os.path.dirname(os.path.abspath(__file__))
    linux_path = os.path.join(script_path, "../..")

    parser = ArgumentParser(description="Check the translation update")
    parser.add_argument(
        "-l",
        "--locale",
        default="zh_CN",
        type=valid_locales,
        help="Locale to check when files are not specified",
    )

    parser.add_argument(
        "--print-missing-translations",
        action=BooleanOptionalAction,
        default=True,
        help="Print files that do not have translations",
    )

    parser.add_argument(
        '--log',
        default='INFO',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        help='Set the logging level')

    parser.add_argument(
        '--logfile',
        default='checktransupdate.log',
        help='Set the logging file (default: checktransupdate.log)')

    parser.add_argument(
        "files", nargs="*", help="Files or directories to check, if not specified, check all files"
    )
    args = parser.parse_args()

    # Configure logging based on the --log argument
    log_level = getattr(logging, args.log.upper(), logging.INFO)
    config_logging(log_level, args.logfile)

    # Get files related to linux path
    files = args.files
    if len(files) == 0:
        offical_files = list_files_with_excluding_folders(
            os.path.join(linux_path, "Documentation"), ["translations", "output"], "rst"
        )

        for file in offical_files:
            # split the path into parts
            path_parts = file.split(os.sep)
            # find the index of the "Documentation" directory
            kindex = path_parts.index("Documentation")
            # insert the translations and locale after the Documentation directory
            new_path_parts = path_parts[:kindex + 1] + ["translations", args.locale] \
                           + path_parts[kindex + 1 :]
            # join the path parts back together
            new_file = os.sep.join(new_path_parts)
            if os.path.isfile(new_file):
                files.append(new_file)
            else:
                if args.print_missing_translations:
                    logging.info(os.path.relpath(os.path.abspath(file), linux_path))
                    logging.info("No translation in the locale of %s\n", args.locale)
    else:
        # check if the files are directories or files
        new_files = []
        for file in files:
            relative_file = os.path.relpath(os.path.abspath(file), linux_path)
            if not is_translation_path(relative_file):
                logging.error(
                    "Invalid translation path: %s "
                    "(expected Documentation/translations/<locale>/...)",
                    file,
                )
                return 1
            if os.path.isfile(file):
                new_files.append(file)
            elif os.path.isdir(file):
                # for directories, list all files in the directory and its subfolders
                new_files.extend(list_files_with_excluding_folders(file, [], "rst"))
            else:
                logging.error("Cannot find input path: %s", file)
                return 1
        files = new_files

    files = list(map(lambda x: os.path.relpath(os.path.abspath(x), linux_path), files))

    # cd to linux root directory
    os.chdir(linux_path)

    success = True
    for file in files:
        try:
            check_per_file(file)
        except (GitCommandError, BaselineError) as error:
            logging.error("Cannot check %s: %s", file, error)
            success = False
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
