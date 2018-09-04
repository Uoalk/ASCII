from PIL import Image
import math



def toBlackAndWhite(pixels):
    jump=1
    row=0
    while(row<len(pixels)-jump):
        col=0
        while(col<len(pixels[row])-jump):
            avg=0;
            for y in range(jump):
                for x in range(jump):
                    pixel=pixels[row+y][col+x]
                    avg+=int((0.2126*pixel[0] + 0.7152*pixel[1] + 0.0722*pixel[2]))
            avg/=(jump*jump);
            avg=int(avg)
            pixels[int(row/jump)][int(col/jump)]=(avg,avg,avg)
            col+=jump
        row+=jump
    return pixels;

def pixelate(pixels,pixelSize):
    jump=pixelSize
    row=0
    while(row<len(pixels)-jump):
        col=0
        while(col<len(pixels[row])-jump):
            avg=[0,0,0]
            for y in range(jump):
                for x in range(jump):
                    pixel=pixels[row+y][col+x]
                    avg[0]+=pixel[0]
                    avg[1]+=pixel[1]
                    avg[2]+=pixel[2]
            avg[0]=int(avg[0]/jump/jump)
            avg[1]=int(avg[1]/jump/jump)
            avg[2]=int(avg[2]/jump/jump)
            for y in range(jump):
                for x in range(jump):
                    pixels[row+y][col+x]=(avg[0],avg[1],avg[2])
            col+=jump
        row+=jump
    return pixels;

def colorDifference(c1,c2):
    return math.sqrt((c1[0]-c2[0])**2 + (c1[1]-c2[1])**2+ (c1[2]-c2[2])**2)
def onlyEdges(pixels,threshold):
    row=0
    while(row<len(pixels)-1):
        col=0
        while(col<len(pixels[row])-1):
            if(colorDifference(pixels[row][col],pixels[row][col+1])>threshold or colorDifference(pixels[row+1][col],pixels[row][col+1])>threshold):
                    pixels[row][col]=(0,0,0)
            else:
                pixels[row][col]=(255,255,255)
            col+=1
        row+=1
    return pixels;
def renderImage(data,name):
    pixels=data
    im= Image.new('RGB', (len(data[0]), len(data)))
    allData=[];
    for row in range(len(pixels)):
        for col in range(len(pixels[0])):
            allData.append(pixels[row][col])
    im.putdata(allData)
    im.save(name+'.png')
def reduceSize(pixels,factor):
    jump=factor
    row=0
    newPixels=[];
    while(row<len(pixels)-jump-1):
        col=0
        newPixels.append([]);
        while(col<len(pixels[row])-jump-1):
            avg=[0,0,0]
            for y in range(jump):
                for x in range(jump):
                    pixel=pixels[row+y][col+x]
                    avg[0]+=pixel[0]
                    avg[1]+=pixel[1]
                    avg[2]+=pixel[2]
            avg[0]=int(avg[0]/jump/jump)
            avg[1]=int(avg[1]/jump/jump)
            avg[2]=int(avg[2]/jump/jump)


            newPixels[int(row/factor)].append((avg[0],avg[1],avg[2]))
            col+=jump
        row+=jump
    return newPixels
def toASCII(pixels):
    string="";
    row=1
    while(row<len(pixels)-1):
        col=1
        while(col<len(pixels[row])-1):
            if pixels[row-1][col]==(0,0,0):
                above=pixels[row-1][col]==(0,0,0)
                below=pixels[row+1][col]==(0,0,0)
                left=pixels[row][col-1]==(0,0,0)
                right=pixels[row][col+1]==(0,0,0)
                topLeft=pixels[row-1][col-1]==(0,0,0)
                topRight=pixels[row-1][col+1]==(0,0,0)
                bottomLeft=pixels[row+1][col-1]==(0,0,0)
                bottomRight=pixels[row+1][col+1]==(0,0,0)

                total=above+below+left+right;
                if(above and below and left and right):
                    string+="+"
                elif above and below and not left and not right:
                    string += "|"
                elif not above and not below and left and right:
                    string+="-"
                elif topLeft and topRight and bottomLeft and bottomRight:
                    string+="X"
                elif topLeft and bottomRight:
                    string+="\\"
                elif topRight and bottomLeft:
                    string+="/"
                elif total>=3:
                    string+="*";
                    pass;
                else:
                    string +=" "

                """if(above and below and left and right):
                    string+="+"
                elif above and below and not left and not right:
                    string += "|"
                elif not above and not below and left and right:
                    string+="-"
                elif above and below and right and not left:
                    string +="Ͱ"
                elif above and below and left and not right:
                    string+="˧"
                elif not above and below and right and left:
                    string+="T"
                elif above and left and right and not below:
                    string+="┴ "
                else:
                    string +="*"
                """

            else:
                string +=" "
            col+=1
        string+="\n"
        row+=1
    return string;
#pixels=toBlackAndWhite(pixels)

#american gothic redoce=5, threshold=40
#wave: recode=1, threshold=50
#monalisa: reduce=10, thershold=19
#einstein: recude=3, threshold=30
#pinkfloyd: reduce=4, threshold=50


#i = Image.open("american-gothic.jpg")
#i=Image.open("wave.jpg")
#i=Image.open("mona-lisa.jpg")
#i=Image.open("einstein.png")
#i=Image.open("pinkfloyd.jpg")




def render(image,reduce,threshold):
    i=Image.open(image)
    pixelData = i.load() # this is not a list, nor is it list()'able
    width, height = i.size

    pixels = []
    for y in range(height):
        pixels.append([])
        for x in range(width):
            cpixel = pixelData[x, y]
            pixels[y].append((cpixel[0],cpixel[1],cpixel[2]))
    pixels=reduceSize(pixels,reduce)
    pixels=onlyEdges(pixels,threshold)
    print(toASCII(pixels))
    renderImage(pixels,"outlines/outline-"+image.split("/")[1])

render("images/american-gothic.jpg",5,40)

render("images/mona-lisa.jpg",10,19)
render("images/pinkfloyd.jpg",4,50)
render("images/einstein.png",3,30)


render("images/wave.png",2,45)
