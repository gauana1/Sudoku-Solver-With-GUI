import numpy as np
import pygame  
import copy
import random
import pygame_gui 
Window_width = 800
Window_height = 594
rows = 9
cols = 9
size = rows*cols
moves = []
default_coords = []
solved = np.array([[]])
for x in range(9):
    for y in range(9):
        moves.append((x,y))
moves_set = set(moves)
# pygame setup
def main():
    pygame.init()
    my_font1 = pygame.font.SysFont('Comic Sans MS', 40)
    my_font2 = pygame.font.SysFont('Comic Sans MS', 20)
    screen = pygame.display.set_mode((800, 594))
    pygame.display.set_caption("Sudoku Game")
    manager = pygame_gui.UIManager((800, 594))

    clock = pygame.time.Clock()
    running = True
    Easy = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 400), (100, 50)),text='Easy',manager=manager)
    Medium = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650, 475), (100, 50)),text='Medium',manager=manager)
    Hard = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((650,550), (100, 50)),text='Hard',manager=manager)
    solve_puzzle = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((625,250), (150, 50)),text='Solve Puzzle',manager=manager)
    Submit = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((625,100), (150, 50)),text='Submit Solution',manager=manager)
    screen.fill("white")
    drawgridlines(screen)
    board_active = 0
    click = False
    while running:
        display_text(screen, my_font2, "Select Difficulty:", (0,0,0), (700, 350))
        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        
        for event in pygame.event.get():
            time_delta = clock.tick(60)/1000.0
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and board_active == 1:
                position = pygame.mouse.get_pos()
                if(position[0] < 600 and position[1] < 600):
                    x = position[0]//66
                    y = position[1]//66
                    click = True
            if event.type == pygame.KEYDOWN and click:
                val = 0
                if event.key == pygame.K_1:
                    val = 1
                if event.key == pygame.K_2:
                    val = 2   
                if event.key == pygame.K_3:
                    val = 3
                if event.key == pygame.K_4:
                    val = 4
                if event.key == pygame.K_5:
                    val = 5
                if event.key == pygame.K_6:
                    val = 6
                if event.key == pygame.K_7:
                    val = 7
                if event.key == pygame.K_8:
                    val = 8
                if event.key == pygame.K_9:
                    val = 9 
                if event.key == pygame.K_DELETE:
                    val = 0
                insert(mat, (x,y), val)
                screen.fill("white")
                display_board(screen, my_font1,mat)
                drawgridlines(screen)
                click = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                screen.fill("white")
                if event.ui_element == Easy:
                    board_active = 1
                    mat = np.array([0]*size).reshape(rows,cols)
                    default_coords = []
                    solved = initialize_board(mat, "Easy")
                    drawgridlines(screen)
                    display_board(screen, my_font1,mat)
                elif event.ui_element == Medium:
                    board_active = 1
                    mat = np.array([0]*size).reshape(rows,cols)
                    default_coords = []
                    solved = initialize_board(mat, "Medium")
                    drawgridlines(screen)
                    display_board(screen, my_font1,mat)
                elif event.ui_element == Hard:
                    board_active = 1
                    mat = np.array([0]*size).reshape(rows,cols)
                    default_coords = []
                    solved = initialize_board(mat, "Hard")
                    drawgridlines(screen)
                    display_board(screen, my_font1,mat)
                elif event.ui_element == solve_puzzle:
                    board_active = 2
                    drawgridlines(screen)
                    display_board(screen, my_font1, solved)
                    mat = solved
                elif event.ui_element == Submit:
                    if game_over(mat):
                        display_text(screen, my_font2, "You Win!", (0,0,0), (700, 200))
                    else:
                        display_text(screen, my_font2, "Invalid Solution", (0,0,0), (700, 200))
                        drawgridlines(screen)
                        display_board(screen, my_font1, mat)
            manager.process_events(event)
            manager.update(time_delta)
        
       
        manager.draw_ui(screen)
            
        
        
        pygame.display.update()
        
        pygame.display.flip()

        # pygame.quit()
        clock.tick(60)  # limits FPS to 60
def insert(board, coord, val):

    if(coord not in default_coords):
        board[coord[0]][coord[1]] = val
def display_text(screen, font, words, color, center):
    text = font.render(words, True, color) 
    text_rect = text.get_rect(center = center)
    screen.blit(text, text_rect)
def drawgridlines(screen):
    block_size = 66
    for x in range(0,Window_width-200, block_size):
        pygame.draw.line(screen, (0,0,0), (x,0), (x, Window_height))
    for y in range(0, Window_height, block_size):
        pygame.draw.line(screen, (0,0,0), (0,y), (Window_height,y))

def initialize_board(board, level):
    count = 0 
    number = random.randint(5,17)
    temp_board = copy.deepcopy(board)
    moves_list = random.sample(list(moves_set),  number)
    while count < number: #populates the board with random moves (number times)
        for coord in moves_list: #one way to implement this is to take a random size from 1-20 and then take the solved version and give 10,20,30 random squares based off of difficulty
            val = random.randint(1,9)
            temp_board[coord[0]][coord[1]] = val
            if not check(temp_board): #if move is invalid, keep it in the moves_list
                temp_board[coord[0]][coord[1]] = 0 
            else:
                count+=1
                moves_list.remove((coord[0], coord[1]))
    solver(temp_board) #after the temp board is populated, solve it
    solved = temp_board
    if(level == "Easy"):
        real_board_moves = random.sample(list(moves_set), k = 40)
        for coord in real_board_moves:
            default_coords.append(coord)
            board[coord[0]][coord[1]] =  temp_board[coord[0]][coord[1]]
    elif(level == "Medium"):
        real_board_moves = random.sample(list(moves_set), k = 30)
        for coord in real_board_moves:
            default_coords.append(coord)
            board[coord[0]][coord[1]] =  temp_board[coord[0]][coord[1]]
    elif(level == "Hard"):
        real_board_moves = random.sample(list(moves_set), k = 20)
        for coord in real_board_moves:
            default_coords.append(coord)
            board[coord[0]][coord[1]] =  temp_board[coord[0]][coord[1]]
    return solved

def display_board(screen, font, board_matrix):
    temp = board_matrix.reshape(81)
    counter = 0
    for x in range(33,Window_height, 66):
        for y in range(33, Window_height, 66):
            rx = x//66
            ry = y//66
            val = temp[counter]
            text = None
            if val == 0:
                text = font.render("", True, (230,0,0)) 
            elif (rx, ry) in default_coords:
                text = font.render(str(val), True, (0,0,0)) 
            else:
                text = font.render(str(val), True, (230,0,0)) 
            text_rect = text.get_rect(center = (x,y))
            screen.blit(text, text_rect)
            counter+=1


# rows = 9
# cols = 9
# size = rows*cols
def game_over(current_board):
    for row in range(9): 
        if 0 in current_board[row]:
            return False
    if check(current_board):
        return True
    return False
def check(current_board):
    for row in range(9):
        dict1 = {}
        dict2 = {}
        for col in range(9):
            if(current_board[row][col] not in dict1 and current_board[row][col] != 0):
                dict1[current_board[row][col]] = None
            elif(current_board[row][col] != 0 and current_board[row][col] in dict1):
                return False
            if(current_board[col][row] not in dict2 and current_board[col][row] !=0):
                dict2[current_board[col][row]] = None
            elif(current_board[col][row] != 0 and current_board[col][row] in dict2):
                return False
    for row in range(0,9,3):
        for col in range(0,9,3):
            valid = check_cell(row, col, current_board)
            if not valid:
                return False
    return True
def check_cell(row, col, current_board):
    dict3 = {}
    for nrow in range(row, row +3):
        for ncol in range(col, col +3):
            if(current_board[nrow][ncol] not in dict3 and current_board[nrow][ncol] != 0):
                dict3[current_board[nrow][ncol]] = None
            elif(current_board[nrow][ncol] != 0 and current_board[nrow][ncol] in dict3):
                return False
    return True

def pick_cell(current_board):
    for i in range(9):
        for j in range(9):
            if current_board[i][j] == 0:
                return (i,j)
    return None
def solver(current_board):
    if game_over(current_board):
        return True
    coord1, coord2 = pick_cell(current_board)
    if(pick_cell(current_board) == None):
        return True
    row, col = coord1, coord2
    for number in range(1,10):
        current_board[row][col]=number
        if check(current_board):
            current_board[row][col] = number
            if solver(current_board):
                return True
            current_board[row][col]=0
        else:
            current_board[row][col]=0
    return False
    

main()
# mat = np.array([0]*size).reshape(rows,cols)
# mat[0][0], mat[1][0] = 1,2
# solver(mat)
# display_board(mat)
