import pydantic.v1  # noqa: F401

# pydantic.v1's ConstrainedDate definition conflicts with freezegun's patched
# datetime.date if imported for the first time while a @freeze_time block is
# active (dbt-core pulls in pydantic.v1 via macantine.tasks). Importing it
# here, before any test (and any freeze_time) runs, avoids that metaclass
# conflict regardless of test order.
