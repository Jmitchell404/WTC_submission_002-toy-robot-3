import unittest
import robot
import sys
from unittest.mock import patch
from io import StringIO

class TestRobot(unittest.TestCase):
    @patch("sys.stdin", StringIO("Of\noff\n"))
    def test_commands_exist(self):
        result = 'off'
        self.assertEqual(result,'off')

    def test_commands_upper(self):
        result = 'OFF'
        self.assertEqual(result,'OFF')

    def test_commands_camelcase(self):
        result = 'Off'
        self.assertEqual(result,'Off')

    @patch("sys.stdin", StringIO("hel\nhelp\n"))
    def test_gets_commands_exist(self):
        result = 'help'
        self.assertEqual(result,'help')
    
    
    def test_validate_commands(self):
        result = ['off','help','forward 10'.split()]
        self.assertEqual(robot.valid_command('off'),True)


    @patch("sys.stdin", StringIO("forward 10\nforward 10\n"))
    def test_forward_function_validation(self):
        result = ['off','help','forward 10'.split()]
        self.assertTrue(robot.move_forward('forward',10),True)


    @patch("sys.stdin", StringIO("backward 10\n backward 10\n"))
    def test_move_backward(self):
        result = ['off','help','backward 10'.split()]
        self.assertTrue(robot.move_backward('backward', 10), True)

    
    @patch("sys.stdin", StringIO("10,10\n0,10"))
    def test_tracking_robot_position(self):
        self.assertFalse(robot.show_position("0,10"),True)

    @patch("sys.stdin", StringIO("left,10\nleft,10"))
    def test_robot_left_command(self):
        self.assertTrue(robot.move_left('left 10'),True)


    @patch("sys.stdin", StringIO("right,10\nright,10"))
    def test_robot_right_command(self):
        self.assertTrue(robot.move_right('right 10'),True)


    @patch("sys.stdin", StringIO("Hal\nsprint 5\noff\n"))
    def test_sprint(self):
        output = " > Hal moved forward by 1 steps."
        robot_name = "Hal"
        steps = 5
        self.assertEqual(robot.move_sprint(robot_name,steps)[1],output)


    @patch("sys.stdin", StringIO("sprit,3\nsprint,4"))
    def test_limit_area(self):
        self.assertTrue(robot.move_sprint('sprint',6),False)


    @patch("sys.stdin", StringIO("forward 10\nback 2"))
    def test_add_commands_history(self):
        robot.history = []
        actual_output = robot.add_commands_history('forward')
        self.assertEqual(actual_output,['forward'])


    @patch("sys.stdin", StringIO("hal\nforward\nreplay"))
    def test_replay_command(self):
        command = 'replayed 1 commands'
        robot_name = "hal"
        actual_output = robot.replay(command,robot_name)
        self.assertEqual(actual_output[0],True)
        self.assertTrue(actual_output[1],True)