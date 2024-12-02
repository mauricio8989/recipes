from unittest import TestCase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

    def test_first_range_is_static_if_current_page_is_less_than_middlwe_page(self):  # noqa:E501
        # Current page = 1 - qty page = 2 middlwe page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1
        )
        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

        # Current page = 2 - qty page = 2 middlwe page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2
        )
        self.assertEqual([1, 2, 3, 4], pagination["pagination"])

        # Current page = 3 - qty page = 2 middlwe page = 3
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3
        )
        self.assertEqual([2, 3, 4, 5], pagination["pagination"])

        # Current page = 4 - qty page = 2 middlwe page = 4
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4
        )
        self.assertEqual([3, 4, 5, 6], pagination["pagination"])

    def test_make_sure_middle_ranges_are_correct(self):
        # Current page = 10 - qty page = 2 middlwe page = 10
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10
        )
        self.assertEqual([9, 10, 11, 12], pagination["pagination"])

        # Current page = 14 - qty page = 2 middlwe page = 14
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=14
        )
        self.assertEqual([13, 14, 15, 16], pagination["pagination"])

    def test_make_sure_last_range_is_static_if_current_page_is_greater_than_middlwe_page(self):  # noqa:E501
        # Current page = 19 - qty page = 2 middlwe page = 19
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19
        )
        self.assertEqual([17, 18, 19, 20], pagination["pagination"])

        # Current page = 20 - qty page = 2 middlwe page = 19
        # HERE RANGE SHOULD CHANGE
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20
        )
        self.assertEqual([17, 18, 19, 20], pagination["pagination"])
