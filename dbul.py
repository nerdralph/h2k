#!/usr/bin/env python
# Ralph Doncaster 2022
# upload ERS files to dropbox
# based on dropbox sdk updown example
# https://github.com/dropbox/dropbox-sdk-python

import argparse
import contextlib
import datetime
import os
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET

import dropbox

# directory to upload ERS files to on dropbox
dbdir = "Ralph/Files for Submission"

parser = argparse.ArgumentParser(description='Sync ERS files to Dropbox')
parser.add_argument("fileid")
#parser.add_argument('folder', nargs='?', default='Downloads',
parser.add_argument('folder', nargs='?', default=dbdir,
                    help='Folder name in your Dropbox')
#parser.add_argument('localdir', nargs='?', default='~/Downloads',
parser.add_argument('localdir', nargs='?', default='../',
                    help='Local directory to upload')
# OAuth2 access token.
parser.add_argument('--token', default="",
                    help='Access token '
                    '(see https://www.dropbox.com/developers/apps)')
parser.add_argument('--yes', '-y', action='store_true',
                    help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true',
                    help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true',
                    help='Take default answer on all questions')

def main():
    """Main program.

    Parse command line, then iterate over files and directories under
    localdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    args = parser.parse_args()
    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        print('At most one of --yes, --no, --default is allowed')
        sys.exit(2)
    if not args.token:
        print('--token is mandatory')
        sys.exit(2)

    fileid = args.fileid
    folder = args.folder
    #localdir = os.path.expanduser(args.localdir)
    localdir = args.localdir
    print('Dropbox folder name:', folder)
    print('Local directory:', localdir)
    if not os.path.exists(localdir):
        print(localdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(localdir):
        print(localdir, 'is not a folder on your filesystem')
        sys.exit(1)

    dbx = dropbox.Dropbox(args.token)

    fname = fileid + ".h2k"
    fqfn = localdir + '/' + fname
    t = ET.parse(fqfn)
    if len(t.find("ProgramInformation/File/TaxNumber").text.strip()) == 0:
        print("Error: Tax # missing")
        sys.exit(1)

    dbxsubdir = fileid + ' ' + t.find("./ProgramInformation/Client/StreetAddress/Street").text

    # upload(dbx, localfile, folder, subfolder, name, overwrite=True):
    upload(dbx, fqfn, folder, dbxsubdir, fname)

    reports = ("HOIS", "LBL", "SRUR")
    for rpt in reports:
        fname = fileid + rpt + ".pdf"
        fqfn = localdir + '/' + fname
        if os.path.exists(fqfn):
            upload(dbx, fqfn, folder, dbxsubdir, fname)
        else:
            print(fqfn + " does not exist.")

    for dn, dirs, files in os.walk(localdir + fileid):
        subfolder = dn[len(localdir):].strip(os.path.sep)
        listing = list_folder(dbx, folder, subfolder)
        print('Descending into', subfolder, '...')

        # First do all the files.
        for name in files:
            fullname = os.path.join(dn, name)
            #if not isinstance(name, six.text_type):
            if not isinstance(name, str):
                name = name.decode('utf-8')
            nname = unicodedata.normalize('NFC', name)
            if name.startswith('.'):
                print('Skipping dot file:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary file:', name)
            elif name.endswith('.pyc') or name.endswith('.pyo'):
                print('Skipping generated file:', name)
            else: 
                upload(dbx, fullname, folder, dbxsubdir, name)

        # Then choose which subdirectories to traverse.
        keep = []
        for name in dirs:
            if name.startswith('.'):
                print('Skipping dot directory:', name)
            elif name.startswith('@') or name.endswith('~'):
                print('Skipping temporary directory:', name)
            elif name == '__pycache__':
                print('Skipping generated directory:', name)
            elif yesno('Descend into %s' % name, True, args):
                print('Keeping directory:', name)
                keep.append(name)
            else:
                print('OK, skipping directory:', name)
        dirs[:] = keep

    dbx.close()

def list_folder(dbx, folder, subfolder):
    """List a folder.

    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

def download(dbx, folder, subfolder, name):
    """Download a file.

    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(len(data), 'bytes; md:', md)
    return data

def upload(dbx, localfile, folder, subfolder, name, overwrite=True):
    """Upload a file.

    Return the request response, or None in case of error.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    mode = (dropbox.files.WriteMode.overwrite
            if overwrite
            else dropbox.files.WriteMode.add)
    mtime = os.path.getmtime(localfile)
    with open(localfile, 'rb') as f:
        data = f.read()
    #with stopwatch('upload %d bytes' % len(data)):
        try:
            res = dbx.files_upload(
                data, path, mode,
                client_modified=datetime.datetime(*time.gmtime(mtime)[:6]),
                mute=True)
        except dropbox.exceptions.ApiError as err:
            print('*** API error', err)
            return None
    print('uploaded as', res.name.encode('utf8'))
    return res

def yesno(message, default, args):
    """Handy helper function to ask a yes/no question.

    Command line arguments --yes or --no force the answer;
    --default to force the default answer.

    Otherwise a blank line returns the default, and answering
    y/yes or n/no returns True or False.

    Retry on unrecognized answer.

    Special answers:
    - q or quit exits the program
    - p or pdb invokes the debugger
    """
    if args.default:
        print(message + '? [auto]', 'Y' if default else 'N')
        return default
    if args.yes:
        print(message + '? [auto] YES')
        return True
    if args.no:
        print(message + '? [auto] NO')
        return False
    if default:
        message += '? [Y/n] '
    else:
        message += '? [N/y] '
    while True:
        answer = input(message).strip().lower()
        if not answer:
            return default
        if answer in ('y', 'yes'):
            return True
        if answer in ('n', 'no'):
            return False
        if answer in ('q', 'quit'):
            print('Exit')
            raise SystemExit(0)
        if answer in ('p', 'pdb'):
            import pdb
            pdb.set_trace()
        print('Please answer YES or NO.')

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

if __name__ == '__main__':
    main()
