from unittest import mock

from django.test import SimpleTestCase, override_settings

from macantine import tasks


class DbtRunTest(SimpleTestCase):
    @override_settings(ENVIRONMENT="dev")
    @mock.patch("macantine.tasks.dbtRunner")
    def test_dbt_run_targets_dev_outside_prod(self, dbt_runner_mock):
        dbt_runner_mock.return_value.invoke.return_value = mock.Mock(success=True, exception=None)

        result = tasks.dbt_run()

        self.assertIn("dbt run completed", result)
        calls = dbt_runner_mock.return_value.invoke.call_args_list
        self.assertEqual(len(calls), 2)
        deps_args, run_args = calls[0].args[0], calls[1].args[0]
        self.assertEqual(deps_args[0], "deps")
        self.assertEqual(run_args[0], "run")
        self.assertIn("dev", deps_args)
        self.assertIn("dev", run_args)

    @override_settings(ENVIRONMENT="prod")
    @mock.patch("macantine.tasks.dbtRunner")
    def test_dbt_run_targets_prod_in_prod(self, dbt_runner_mock):
        dbt_runner_mock.return_value.invoke.return_value = mock.Mock(success=True, exception=None)

        tasks.dbt_run()

        run_args = dbt_runner_mock.return_value.invoke.call_args_list[1].args[0]
        self.assertIn("prod", run_args)

    @mock.patch("macantine.tasks.dbtRunner")
    def test_dbt_run_raises_dbt_exception_on_failure(self, dbt_runner_mock):
        dbt_error = RuntimeError("boom")
        dbt_runner_mock.return_value.invoke.return_value = mock.Mock(success=False, exception=dbt_error)

        with self.assertRaises(RuntimeError) as ctx:
            tasks.dbt_run()
        self.assertIs(ctx.exception, dbt_error)

        # "run" should never be attempted if "deps" already failed
        dbt_runner_mock.return_value.invoke.assert_called_once()

    @mock.patch("macantine.tasks.dbtRunner")
    def test_dbt_run_raises_generic_error_when_no_exception_attached(self, dbt_runner_mock):
        dbt_runner_mock.return_value.invoke.return_value = mock.Mock(success=False, exception=None)

        with self.assertRaises(RuntimeError):
            tasks.dbt_run()
