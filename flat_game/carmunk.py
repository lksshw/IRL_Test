import sys, random, math
import pygame
from pygame.locals import *
import pymunk
import pymunk.pygame_util
from pygame.color import THECOLORS
from pymunk.pygame_util import DrawOptions as draw
from pymunk.vec2d import Vec2d
import numpy as np



width = 1600
height = 950
pygame.init()
screen = pygame.display.set_mode((1600, 950))
pygame.display.set_caption("INVOKER")
clock = pygame.time.Clock()


screen.set_alpha(None)

flag = 1
show_sensors = flag
draw_screen = flag

class GameState:
    def __init__(self, weights):
        self.ticks_to_next_ball = 10
        self.col = 'green'
        self.W = weights
        self.space = pymunk.Space()
        self.space.gravity = (0.0, -900.0)
        self.create_car(100, 200, 10)
        self.ball_shape = self.Signal()
        self.ticks_to_next_ball -= 1
        if (self.ticks_to_next_ball <= 0):
            self.ticks_to_next_ball = 500
            self.ball_shape = self.Signal()
            self.col = self.ball_shape

        self.num_steps = 0
        self.num_obstacles_type = 4
        self.add_rot()
        static = [
            pymunk.Segment(self.space.static_body, (0, 1), (0, height), 1),
            pymunk.Segment(self.space.static_body, (1, height), (width, height), 1),
            pymunk.Segment(self.space.static_body, (width - 1, height), (width - 1, 1), 1),
            pymunk.Segment(self.space.static_body, (1, 1), (width, 1), 1)]

        for s in static:
            s.friction = 1.
            s.group = 1
            s.collision_type = 1
            s.color = THECOLORS['red4']
        self.space.add(static)


        self.obstacles = []

        self.obstacles.append(self.create_obstacle([50, 90], [50, 670], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([310, 670], [50, 670], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([170, 90], [170, 600], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([130, 600], [200, 600], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([200, 350], [200, 600], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([310, 570], [310, 670], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([270, 570], [310, 570], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([270, 570], [270, 470], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([200, 350], [350, 350], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([270, 470], [700, 470], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([350, 350], [700, 350], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([700, 470], [700, 890], 2, "orange"))
        self.obstacles.append(self.create_obstacle([700, 350], [700, 20], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([850, 470], [850, 770], 2, "orange"))
        self.obstacles.append(self.create_obstacle([850, 470], [850, 350], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([850, 350], [850, 110], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([850, 600], [800, 600], 2, "orange"))
        self.obstacles.append(self.create_obstacle([700, 800], [750, 800], 2, "orange"))
        self.obstacles.append(self.create_obstacle([700, 250], [750, 250], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([800, 150], [850, 150], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([700, 890], [1570, 890], 2, "orange"))
        self.obstacles.append(self.create_obstacle([850, 770], [1570, 770], 2, "orange"))
        self.obstacles.append(self.create_obstacle([1170, 860], [1170, 890], 2, "orange"))
        self.obstacles.append(self.create_obstacle([1170, 770], [1170, 800], 2, "orange"))
        self.obstacles.append(self.create_obstacle([1400, 770], [1400, 830], 2, "orange"))
        self.obstacles.append(self.create_obstacle([1570, 770], [1570, 890], 2, "orange"))
        self.obstacles.append(self.create_obstacle([850, 110], [1300, 110], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([700, 20], [1450, 20], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1450, 20], [1450, 500], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1300, 110], [1300, 400], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1100, 400], [1300, 400], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1100, 500], [1450, 500], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1100, 500], [1100, 400], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1300, 500], [1300, 470], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1300, 350], [1370, 350], 2, "yellow"))
        self.obstacles.append(self.create_obstacle([1400, 150], [1450, 150], 2, "yellow"))

    def create_obstacle(self, xy1, xy2, r, color):

        c_body = pymunk.Body(1, pymunk.inf, body_type = pymunk.Body.STATIC)
        c_shape = pymunk.Segment(c_body, xy1, xy2, r)
        c_shape.friction = 1.
        c_shape.group = 1
        c_shape.collision_type = 1
        c_shape.color = THECOLORS[color]
        self.space.add(c_body, c_shape)
        return c_body

    def add_rot(self):

        rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body.position = (500, 410)

        # 1st rotation
        body = pymunk.Body(10, 10000)
        body.position = (500, 410)
        l1 = pymunk.Segment(body, (-55, 0), (55.0, 0.0), 2.0)
        l1.color = THECOLORS['yellow']
        # 2nd rotation
        rotation_center_body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
        rotation_center_body2.position = (770, 410)

        body2 = pymunk.Body(10, 10000)
        body2.position = (770, 410)
        l2 = pymunk.Segment(body2, (-55, 0), (55.0, 0.0), 2.0)
        l2.color = THECOLORS['yellow']

        rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
        rotation_center_joint2 = pymunk.PinJoint(body2, rotation_center_body2, (0, 0), (0, 0))

        tw = pymunk.SimpleMotor(body, rotation_center_body, 0.7)
        tw2 = pymunk.SimpleMotor(body2, rotation_center_body2, -0.7)

        self.space.add(l1, l2, body, body2, rotation_center_joint, rotation_center_joint2, tw, tw2)
        return l1, l2


    def Signal(self):
        """Add a ball to the given space at a random position"""
        mass = 1
        radius = 5
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia, body_type=pymunk.Body.STATIC)
        body.position = 1000, 830
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.color = THECOLORS[self.col]
        self.space.add(body, shape)
        if (self.col == 'green'):
            return 'red'
        elif (self.col == 'red'):
            return 'green'

    def create_car(self, x, y, r):
        inertia = pymunk.moment_for_circle(1, 0, 14, (0, 0))
        self.car_body = pymunk.Body(1, inertia)
        self.car_body.position = x, y
        self.car_shape = pymunk.Circle(self.car_body, r)
        self.car_body.mass = 10
        self.car_shape.color = THECOLORS["green"]
        self.car_shape.elasticity = 1.0
        self.car_body.angle = 1.4
        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.apply_impulse_at_world_point(driving_direction)
        self.space.add(self.car_body, self.car_shape)



    def frame_step(self, action):
        if action == 0:  # Turn left.
            self.car_body.angle -= .3
        elif action == 1:  # Turn right.
            self.car_body.angle += .3



        driving_direction = Vec2d(1, 0).rotated(self.car_body.angle)
        self.car_body.velocity = 100 * driving_direction

        # Update the screen and stuff.
        draw_options = pymunk.pygame_util.DrawOptions(screen)
        screen.fill((0, 0, 0))
        self.space.debug_draw(draw_options)

        self.space.step(1/50.0)
        if draw_screen:
            pygame.display.flip()
        clock.tick()


        # Get the current location and the readings there.
        x, y = self.car_body.position
        readings = self.get_sonar_readings(x, y, self.car_body.angle)

        # Set the reward.
        # Car crashed when any reading == 1
        if self.car_is_crashed(readings):
            self.crashed = True
            readings.append(1)
            self.recover_from_crash(driving_direction)
        else:
            readings.append(0)

        reward = np.dot(self.W, readings)
        state = np.array([readings])

        self.num_steps += 1

        return reward, state, readings

    def move_obstacles(self):
        # Randomly move obstacles around.
        for obstacle in self.obstacles:
            speed = random.randint(1, 5)
            direction = Vec2d(1, 0).rotated(self.car_body.angle + random.randint(-2, 2))
            obstacle.velocity = speed * direction

    def move_cat(self):
        speed = random.randint(20, 200)
        self.cat_body.angle -= random.randint(-1, 1)
        direction = Vec2d(1, 0).rotated(self.cat_body.angle)
        self.cat_body.velocity = speed * direction

    def car_is_crashed(self, readings):
        if readings[0] >= 0.96 or readings[1] >= 0.96 or readings[2] >= 0.96:
            return True
        else:
            return False

    def recover_from_crash(self, driving_direction):
        """
        We hit something, so recover.
        """
        while self.crashed:
            # Go backwards.
            self.car_body.velocity = -100 * driving_direction
            self.crashed = False
            for i in range(10):
                self.car_body.angle += .2  # Turn a little.
                draw_options = pymunk.pygame_util.DrawOptions(screen)
                self.space.debug_draw(draw_options)
                self.space.step(1 / 50.0)
                if draw_screen:
                    pygame.display.flip()
                clock.tick()



    def get_sonar_readings(self, x, y, angle):
        readings = []


        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left

        obstacleType = []
        obstacleType.append(self.get_arm_distance(arm_left, x, y, angle, 0.75)[1])
        obstacleType.append(self.get_arm_distance(arm_middle, x, y, angle, 0)[1])
        obstacleType.append(self.get_arm_distance(arm_right, x, y, angle, -0.75)[1])

        ObstacleNumber = np.zeros(self.num_obstacles_type)

        for i in obstacleType:
            if i == 0:
                ObstacleNumber[0] += 1
            elif i == 1:
                ObstacleNumber[1] += 1
            elif i == 2:
                ObstacleNumber[2] += 1
            elif i == 3:
                ObstacleNumber[3] += 1

        # Rotate them and get readings.
        readings.append(1.0 - float(self.get_arm_distance(arm_left, x, y, angle, 0.75)[0] / 39.0))  # 39 = max distance
        readings.append(1.0 - float(self.get_arm_distance(arm_middle, x, y, angle, 0)[0] / 39.0))
        readings.append(1.0 - float(self.get_arm_distance(arm_right, x, y, angle, -0.75)[0] / 39.0))
        readings.append(float(ObstacleNumber[0] / 3.0))
        readings.append(float(ObstacleNumber[1] / 3.0))
        readings.append(float(ObstacleNumber[2] / 3.0))
        readings.append(float(ObstacleNumber[3] / 3.0))

        if show_sensors:
            pygame.display.update()

        return readings

    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1

            # Move the point to the right spot.
            rotated_p = self.get_rotated_point(
                x, y, point[0], point[1], angle + offset
            )

            # Check if we've hit something. Return the current i (distance)
            # if we did.
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 \
                    or rotated_p[0] >= width or rotated_p[1] >= height:
                return [i, 3]  # Sensor is off the screen, return 3 for wall obstacle
            else:
                obs = screen.get_at(rotated_p)
                temp = self.get_track_or_not(obs)
                if temp != 0:
                    return [i, temp]  # sensor hit a round obstacle, return the type of obstacle

            if show_sensors:
                pygame.draw.circle(screen, (255, 255, 255), (rotated_p), 2)

        # Return the distance for the arm.
        return [i, 0]  # sensor did not hit anything return 0 for black space

    def make_sonar_arm(self, x, y):
        spread = 8  # Default spread.
        distance = 7  # Gap before first sensor.
        arm_points = []
        # Make an arm. We build it flat because we'll rotate it about the
        # center later.
        for i in range(1, 40):
            arm_points.append((distance + x + (spread * i), y))

        return arm_points

    def get_rotated_point(self, x_1, y_1, x_2, y_2, radians):
        # Rotate x_2, y_2 around x_1, y_1 by angle.
        x_change = (x_2 - x_1) * math.cos(radians) + \
                   (y_2 - y_1) * math.sin(radians)
        y_change = (y_1 - y_2) * math.cos(radians) - \
                   (x_1 - x_2) * math.sin(radians)
        new_x = x_change + x_1
        new_y = height - (y_change + y_1)
        return int(new_x), int(new_y)

    # def get_track_or_not(self, reading):
    #     if reading == THECOLORS['black']:
    #         return 0
    #     else:
    #         return 1

    def get_track_or_not(self, reading):  # basically differentiate b/w the objects the car views.
        if reading == THECOLORS['yellow']:
            return 1  # Sensor is on a yellow obstacle
        elif reading == THECOLORS['orange']:
            return 2
            # Sensor is on brown obstacle
        else:
            return 0  # for black


if __name__ == "__main__":
    weights = [1, 1, 1, 1, 1, 1, 1, 1]
    game_state = GameState(weights)
    while True:
        screen.fill((0,0,0))
        game_state.frame_step((random.randint(0, 2)))

