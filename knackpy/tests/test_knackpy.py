import pytest
import pdb

from test_secrets import AUTH
from test_config import APP

"""
Tests:
- [x] view + scene 
- [x] object
- [x] both view + scene + object
- [x] page limit
- [x] rows per page
- public view/scene
- all params
- all methods
- datestings
- each fieldtype
- mutilple attachments
- downloads
- insert
- update
- delete (need this method)
- csv
- insert connected record
- populate connection field
"""

class TestKnackpy:

    def test_record_update_datetime(self):
        import knackpy
        import datetime

        module = APP["all_fields"]

        now = int(datetime.datetime.now().timestamp()) * 1000
        
        # this updates the record with a current *UTC* timestamp into PYTEST_MODIFIED_DATE
        record = {
            'field_37': now, # PYTEST_MODIFIED_DATE
            'id': '5d7964422d7159001659b27a'
        }

        res = knackpy.record(
            record,
            obj_key=module["obj"],
            app_id=AUTH["app_id"],
            api_key=AUTH["api_key"],
            id_key="id",
            method="update"
        )

        now_knack = res["field_37_raw"]["unix_timestamp"]

        # check that updated value is within 1 minute (60k milliseconds) of update
        # (Knack rounds to nearest minute)
        assert abs(now - now_knack) < 60000


    def test_record_insert_datetime(self):
        import knackpy
        import datetime

        module = APP["all_fields"]

        now = int(datetime.datetime.now().timestamp()) * 1000
        
        # this inserts the record with a current *UTC* timestamp into PYTEST_MODIFIED_DATE
        record = {
            'field_37': now, # PYTEST_MODIFIED_DATE
            'field_38' : True # PYTEST_TEST_RECORD
        }

        res = knackpy.record(
            record,
            obj_key=module["obj"],
            app_id=AUTH["app_id"],
            api_key=AUTH["api_key"],
            id_key="id",
            method="create"
        )

        now_knack = res["field_37_raw"]["unix_timestamp"]

        pdb.set_trace()
        # check that updated value is within 1 minute (60k milliseconds) of update
        # (Knack rounds to nearest minute)
        assert abs(now - now_knack) < 60000


    def test_record_delete(self):
        """
        I have no idea how to *unit test* a record delete. I guess we could insert
        records in the setup? What if the setup fails? Hrumph.
        Setup seems like the right way to handle this.
        This means using pytest fixtures.
        """
        import knackpy
        
        module = APP["all_fields"]

        # get all knackpy test records

        kn = Knack(
            obj=module["obj"],
            app_id=AUTH["app_id"],
            api_key=AUTH["api_key"]
        )

        res = knackpy.record(
            record,
            obj_key=module["obj"],
            app_id=AUTH["app_id"],
            api_key=AUTH["api_key"],
            id_key="id",
            method="create"
        )

        now_knack = res["field_37_raw"]["unix_timestamp"]

        pdb.set_trace()
        # check that updated value is within 1 minute (60k milliseconds) of update
        # (Knack rounds to nearest minute)
        assert abs(now - now_knack) < 60000

    def test_scene_view_with_api_key(self):
        # create a Knack instance from a scene key + view key
        # also tests page limit and rows per page
        from knackpy import Knack

        module = APP["all_fields"]

        kn = Knack(
            scene=module["scene"],
            view=module["view"],
            ref_obj=module["ref_obj"],
            app_id=AUTH["app_id"],
            api_key=AUTH["api_key"],
            page_limit=1,
            rows_per_page=1,
        )

        assert len(kn.data) == 1


    def test_object_api_key(self):
        # create a Knack instance from an object key
        from knackpy import Knack

        module = APP["all_fields"]

        kn = Knack(
            obj=module["obj"],
            app_id=AUTH["app_id"],
            api_key=AUTH["api_key"],
            page_limit=1,
            rows_per_page=1,
        )

        assert len(kn.data) > 0

    def test_object_view_scene_error(self):
        # an instance must have either an object or a scene/view, but not both
        from knackpy import Knack

        module = APP["all_fields"]

        with pytest.raises(Exception) as excinfo:

            assert Knack(
                obj=module["obj"],
                scene=module["scene"],
                view=module["view"],
                app_id=AUTH["app_id"],
                api_key=AUTH["api_key"],
                page_limit=1,
                rows_per_page=1,
            )

            # check for text of expected generic error message
        assert "not both" in str(excinfo.value).lower()
