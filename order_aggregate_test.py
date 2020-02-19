import unittest

from order_aggregate import Order, OrderCreated, StatusChanged


class OrderAggregateTest(unittest.TestCase):
    def test_should_create_order(self):
        order = Order.create(user_id=1)
        self.assertEqual(order.changes, [OrderCreated(user_id=1)])
        pass

    def test_should_emit_a_status_change(self):
        order = Order.create(user_id=2)
        order.set_status("shipped")
        self.assertEqual(order.changes, [OrderCreated(2), StatusChanged("shipped")])
