import pygame as pygame
from pygame import Color
from core.lib.maps.utils import constants as map_c
from math import sin, cos, pi, sqrt, atan2


class RoadNetworkRenderer:
    def __init(self):
        return

    def draw(self, road_net, screen):
        draw_tools = DrawTools(screen)
        for road in road_net.get_roads():
            road = road[2]["object"]
            draw_tools.add_road(road)
        draw_tools.draw_roads(road_width=25)

    def draw_specific_road(self, road, screen):
        draw_tools = DrawTools(screen)
        # draw_tools.draw_specific_road(road)
        pts = road.bounding_polygon.exterior.coords.xy
        # print(pts)
        pygame.draw.polygon(screen, (0, 255, 0), list(zip(*pts)), 3)


class CarRenderer:
    def __init(self):
        return

    def draw(self, car, screen):

        # polygon = car.get_car_bounding_box()
        # pointslist = [(x,y) for x,y in zip(polygon.exterior.coords.xy[0],polygon.exterior.coords.xy[1])]
        # pygame.draw.polygon(screen, (0, 255, 0), pointslist, 3)
        #
        polygon_front = car.get_car_bounding_box_front()
        pointslist = [(x,y) for x,y in zip(polygon_front.exterior.coords.xy[0],polygon_front.exterior.coords.xy[1])]
        pygame.draw.polygon(screen, (0, 255, 0), pointslist, 3)

        # polygon_back = car.get_car_bounding_box_back()
        # pointslist = [(x,y) for x,y in zip(polygon_back.exterior.coords.xy[0],polygon_back.exterior.coords.xy[1])]
        # pygame.draw.polygon(screen, (255, 0, 0), pointslist, 3)

        # polygon_adj_right = car.get_car_bounding_box_adj(map_c.LANE_WIDTH,direction='right')
        # polygon_adj_left = car.get_car_bounding_box_adj(map_c.LANE_WIDTH, direction='left')

        # pointslist = [(x,y) for x,y in zip(polygon_adj_left.exterior.coords.xy[0],polygon_adj_left.exterior.coords.xy[1])]
        # pygame.draw.polygon(screen, (0, 0, 255), pointslist, 3)
        # pointslist = [(x,y) for x,y in zip(polygon_adj_right.exterior.coords.xy[0],polygon_adj_right.exterior.coords.xy[1])]
        # pygame.draw.polygon(screen, (0, 0, 255), pointslist, 3)

        draw_rect = car.image.get_rect().move(
            car.pos.x - car.image_w / 2,
            car.pos.y - car.image_h / 2
        )
        screen.blit(car.image, draw_rect)


class DrawTools:
    def __init__(self, screen):
        self.objects = []
        self.roads = []
        self.screen = screen

    def add_road(self, road):
        self.roads.append(road)
        return road

    def draw_objects(self):
        [self.__draw_polygon(list(o.poly.exterior.coords)) for o in self.objects]
        return

    def __get_road_segment_bounding_polygon(self, road, road_width):
        # TODO: use heading attr on edge
        heading = road.heading
        xls_start = []
        yls_start = []
        xls_end = []
        yls_end = []
        lane_width = road.lane_width
        no_of_lanes = road.no_of_lanes
        for lane in range(no_of_lanes+1):
            xls_start.append((lane * lane_width) * cos(heading + pi / 2) + (no_of_lanes * lane_width / 2.0) * cos(heading - pi / 2) + road.start_node.X)
            yls_start.append((lane * lane_width) * sin(heading + pi / 2) + (no_of_lanes * lane_width / 2.0) * sin(heading - pi / 2) + road.start_node.Y)
            xls_end.append((lane * lane_width) * cos(heading + pi / 2) + (no_of_lanes * lane_width / 2.0) * cos(heading - pi / 2) + road.end_node.X)
            yls_end.append((lane * lane_width) * sin(heading + pi / 2) + (no_of_lanes * lane_width / 2.0) * sin(heading - pi / 2) + road.end_node.Y)
        return xls_start, yls_start, xls_end, yls_end

    def draw_roads(self, road_width=10):
        for road in self.roads:
            xls_start, yls_start, xls_end, yls_end = self.__get_road_segment_bounding_polygon(road, road_width)
            l = list(zip(xls_start, yls_start, xls_end, yls_end))
            xsu, ysu, xeu, yeu = l[0]
            xsl, ysl, xel, yel = l[-1]
            self.__draw_polygon(((xsu, ysu), (xeu, yeu), (xel, yel), (xsl, ysl)))
        for road in self.roads:
            xls_start, yls_start, xls_end, yls_end = self.__get_road_segment_bounding_polygon(road, road_width)
            if road.type == "straight":
                for xs, ys, xe, ye in zip(xls_start, yls_start, xls_end, yls_end):
                    self.__draw_dashed_line(((xs, ys), (xe, ye)))
            else:
                for xs, ys, xe, ye in zip(xls_start, yls_start, xls_end, yls_end):
                    self.__draw_dashed_line(((xs, ys), (xe, ye)), (140, 140, 140))
        self.__draw_traffic_signals()
        return

    def draw_specific_road(self, road):
        pts = road.bounding_polygon.exterior.coords.xy
        print(pts)
        self.__draw_polygon(coords=list(zip(*pts)), wallcolor=Color(255, 0, 0))
        # pygame.draw.polygon(screen, (0, 255, 0), list(zip(*pts)), 3)


    def __draw_traffic_signals(self, road_width=10):
        for road in self.roads:
            xls_start, yls_start, xls_end, yls_end = self.__get_road_segment_bounding_polygon(road, road_width)
            i = 1
            while i < len(xls_end):
                if road.end_node.traffic_signals[i-1]:
                    if road.end_node.traffic_signals[i-1].color == 'r':
                        self.__draw_line(((xls_end[i-1], yls_end[i-1]), (xls_end[i], yls_end[i])),
                                         wallcolor=Color(255, 0, 0))
                    elif road.end_node.traffic_signals[i-1].color == 'g':
                        self.__draw_line(((xls_end[i - 1], yls_end[i - 1]), (xls_end[i], yls_end[i])),
                                         wallcolor=Color(0, 255, 0))
                    else:
                        self.__draw_line(((xls_end[i - 1], yls_end[i - 1]), (xls_end[i], yls_end[i])),
                                         wallcolor=Color(255, 255, 0))
                i+=1
        return

    def __draw_line(self, coords, wallcolor=Color(255, 255, 255)):
        pygame.draw.line(self.screen, wallcolor, coords[0], coords[1], 3)
        return coords

    def __draw_dashed_line(self, coords, wallcolor=(255, 255, 255)):
        length = sqrt((coords[1][1]-coords[0][1])**2 + (coords[1][0]-coords[0][0])**2)
        dash_length = 5.0
        slope = atan2((coords[1][1]-coords[0][1]), (coords[1][0]-coords[0][0]))
        for index in range(0, int(length/dash_length), 2):
            start = (coords[0][0] + (index * dash_length)*cos(slope), coords[0][1] +
                     (index * dash_length)*sin(slope))
            end = (coords[0][0] + ((index+1) * dash_length)*cos(slope), coords[0][1] +
                   ((index+1) * dash_length)*sin(slope))
            pygame.draw.line(self.screen, wallcolor, start, end, 1)

    def __draw_polygon(self, coords, wallcolor=Color(100, 100, 100)):
        pygame.draw.polygon(self.screen, wallcolor, coords)
        return coords

    def draw_text(self, car, road_net):
        myfont = pygame.font.SysFont(None, 30)
        current_road = road_net.get_road((car.current_node.id, car.next_node.id))
        if current_road.get_lane(car.x, car.y):
            current_lane = current_road.lanes[current_road.get_lane(car.x, car.y)]
            textsurface = myfont.render(current_lane.name, False, (0, 0, 0))
            self.screen.blit(textsurface, (0, 0))
