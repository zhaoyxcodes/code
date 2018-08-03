import web  
import newface
import argparse
import random
import io

# from web.wsgiserver import CherryPyWSGIServer
urls = (  
    '/myHome/face/info/facefile', 'setface',
    '/myHome/face/info/validatefacefile','validateface',
    '/myHome/face/info/getImage','getImage'
)
 
# CherryPyWSGIServer.ssl_certificate = "/Users/zhaoyuanxu/desktop/myserver.crt"
# CherryPyWSGIServer.ssl_private_key = "/Users/zhaoyuanxu/desktop/myserver.key"

img_dirpath="/Users/zhaoyuanxu/desktop/face/facefiles/IMG"
face_dirpath="/Users/zhaoyuanxu/desktop/face/facefiles/FACE"
validate_dirpath="/Users/zhaoyuanxu/desktop/face/facefiles/VALIDATE"
app = web.application(urls, globals())

class getImage:
    def GET(self):
        form = web.input(url="")
        if(form.url!=""):
            print(form.url)
            fo = open(form.url, "rb+")
            img=fo.read()
            fo.close()
            return img;
        return "";
class validateface:
    def POST(self):
        form = web.input(file="")
        if(form.file!=""):
            validateimg=validate_dirpath+"/validate.jpg"
            fo = open(validateimg, "wb+")
            fo.write(form.file)
            fo.close()
            #argv=[validateimg,validate_dirpath+"/validate_face.jpg"]
            #vface= set_other_people.main(argv)
            #if(vface=="true"):
            argv2=[validate_dirpath+"/validate.jpg",img_dirpath]
            parser2 = argparse.ArgumentParser()
            parser2.add_argument('image_files', type=str, nargs='+', help='Images to compare')
            return newface.main( parser2.parse_args(argv2))
        return "error"
class setface:
    def POST(self):
        form = web.input(file="")
        if(form.file!=""):
            randomnum=str(random.randint(0,1000))
            ytimg=img_dirpath+"/"+randomnum+".jpg"
            fo = open(ytimg, "wb+")
            fo.write(form.file)
            fo.close()
            #argv=[ytimg,face_dirpath+"/"+randomnum+"_face.jpg"]
            #set_other_people.main( argv)
            return "true"
        return "error"

if __name__ == "__main__":
    app.run() 