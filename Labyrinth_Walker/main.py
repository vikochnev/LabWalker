#Обучающий проект, представляющий собой игру, в которой персонаж должен дойти от начальной точки до конечной в лабиринте
#Возможно передвижение либо клавишами, либо автоматическое посредством алгоритма поиска кратчайшего пути
#Движение возможно в горизонтальном и вертикальном направлении
#Карта лабиринта подгружается из файла
#Лабиринт состоит из пустых клеток и стен
#Условие победы - нахождение персонажа на тайле "конец"

import draw, labyrinth, pathfinder

lab = labyrinth.create_labyrinth("map.txt")
labyrinth_Walker = draw.Game()
labyrinth_Walker.set_board(lab)
labyrinth_Walker.play()
