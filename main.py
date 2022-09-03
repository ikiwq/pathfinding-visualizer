import sys

from queue import PriorityQueue

import pygame.event

from Node import *
from Utils import *

ROWS = 32
VIDEOWH = 800

class AlgorithVisualizer:
    def __init__(self):
        self.VideoWH = VIDEOWH
        self.Rows = ROWS
        self.algorithm = None
        self.Init()
        self.RunMenu()

    def Init(self):
        pg.init()
        pg.font.init()
        self.ButtonText = pg.font.Font("Fonts/PressStart2P.ttf", 18)
        self.TitleText = pg.font.Font("Fonts/PressStart2P.ttf", 37)
        self.window = pg.display.set_mode((self.VideoWH, self.VideoWH))
        self.Clock = pg.time.Clock()

        self.NodeWH = self.VideoWH // self.Rows
        self.nodeGroup = pg.sprite.Group()

    def buildNodes(self):
        self.map = []
        for i in range(self.Rows):
            self.map.append([])
            for j in range(self.Rows):
                node = Node((i*self.NodeWH, j*self.NodeWH), self.NodeWH, WHITE, self.Rows)
                self.nodeGroup.add(node)
                self.map[i].append(node)

    def drawGrid(self):
        for i in range(self.Rows):
            pg.draw.line(self.window, BLACK, (0, i*self.NodeWH), (self.VideoWH, i*self.NodeWH))
            pg.draw.line(self.window, BLACK, (i*self.NodeWH, 0), (i*self.NodeWH, self.VideoWH))

    def getNodeOnClick(self):
        x, y = pg.mouse.get_pos()
        xpos, ypos = x//self.NodeWH, y//self.NodeWH
        return self.map[xpos][ypos]

    def RunMenu(self):
        running = True
        deg = 0
        c = 1
        while running:
            self.Clock.tick(60)
            self.window.fill(BLACK)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_DOWN:
                        if c<2:
                            c+=1
                    if event.key == pg.K_UP:
                        if c>1:
                            c-=1
                    if event.key == pg.K_SPACE:
                        if c==1:
                            self.algorithm = "astar"
                            self.AlgoVisualizer()
                        elif c==2:
                            self.algorithm = "dijkstra"
                            self.AlgoVisualizer()

                        running = False

            deg += 0.03

            if(c==1):
                drawRectText(self.window, 250 , 326+ math.cos(deg)*7, 300, 75, GREY, self.ButtonText, "A*")
                drawRectText(self.window, 250 , 451+math.sin(deg)*7, 300, 75, WHITE, self.ButtonText, "Dijkstra")
            elif(c==2):
                drawRectText(self.window, 250, 326 + math.cos(deg) * 7, 300, 75, WHITE, self.ButtonText, "A*")
                drawRectText(self.window, 250, 451 + math.sin(deg) * 7, 300, 75, GREY, self.ButtonText, "Dijkstra")

            drawTitle(self.window, 0,50, self.TitleText, "Algorithm Visualizer", WHITE)
            pg.display.flip()


    def AlgoVisualizer(self):
        running = True
        self.buildNodes()

        self.Start = None
        self.End = None

        hasRun = False
        while running:
            self.Clock.tick(60)
            self.window.fill(BLACK)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

                if pg.mouse.get_pressed()[0] and hasRun is False:
                    node = self.getNodeOnClick()
                    if not self.Start:
                        self.Start = node
                        node.make_start()
                    elif not self.End and not node.is_start():
                        self.End = node
                        node.make_end()
                    elif not node.is_start() and not node.is_end():
                        node.make_barrier()

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        if hasRun == False:
                            if self.Start is not None and self.End is not None:
                                hasRun = True

                                for row in self.map:
                                    for node in row:
                                        node.inspect_neighbours(self.map)

                                if(self.algorithm == "astar"):
                                    self.runAStar()
                                if(self.algorithm == "dijkstra"):
                                    self.rundijkstra()
                        else:
                            self.RunMenu()


                if pg.mouse.get_pressed()[2]:
                    node = self.getNodeOnClick()
                    if node.is_start():
                        self.Start = None
                        node.make_open()
                    if node.is_end():
                        self.End = None
                        node.make_open()
                    else:
                        node.make_open()

            self.nodeGroup.update()
            self.nodeGroup.draw(self.window)
            self.drawGrid()
            pg.display.flip()

    def runAStar(self):
        self.Start.gscore = 0
        self.Start.hscore = HeurDist(self.Start.get_pos(), self.End.get_pos())

        self.nodeGroup.update()

        open_set = PriorityQueue()
        open_set.put((self.Start.fscore, self.Start))

        open_set_arr = {self.Start}

        algrunning = True

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            current = open_set.get()[1]
            open_set_arr.remove(current)

            if current == self.End:
                self.gen_path(current)
                return True

            for neighbor in current.neighbours:
                tempg = current.gscore + 1
                if tempg < neighbor.gscore:
                    neighbor.cameFrom = current
                    neighbor.gscore = tempg
                    neighbor.hscore = HeurDist(neighbor.get_pos(), self.End.get_pos())
                    self.nodeGroup.update()
                    if neighbor not in open_set_arr:
                        open_set.put((neighbor.fscore, neighbor))
                        open_set_arr.add(neighbor)
                        neighbor.make_explor()

            if current != self.Start and current != self.End:
                current.make_explored()

            self.nodeGroup.update()
            self.nodeGroup.draw(self.window)
            self.drawGrid()

            pg.display.flip()

        return False

    def gen_path(self, current):
        if current.cameFrom == self.Start:
            return True
        else:
            current.cameFrom.make_path()
            self.nodeGroup.update()
            self.nodeGroup.draw(self.window)
            self.drawGrid()
            pg.display.flip()
            self.gen_path(current.cameFrom)


    def rundijkstra(self):
        self.Start.gscore = 0
        open_set = PriorityQueue()
        open_set.put((self.Start.gscore, self.Start))
        open_set_arr = {self.Start}

        while not open_set.empty():
            for event in pygame.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            current = open_set.get()[1]
            open_set_arr.remove(current)

            if current == self.End:
                self.gen_path(current)
                return True

            for neighbor in current.neighbours:
                tempg = current.gscore+1
                if tempg < neighbor.gscore:
                    neighbor.gscore = tempg
                    neighbor.cameFrom = current
                    if neighbor not in open_set_arr:
                        open_set.put((neighbor.gscore, neighbor))
                        open_set_arr.add(neighbor)
                        neighbor.make_explor()

            if current != self.Start and current != self.End:
                current.make_explored()

            self.nodeGroup.update()
            self.nodeGroup.draw(self.window)
            self.drawGrid()
            pg.display.flip()



def main():
    algo = AlgorithVisualizer()

main()
