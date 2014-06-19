##############################################
# Skeleton code for COMP10001 Proj 2 S1/2014
#
# Provided by Andrew Turpin and Tim Baldwin
#
# Date: 17/4/2014
#
# Your submission should be based on this skeleton
#
##############################################

import Image

TEST_REPORT = "testReport.html"
CAFE_FILE = "cafe.png"
THREE_IN_ONE_FILE = "3in1.png"


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)


def draw_square(image, (x, y), r, colour):
    assert not image == None
    width, height = image.size
    pixels = image.load()
    ex,ey = x+r,y+r
    if ex > width:
        ex = width
    if ey > height:
        ey = height
    yy = 0
    for yy in range(r):
        draw_line(image, (x,y+yy), (1,0), (ex,ey), colour)


def draw_line(image, (sx,sy), (dx,dy), (ex,ey), colour):
    assert not image == None
    width,height = image.size
    pixels = image.load()
    if (sx<0 and ex<0) or (sy<0 and ey<0) or (sx>width and ex>width) or (sy>height and ey>height):
        exit()
    if (sx<ex and dx<0) or (ex<sx and dx>0) or (sy<ey and dy<0) or (ey<sy and dy>0):
        exit()
    if dx>=0 and sx<0:
        sx = 0
    if dx>=0 and ex>width:
        ex = width
    if dx<=0 and ex<0 and ex!=None:
        ex = 0
    if dx<=0 and sx > width:
        sx = width
    if dy>=0 and sy<0:
        sy = 0
    if dy>=0 and ey>height:
        ey = height
    if dx<=0 and ey<0 and ey!=None:
        ey = 0
    if dy<=0 and sy>height:
        sy = height
    if sx == ex and ey == None:
        pixels[sx,sy]=colour
    if sx == ex and ey != None:
        k = 0
        while sy+k*dy<ey:
            pixels[sx,sy+k*dy] = colour
            k += 1
    if sy == ey and ex == None:
        pixels[sx,sy]=colour
    elif sy == ey and ex != None:
        k = 0
        while sx+k*dx<ex:
            try:
                pixels[sx+k*dx,sy] = colour
                k += 1
            except:
                break
    else:
        x,y,k=sx,sy,0
        while x!=ex and y!=ey:
            pixels[x,y] = colour
            x = sx + k*dx
            y = sy + k*dy
            k += 1
        if ex == 0 or ey == 0:
            pixels[x,y]=colour


######################################################
def set_colour(image, colour):
    """
    Set all pixels in `image` to `colour`
    
    INPUTS:
      image - an Image object
      colour - [R,G,B] list for background
    
    RETURNS: Nothing
    IN-PLACE MODIFICATION: sets all pixels in `image` to `colour`
    """
    width, height = image.size
    pixels = image.load()
    for x in range(0,width):
        for y in range(0,height):
            pixels[x,y] = colour


def draw_square_sequential(image, (x, y), radius, bg_colour, fg_colour):
    assert not image == None
    width,height = image.size
    pixels = image.load()
    control = False
    while x <= width:
        if control == False:
            draw_square(image, (x, y), radius, bg_colour)
            control = True
        else:
            draw_square(image, (x, y), radius, fg_colour)
            control = False
        x += radius
    return image


def draw_offset_line_sequential(image,(x, y), radius, offset, bg_colour, fg_colour):
    assert not image == None
    width,height = image.size
    pixels = image.load()
    yy = 0
    for yy in range(radius):
        draw_line(image, (0,y+yy), (1,0), (radius*offset,None), fg_colour)
    draw_square_sequential(image, (x+radius*offset, y), radius, bg_colour, fg_colour)
    return image


def draw_cafe(width, height, radius, offset, bg_colour, fg_colour):
    image = Image.new('RGB', (width, height))
    assert not image == None
    set_colour(image, bg_colour)
    # ADD YOUR CODE HERE
    pixels = image.load()
    x,y = 0,0
    offset_line = False
    while y <= height:
        if offset_line == False:
            draw_square_sequential(image, (x, y), radius, bg_colour, fg_colour)
            offset_line = True
        else:
            draw_offset_line_sequential(image,(x, y), radius, offset, bg_colour, fg_colour)
            offset_line = False
        y += radius
    image.show()
    return(image)
    

def draw_three_in_one(radius, fg_colour, bg_colour):
    """
    Draw 3 nested squares of side length 3*radius, 
    4*radius and 5*radius in `fg_colour` on a background
    of 9 tiled frames in `bg_colour`, where each frame is 
    4 nested squares that are diagonaly shaded alternately.
    
    INPUTS:
      radius - width of an individual frame part == 
               1/3 sidelength of inner square
      fg_colour - colour of 3 inner squares
      bg_colour - colour of background frames
    RETURNS: 
      Image of size 24*radius x 24*radius with RGB values
    """

    image = Image.new('RGB', (3*radius*8, 3*radius*8))
    assert not image == None
    set_colour(image, WHITE)

    # ADD CODE HERE FOR THE-BONUS-QUESTION
    # This function is not required - it is a bonus.
    # Finish the other functions first.

    return(image)


def images_equal(im1, im2):
    """
    Compare the pixel values of two images, returning
    True if they are the same, False otherwise
    INPUTS:
       im1, im2 - both Image objects
    RETURNS:
       True if pixel values of `im1` and `im2` are the same
       False otherwise
    """
    if not im1.size == im2.size:
        return False
    width,height = im1.size
    p1 = im1.load()
    p2 = im2.load()
    for x in range(0,width):
        for y in range(0,height):
            if not p1[x,y] == p2[x,y]:
                return False
    return True
    
def test_all(output_file, testlist):
    """
    Run all tests provided in `testlist` and print a HTML section 
    for each (which is an h2 heading and a table showing the 
    desired and obtained images).
    INPUTS:
      output_file - an open file object (NOT a filename)
      testlist - a list of dictionaries, where each dictionary contains
                'name'  - printed as heading and used 
                          without spaces as the image filenames
             'function' - name of function to call as string
                          This function should not return anything.
               'params' - List of parameters (in the correct order)
                          as strings for passing to the funciton.
                          The parameter "canvas" is available as an
                          empty image that is the same size as...
               'result' - An Image object that is the expected result
                          of calling funciton(params)
    RETURNS: Nothing.
    IN-PLACE MODIFICATION: 
      Outputs HTML to `output_file` that includes for each element of 
      `testlist`, `tc`:
         A h2 heading that is tc['name'] and Passed or Failed
         The desired image (tc['result'])
         The obtained image (canvas after tc['function'](tc['params']) is run)
    """
    assert not output_file == None
    for tc in testlist:
        result_image = tc['result']
        canvas = Image.new('RGB', result_image.size)
        cmd = "{0}({1})".format(tc['function'], ','.join([str(p) for p in tc['params']]))
        print (cmd)
        answer = eval(cmd)
        if answer == None:
            answer = canvas
        wanted_filename = "{0}-wanted.png".format(tc['name']).replace(" ", "")
        got_filename    = "{0}-got.png".format(tc['name']).replace(" ", "")
        answer.save(got_filename)
        result_image.save(wanted_filename)
        pass_fail = "Passed" if images_equal(answer, result_image) else "Failed"
        output_file.write("<h2>{0} - {1}</h2>".format(tc['name'], pass_fail))
        output_file.write("<table><tr>\n")
        output_file.write("<td><img src={0} width=200></td>\n".format(wanted_filename))
        output_file.write("<td><img src={0} width=200></td></tr>\n".format(got_filename))
        output_file.write("<tr><td>Wanted</td><td>Got</td></tr>\n")
        output_file.write("</table>\n")


#######################################################
# Test cases
#######################################################

res1 = Image.new('RGB', (5, 5))
res1.putdata([
        RED  ,BLACK,BLACK,BLACK,BLACK, 
        BLACK,RED  ,BLACK,BLACK,BLACK, 
        BLACK,BLACK,  RED,BLACK,BLACK, 
        BLACK,BLACK,BLACK, RED ,BLACK, 
        BLACK,BLACK,BLACK,BLACK,  RED 
    ])

res2 = Image.new('RGB', (5, 3))
res2.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK, 
        BLACK,BLACK, RED ,BLACK,BLACK, 
        BLACK,BLACK,BLACK,BLACK,BLACK 
    ])

res3 = Image.new('RGB', (5, 5))
res3.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK, 
        BLACK, RED , RED , RED ,BLACK, 
        BLACK, RED , RED , RED ,BLACK, 
        BLACK, RED , RED , RED ,BLACK, 
        BLACK,BLACK,BLACK,BLACK,BLACK 
    ])

res4 = Image.new('RGB', (5, 5))
res4.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,
        WHITE,WHITE,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK
    ])

res5 = Image.new('RGB', (5, 5))
res5.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,WHITE,BLACK,BLACK,
        BLACK,BLACK,WHITE,BLACK,BLACK,
        BLACK,BLACK,WHITE,BLACK,BLACK
    ])

res6 = Image.new('RGB', (8, 8))
res6.putdata([
         RED ,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK, RED ,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK, RED ,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK, RED ,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK, RED ,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK
    ])

res7 = Image.new('RGB', (8, 8))
res7.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
         RED , RED , RED , RED , RED , RED ,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK
    ])

res8 = Image.new('RGB', (8, 8))
res8.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK, RED ,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK, RED ,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK, RED ,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK, RED ,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK
    ])

res9 = Image.new('RGB', (8, 8))
res9.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
         RED ,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK, RED ,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK, RED ,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK, RED ,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK, RED ,BLACK,BLACK,BLACK
    ])

res10 = Image.new('RGB', (8,8))
res10.putdata([
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK, RED , RED , RED , RED ,BLACK,BLACK,BLACK,
        BLACK, RED , RED , RED , RED ,BLACK,BLACK,BLACK,
        BLACK, RED , RED , RED , RED ,BLACK,BLACK,BLACK,
        BLACK, RED , RED , RED , RED ,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,
        BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK,BLACK
    ])


# Note: canvas is defined in the test harness to be the same 
# size as result with a BLACK background
test_cases = [
    {'name':'Test 1', 
     'function':'draw_line', 
     'params':['canvas', '(-2,-2)', '(+1,+1)', '(20,20)', 'RED'], 
     'result': res1
    },

    {'name':'Test 2', 
     'function':'draw_line', 
     'params':['canvas','(2,1)', '(0,0)', '(None,1)', 'RED'], 
     'result': res2
    },

    {'name':'Test 3', 
     'function':'draw_square', 
     'params':['canvas','(1,1)', '3', 'RED'], 
     'result': res3
    },

    {'name':'Test 4',
     'function':'draw_line',
     'params':['canvas', '(0,2)', '(+1,0)', '(2,2)', 'WHITE'],
     'result': res4
    },

    {'name':'Test 5',
     'function':'draw_line',
     'params':['canvas', '(2,4)', '(0,-1)', '(None,1)', 'WHITE'],
     'result': res5
    },

    {'name':'Test 6',
     'function':'draw_line',
     'params':['canvas', '(0,0)', '(1,1)', '(5,5)', 'RED'],
     'result': res6
    },

    {'name':'Test 7',
     'function':'draw_line',
     'params':['canvas', '(5,3)', '(-1,0)', '(0,None)', 'RED'],
     'result': res7
    },

    {'name':'Test 8',
     'function':'draw_line',
     'params':['canvas', '(5,3)', '(0,-1)', '(None,0)', 'RED'],
     'result': res8
    },

    {'name':'Test 9',
     'function':'draw_line',
     'params':['canvas', '(4,7)', '(-1,-1)', '(0,3)', 'RED'],
     'result': res9
    }, 

    {'name':'Test 10',
     'function':'draw_square',
     'params':['canvas','(1,1)', '4', 'RED'],
     'result': res10
    },

    {'name':'Test 11',
     'function':'draw_square',
     'params':['canvas','(5,5)', '3', 'WHITE'],
     'result': res11
    },

    {'name':'Test 12',
     'function':'draw_cafe',
     'params':['canvas','(5,5)', '3', 'WHITE'],
     draw_cafe(width, height, radius, offset, bg_colour, fg_colour)
     'result': res12
    }

]



def main():
    """
    Main function to generate www page
    """
    radius   = 50
    image = draw_cafe(int(10.5*radius), 10*radius, radius, 0.66, WHITE, BLACK)
    image.save(CAFE_FILE)
    print 'pass image.save(CAFE_FILE)'
    '''
    radius = 20
    image = draw_three_in_one(radius, RED, BLACK)
    image.save(THREE_IN_ONE_FILE)
    '''
    f = open(TEST_REPORT, 'w')
    assert not f == None

    # ADD CODE HERE: f.write some HTML
    f.write('<!DOCTYPE html>\n<html>\n'+' '*4
            +'<head><title><COMP10001 Project 2></title></head>\n'+' '*4
            +'<body>\n'+' '*4+'<h1>Project 1 Images</h1>\n'
            +'<img src='+CAFE_FILE+' alt="Cafe Wall Illusion(left)" height="400" width="400">\n'
            +' '*4+'<h1>Test Results</h1>\n'+' '*4)
    test_all(f,test_cases)
    f.write(' '*4+'</body>\n</html>')
    f.close()
    print 'pass test_all(f, test_cases)'

main()
