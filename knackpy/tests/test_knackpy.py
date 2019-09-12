import pytest

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
"""

import pdb

class TestKnackpy:
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