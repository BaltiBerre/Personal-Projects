import turtle

def draw_tree(t, branch_length, depth):
    if depth == 0:
        return

    # Draw the current branch
    t.forward(branch_length)

    if depth == 3:
        # Draw left child with two children
        t.left(45)
        draw_tree(t, branch_length / 2, depth - 1)
        t.right(59)

        # Draw right child with one child that has one child
        t.right(45)
        draw_tree(t, branch_length / 2, depth - 1)
        t.left(45)
    elif depth == 2:
        # Draw left child
        t.left(45)
        draw_tree(t, branch_length, depth - 1)
        t.right(45)

        # Draw right child
        t.right(45)
        draw_tree(t, branch_length / 2, depth - 1)
        t.left(50)

        t.right(45)
        draw_tree(t, branch_length, depth-2)
        t.left(60)

        t.right(45)
        draw_tree(t, branch_length, depth-1)
        t.left(60)
    elif depth == 1:
        # End nodes without children
        pass

    # Return to the starting point of the current branch
    t.backward(branch_length)

def setup_turtle():
    # Initialize turtle
    t = turtle.Turtle()
    t.speed('fastest')
    t.penup()
    t.goto(-200, 0)  # Start drawing from the left side of the screen
    t.pendown()
    t.left(90)  # Point the turtle upwards

    return t

def draw_forest():
    # Set up the screen
    screen = turtle.Screen()
    screen.bgcolor("white") 

    # Draw the first specific tree
    t1 = setup_turtle()
    draw_tree(t1, 100, 3)
    t1.hideturtle()

    # Move to a new location and draw a second, unconnected tree
    t2 = setup_turtle()
    t2.penup()
    t2.goto(200, 0)  # Position for the second tree
    t2.pendown()
    draw_tree(t2, 100, 3)
    t2.hideturtle()

    # Keep the window open until it is clicked
    screen.exitonclick()

draw_forest()
