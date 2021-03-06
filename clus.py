import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from random import randint

# the image we're dealing with

print("- reading the image")
img = mpimg.imread('./img/bunny copy.jpg')

# calculate euclidean distance

def distance(p1, p2):
    dist = 0
    for i in range(len(p1)):
        dist += (p1[i] - p2[i])**2
    return dist**0.5

def add_vecs(p1, p2):
    new_p = []
    for i in range(len(p1)):
        new_p.append(p1[i] + p2[i])
    return new_p

# pixel = array of five elements [x, y, r, g, b]

pixels = []

# populate pixel array

print("- getting all the pixel values")
for y in range(len(img)):
    for x in range(len(img[y])):
        color = img[y][x]
        pixels.append((x, y, *color))
        
height = len(img)
width = len(img[0])

# number of clusters, other settings

k = 10
max_iter = 15

# start with k random centroids

print("- generating random centroids")
centroids = [(randint(0, width-1), randint(0,height-1), 
    randint(0,255), randint(0,255), randint(0,255)) for _ in range(k)]

# pixels grouped by centroid

g_pix = [set() for _ in range(k)]

# find out which pixel a centroid should belong to

def which_centroid(p):
    dist = float('inf')
    result = -1
    for c in range(k):
        this_dist = distance(centroids[c], p) 
        if this_dist < dist:
            dist = this_dist
            result = c
    return result

# assign each pixel to a centroid
print("- assigning each pixel to a centroid")
for p in range(len(pixels)):
    if p % 100000 == 0:
        print(p)
    c = which_centroid(pixels[p])
    g_pix[c].add(pixels[p])

# calculate new centroid positions
def adjust_centroids():
    print("- moving centroids around")
    for i in range(k):
        centroid_pix = g_pix[i]
        avg = [0] * 5
        for pix in centroid_pix:
           avg = add_vecs(avg, pix)
        for i in range(len(avg)):
            if len(centroid_pix) != 0:
                avg[i] /= len(centroid_pix)
        centroids[i] = tuple(avg)
        
def which_centroid_current(pix):
    for i in range(k):
        if pix in g_pix[i]:
            return i
    return None

# move pixels to their new centroid
# NOTE TODO this function takes the longest
def move_pix():
    print("- moving pixels around")
    was_change = False
    # for every pixel
    for pix in pixels:
        new_cent = which_centroid(pix)
        if pix not in g_pix[new_cent]:
            was_change = True
            current_cent = which_centroid_current(pix)
            g_pix[current_cent].remove(pix)
            g_pix[new_cent].add(pix)
    return was_change

# make a value copy of the g_pix array of sets. Used to test if 
# the centroid groups have changed
'''
def copy_pixel_groups():
    return [group for group in g_pix]
'''

# repeat until there's convergence or we need to be done
# do this with two lists which swap or maybe keep it all in g_pix? 
# think about the best way
# returns true if there was a change, false otherwise
def iterate():
    adjust_centroids()
    was_change = move_pix()
    return was_change

def cluster():
    iters = 0
    was_change = True
    while iters < max_iter and was_change:
        was_change = iterate()
        iters += 1
        print("iteration ", iters)

cluster()

# load the image again
new_img = mpimg.imread('./img/bunny copy.jpg')
new_img.setflags(write=1)
# draw the result over the current new image
color = 0
for pix_group in g_pix:
    color_shade = color / (k - 1) * 255
    color += 1
    for pix in pix_group:
        new_img[pix[1]][pix[0]][0] = color_shade
        new_img[pix[1]][pix[0]][1] = color_shade
        new_img[pix[1]][pix[0]][2] = color_shade

fig = plt.figure()
a=fig.add_subplot(1,2,1)
imgplot_orig = plt.imshow(new_img)
a.set_title('Before')
a=fig.add_subplot(1,2,2)
imgplot_new = plt.imshow(img)
a.set_title('After')

plt.show()

