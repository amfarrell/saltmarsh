from test_utils import run_frodo, run_samwise, SaltStateTestCase
import shutil
import os.path
import unittest
import yaml

class TestSamwiseRepoCloned(SaltStateTestCase):

    def debian_package_installed(self, packagename):
        return not 'no packages found matching {}'.format(packagename) in \
                run_samwise("dpkg-query -l '{}'".format(packagename))

    def test_virtualenv_exists(self):
        if self.debian_package_installed('python-virtualenv'):
            run_samwise('sudo apt-get remove python-virtualenv')
        if os.path.exists('samwise_vagrant/example-venv/bin/'):
            shutil.rmtree('samwise_vagrant/example-venv')
        state_response_data = self.run_state(state_file='django', target='samwise')
        assert self.debian_package_installed('python-virtualenv')
        assert os.path.exists('samwise_vagrant/example-venv/bin/')
        assert os.path.exists('samwise_vagrant/example-venv/bin/django-admin.py')
        assert os.path.exists('samwise_vagrant/example-venv/bin/gunicorn')

    def test_git_repo_exists(self):
        if os.path.exists('samwise_vagrant/django-example'):
            shutil.rmtree('samwise_vagrant/django-example')
        if self.debian_package_installed('git'):
            run_samwise('sudo apt-get remove git')
        state_response_data = self.run_state(state_file='django', target='samwise')
        assert self.debian_package_installed('git')
        assert os.path.exists('samwise_vagrant/django-example/manage.py'), \
            "The app's git repository has not been cloned."
