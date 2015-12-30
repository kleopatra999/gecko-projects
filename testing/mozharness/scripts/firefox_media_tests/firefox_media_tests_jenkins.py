#!/usr/bin/env python
# ***** BEGIN LICENSE BLOCK *****
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
# ***** BEGIN LICENSE BLOCK *****
"""firefox_media_tests_jenkins.py

Author: Syd Polk
"""
import copy
import glob
import os
import sys

sys.path.insert(1, os.path.dirname(sys.path[0]))

from mozharness.base.log import ERROR, DEBUG, INFO
from mozharness.base.script import PreScriptAction, PostScriptAction
from mozharness.mozilla.blob_upload import (
    BlobUploadMixin,
    blobupload_config_options
)
from mozharness.mozilla.testing.firefox_media_tests import (
    FirefoxMediaTestsBase, BUSTED, TESTFAILED, UNKNOWN, EXCEPTION, SUCCESS
)


class FirefoxMediaTestsJenkins(FirefoxMediaTestsBase):

    def __init__(self):
        super(FirefoxMediaTestsJenkins, self).__init__(
            all_actions=['clobber',
                         'checkout',
                         'download-and-extract',
                         'create-virtualenv',
                         'install',
                         'run-media-tests',
                         ],
        )

    @PreScriptAction('create-virtualenv')
    def _pre_create_virtualenv(self, action):
        dirs = self.query_abs_dirs()
        requirements = os.path.join(dirs['abs_test_install_dir'],
                                    'config',
                                    'marionette_requirements.txt')
        if os.access(requirements, os.F_OK):
            self.register_virtualenv_module(requirements=[requirements],
                                            two_pass=True)
        super(FirefoxMediaTestsJenkins, self)._pre_create_virtualenv(action)

    def query_abs_dirs(self):
        if self.abs_dirs:
            return self.abs_dirs
        dirs = super(FirefoxMediaTestsJenkins, self).query_abs_dirs()
        dirs['abs_blob_upload_dir'] = os.path.join(dirs['abs_work_dir'],
                                                   'blobber_upload_dir')
        dirs['abs_test_install_dir'] = os.path.join(dirs['abs_work_dir'],
                                                    'tests')
        self.abs_dirs = dirs
        return self.abs_dirs

if __name__ == '__main__':
    media_test = FirefoxMediaTestsJenkins()
    media_test.run_and_exit()
