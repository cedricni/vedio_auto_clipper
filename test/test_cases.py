import logging
import os
import glob
from PIL import Image
import unittest
# import natsort
import shutil
from torchvision.transforms import ToPILImage
from clustering.faceCluster import FaceCluster
from clustering.clipper import Clipper
from pre_post_processing.vidClips import frame_duration, extract_clip
from pre_post_processing.vidToImg import extract_frames, detect_faces


logging.basicConfig(level=logging.INFO)
class clipper_test(unittest.TestCase):
    """
    The clipper is involved with 4 phases:
    (1)Video Input (2) Cropping (3) Clustering (4) Clipping
    The test cases covers the whole process
    """
    def test_case_cluster(self):
        """
        Covers (3)
        :return:
        """
        # img_folder = './cropped'
        # if not os.path.exists(img_folder):
        #     raise FileNotFoundError('Image directory not found')
        # img_names = list(glob.glob(img_folder + '/'+'*.jpg'))
        # img_names = natsort.natsorted(img_names)
        #
        # with Image.open(img_names[0]) as img:
        #     print("Image count:", len(img_names), '\nImage size:', img.size)
        # print(img_names)
        cluster = FaceCluster()
        result = cluster.recognition("./cropped")
        print(result)

    def test_mtcnn_cropping(self):
        cluster = FaceCluster()
        img_names = list(glob.glob("./cropped" + '/'+'*.jpg'))
        save_folder = './tmp/mtcnn_crop'
        for img_path in img_names:
            res = cluster.single_frame_crop(img_path, save_path=save_folder + '/' + img_path.split('/')[2])
            if res is None:
                continue
            print(res.shape)

    def test_case_clipper_process(self):
        """
        Cover (3) (4)
        :return:
        """
        # img_folder = './cropped'
        # if not os.path.exists(img_folder):
        #     raise FileNotFoundError('Image directory not found')
        # img_names = list(glob.glob(img_folder + '/' + '*.jpg'))
        # img_names = natsort.natsorted(img_names)
        #
        # with Image.open(img_names[0]) as img:
        #     print("Image count:", len(img_names), '\nImage size:', img.size)

        cluster = FaceCluster()
        cluster_result = cluster.recognition("./cropped")
        logging.info(f"Finished clusering with {len(cluster_result['id'].unique())}")

        output_dir = './test_output'
        video_path = '../resource/video/input.mp4'
        time_info = frame_duration(cluster_result)
        extract_clip(video_path, time_info, output_dir)


    def test_case_clip_cluster_output(self):
        """
        Test (2) (3) (4)
        :return:
        """
        video_path = '../resource/video/input.mp4'
        input_file = video_path

        img_output_folder = "imgs"
        cropped_output_folder = "./test_temp"
        # extract frames from the video
        extract_frames(input_file, img_output_folder)

        # detect faces in frames and export cropped faces
        detect_faces(img_output_folder, cropped_output_folder)

        cluster = FaceCluster()
        cluster_result = cluster.recognition(cropped_output_folder)
        logging.info(f"Finished clusering with {len(cluster_result['id'].unique())}")

        output_dir = './test_output'
        time_info = frame_duration(cluster_result)
        extract_clip(video_path, time_info, output_dir)

        # Delete cropped
        # shutil.rmtree(cropped_output_folder)
        # shutil.rmtree(img_output_folder)

    def test_case_multiface(self):
        """
        Test cropping images with multiple faces.
        :return:
        """
        cluster = FaceCluster()
        img_path = '../resource/multi_face_photo.jpeg'
        save_folder = './tmp/mtcnn_crop'
        res = cluster.single_frame_crop(img_path, save_path=save_folder + '/' + 'multi.png')
        print(res.shape)

    def test_case_crop_dir(self):
        cluster = FaceCluster()
        img_dir = '../resource/frames'
        output_dir = './tmp/batch_crop'
        cluster.batch_crop(img_dir, output_dir)

    def test_main(self):
        cliper = Clipper()
        input_path = '../resource/video/input.mp4'
        output_dir = './test_output'
        cliper.clip(input_path, output_dir)



