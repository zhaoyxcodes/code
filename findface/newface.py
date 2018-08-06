from scipy import misc
import tensorflow as tf
import numpy as np
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import argparse
import facenet
import sys

import copy
import align.detect_face
def main(args):
    modeldir = '/Users/zhaoyuanxu/Desktop/face/models/20170511-185253/20170511-185253.pb'
   

    minsize = 20 # minimum size of face
    threshold = [ 0.6, 0.7, 0.7 ]  # three steps's threshold
    factor = 0.709 # scale factor
    with tf.Graph().as_default():
        gpu_options = tf.GPUOptions(per_process_gpu_memory_fraction=1.0)
        sess = tf.Session(config=tf.ConfigProto(gpu_options=gpu_options, log_device_placement=False))
        with sess.as_default():
            pnet, rnet, onet = align.detect_face.create_mtcnn(sess, None)
    
    ytimg=args.image_files[0]
    imgs=[]
    filelists=[]
    valiatefile=args.image_files[1]
    for filename in os.listdir(valiatefile):
        filedir=valiatefile+'/'+filename
        imgsli=[ytimg,filedir]
        images = load_and_align_data(imgsli,160, 44,minsize, pnet, rnet, onet, threshold, factor)
        imgs.append(images)
        filelists.append(filedir)#保存图片路径
    with tf.Graph().as_default():
        with tf.Session() as sess:
            # Load the model
            facenet.load_model(modeldir)
            # Get input and output tensors
            images_placeholder = tf.get_default_graph().get_tensor_by_name("input:0")
            embeddings = tf.get_default_graph().get_tensor_by_name("embeddings:0")
            phase_train_placeholder = tf.get_default_graph().get_tensor_by_name("phase_train:0")
            urlstring=""
            for j in range(len(imgs)):
                imglist=imgs[j]
                yzimg=filelists[j]
                feed_dict = { images_placeholder: imglist, phase_train_placeholder:False }
                emb = sess.run(embeddings, feed_dict=feed_dict)
                dist = np.sqrt(np.sum(np.square(np.subtract(emb[0,:], emb[1,:]))))
                num='%1.4f  ' % dist
                print(num)
                if float(num)<0.9:
                    urlstring=urlstring+'{"url":"'+yzimg+'"},'
            if len(urlstring)>0:
                nums=len(urlstring)-1
                urlstring=urlstring[0:nums]
                print(urlstring)
                return '{"data":['+urlstring+']}'
            # valiatefile=args.image_files[1]
            # for filename in os.listdir(valiatefile):
            #     filedir=valiatefile+'/'+filename
            #     image2 = cv2.imread(filedir)
            #     image2 = cv2.resize(image2, (image_size,image_size))
            #     #cv2.imwrite("D:\\home\\facefiles\\VALIDATE\\1.jpg", image2)
            #     image2 = facenet.prewhiten(image2)
            #     img_list = [None]*2
            #     img_list[0]=image1
            #     img_list[1]=image2
            #     feed_dict = { images_placeholder: img_list, phase_train_placeholder:False }
            #     emb = sess.run(embeddings, feed_dict=feed_dict)
            #     dist = np.sqrt(np.sum(np.square(np.subtract(emb[0,:], emb[1,:]))))
            #     num='%1.4f  ' % dist
            #     print(num)
            #     if float(num)<1:
            #         return filedir;


    return "";

def load_and_align_data(image_paths,image_size, margin,minsize, pnet, rnet, onet, threshold, factor):

    
  
    tmp_image_paths=copy.copy(image_paths)
    img_list = []
    for image in tmp_image_paths:
        img = misc.imread(os.path.expanduser(image), mode='RGB')
        img_size = np.asarray(img.shape)[0:2]
        bounding_boxes, _ = align.detect_face.detect_face(img, minsize, pnet, rnet, onet, threshold, factor)
        if len(bounding_boxes) < 1:
          image_paths.remove(image)
          print("can't detect face, remove ", image)
          continue
        det = np.squeeze(bounding_boxes[0,0:4])
        bb = np.zeros(4, dtype=np.int32)
        bb[0] = np.maximum(det[0]-margin/2, 0)
        bb[1] = np.maximum(det[1]-margin/2, 0)
        bb[2] = np.minimum(det[2]+margin/2, img_size[1])
        bb[3] = np.minimum(det[3]+margin/2, img_size[0])
        cropped = img[bb[1]:bb[3],bb[0]:bb[2],:]
        aligned = misc.imresize(cropped, (image_size, image_size), interp='bilinear')
        prewhitened = facenet.prewhiten(aligned)
        img_list.append(prewhitened)
    images = np.stack(img_list)
    return images
def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('image_files', type=str, nargs='+', help='Images to compare')
    return parser.parse_args(argv)

if __name__ == '__main__':
    argv=['/Users/zhaoyuanxu/desktop/face/facefiles/VALIDATE/validate.jpg','/Users/zhaoyuanxu/desktop/face/facefiles/IMG']
    main(parse_arguments(argv))
    
   