"""Test TestRail API interface."""

import os
import pytest
import unittest

try:
    import testrail as testrail
except ImportError:
    import staxrail.testrail as testrail

__version__ = '0.0.3'
NON_ACCESS_TESTS_ONLY = os.getenv('TESTRAIL_VALUE', '') == ''


class TestTestRailAPI(unittest.TestCase):
    """TestRail API for OpenStax."""

    def setUp(self):
        """Pretest settings."""
        self.rail = testrail.TestRailAPI(
            'https://%s.testrail.net/' % os.getenv('TESTRAIL_GROUP')
        )
        results = (os.getenv('SHOW_ALL_RESULTS', 'false')).lower() == 'true'
        testrail.TestRailAPI.SHOW_ALL_RESULTS = results

    def tearDown(self):
        """Test destructor."""

    def test_basic_repo_trust(self):
        """Non-test to protect against pytest code 5 for 0 test functions."""
        assert(self.rail is not None), 'Faulty initialization of TestRailAPI'

    @pytest.mark.skipif(NON_ACCESS_TESTS_ONLY,
                        reason='Non-access Travis CI testing')
    def test_get_users(self):
        """."""
        user_one = self.rail.get_user_by_id(1)
        assert(user_one['id'] == 1), 'ID returned: %s != 1' % user_one['id']
        assert(len(user_one['email']) >= 1), 'No email returned for User 1'

        email = user_one['email']
        email_user = self.rail.get_user_by_email(email)
        assert(user_one['id'] == email_user['id']), 'ID mismatch'
        assert(user_one['email'] == email_user['email']), 'Email mismatch'

        user_list = self.rail.get_users()
        assert(len(user_list) >= 1), 'No users returned'

    @pytest.mark.skipif(NON_ACCESS_TESTS_ONLY,
                        reason='Non-access Travis CI testing')
    def test_get_projects(self):
        """."""
        project = self.rail.get_project(1)
        projects = self.rail.get_projects()
        assert(project == projects[0]), 'Project mismatch'

    @pytest.mark.skipif(NON_ACCESS_TESTS_ONLY,
                        reason='Non-access Travis CI testing')
    def test_get_milestones(self):
        """."""
        milestones = self.rail.get_milestones(1)
        assert(milestones is not None), 'Milestone read failure'
        assert(milestones[0]['id'] == 1)

    @pytest.mark.skipif(NON_ACCESS_TESTS_ONLY,
                        reason='Non-access Travis CI testing')
    def test_get_plans(self):
        """."""
        failed_get = self.rail.get_plan(int(os.getenv('NON_PLAN_ID', '99')))
        assert(failed_get == {}), 'Error Report: %s' % failed_get
        plan = self.rail.get_plan(1)
        plans = self.rail.get_plans(1)
        if len(plans) == 0:
            return
        assert(plan == plans[0]), 'Plan mismatch'

        '''
        To Be Coded:
        ------------
        GET Actions
        suite = self.rail.get_suite(1)
        suites = self.rail.get_suites(1)
        case = self.rail.get_case(1)
        cases = self.rail.get_cases(1, {'suite_id': 1, })
        fields = self.rail.get_case_fields()
        types = self.rail.get_case_types()
        priorities = self.rail.get_priorities()
        templates = self.rail.get_templates(1)
        result_fields = self.rail.get_result_fields()
        results = self.rail.get_results(6865)
        case_results = self.rail.get_results_for_case(65, 2)
        run_results = self.rail.get_results_for_run(65)
        test_run = self.rail.get_run(65)
        test_runs = self.rail.get_runs(1)
        statuses = self.rail.get_statuses()
        test = self.rail.get_test(6865)
        tests = self.rail.get_tests(65)
        section = self.rail.get_section(1)
        sections = self.rail.get_sections(1, {'suite_id': 1, })
        '''

        '''
        To Be Added:
        ------------
        POST actions
        '''
