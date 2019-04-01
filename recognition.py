''' Finding Actors Screen Time and time of their first and last presence '''

# Import necessary stuff
import argparse
from imutils import paths
import face_recognition
import cv2

# Passing arguments
ap = argparse.ArgumentParser()

# traindata takes the original images of actors to encode
ap.add_argument("-i", "--traindata", required=True,
	help="path to images for training")

# checkdata takes all images of frames that were generated from the video
ap.add_argument("-j", "--checkdata", required=True,
	help="path to input directory of faces + images")
args = vars(ap.parse_args())

# imagePaths and video_imagePaths are lists of paths to train images and images of videoframes respectively
imagePaths = list(paths.list_images(args["traindata"]))
video_imagePaths = list(paths.list_images(args["checkdata"]))

# In Encodings list, we have face encoding of every actor
Encodings=[]
for image in imagePaths:
    image1 = face_recognition.load_image_file(image)
    Encodings.append(face_recognition.face_encodings(image1)[0])

# We created a list of actors we are concerned about
Names_List = ["ScarlettJohansson","JeremyRenner","RobertDowney","MarkRuffalo","ChrisEvnas"]

# Function to return the frame number, so we could sort the images based on their occurrence in video
def cond(x):
    return(x[10:12])
 
#Final_List is a list of names of the actors where index represents the second and value at that index represents the actor present in that particular second
Final_List = []
for image in sorted(video_imagePaths,key=cond):
    # Loading and creating encodings to faces in a frame 
    picture = face_recognition.load_image_file(image)
    image_encoded = face_recognition.face_encodings(picture)
    
    # If there is a face, an actor is present in that frame else No one is there 
    if(len(image_encoded)>0):
        for i in image_encoded:
                result = face_recognition.compare_faces(Encodings,i)
                if True in result:
                  # Find the index of true
                  match_index = result.index(True)
                  # Find the actor name at the index where true is found
                  Final_List.append(Names_List[match_index])
                
    else:
        Final_List.append("None")

# Writing into a file
f= open("output.txt","w+")
for Actor in Names_List:
    a = str(Final_List.count(Actor))
    # First appearance of actor
    for i in Final_List:
        if(i==Actor):
          start = str(Final_List.index(i))
          break
    
    # Last appearance of actor
    for i in Final_List[::-1]:
        if(i==Actor):
          end = str(len(Final_List)-Final_List[::-1].index(i))
          break

    # First appearance, last appearance and screentime
    f.write(Actor+" first appeared at "+start+" seconds\n")
    f.write(Actor+" last appeared at "+end+" seconds\n")
    f.write("The screen time of "+Actor+" is "+a+" seconds\n")
print("Done Buddy!")
f.close()



