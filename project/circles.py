from images import *
from os import listdir
from sys import argv

def main(directory, name, images, dp, minDist, param1, param2, minRadius, maxRadius, color):
    paths = listdir(directory)
    paths = [f'{directory}/{path}' for path in paths if path.startswith(name)]
    
    images = [cv.imread(path) for path in paths[0:images]]
    first = images[1]
    for image in images:
        result, mask = filterImage(image, color, 2)
        addCircles(first, mask, dp, minDist, param1, param2, minRadius, maxRadius)
    # cv.imshow("First", first)
    # cv.waitKey(0)
    path = f'testing/{name}_{dp}_{color}_{minRadius}_{maxRadius}_{param1}.jpg'
    cv.imwrite(path, first)

if __name__ == "__main__":
    directory, name, images = argv[1:]
    # for dp in range(1.5, 3, 0.5):
    count = 0
    for dp in [3, 3.5, 4, 4.5, 5, 5.5]:
        # for color in ["RED", "GREEN", "YELLOW"]:
        for minDist in [150]:
            for color in ["RED"]: 
                for minRadius in [50]:
                    for maxRadius in [150]:
                        for param1 in [100]:
                            for param2 in [100]:
                                print(count)
                                count += 1
                                main(directory, name, int(images), dp, minDist, param1, param2, minRadius, maxRadius, color) 
