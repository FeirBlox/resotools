'''
Author: Achetair
Date: 2024-03-17 21:19:08
LastEditors: Achetair
Description: 
'''
import os
import numpy as np
from cnocr import CnOcr
from resotools.utils.CommonUtils import *
from resotools.utils.UserLog import obj_log as log

MODEL_ROOT = "D:/work/resotools"

class Ocr_tools():
    def __init__(self,det_model_name="ch_PP-OCRv3_det", rec_model_name= "densenet_lite_114-fc", det_root="model/cnstd", rec_root="model/cnocr", number=False, start=True) -> None:
        det_root, rec_root = os.path.join(MODEL_ROOT, det_root), os.path.join(MODEL_ROOT, rec_root)
        
        print("det_root: {}, rec_root:{}".format(det_root, rec_root))
        rec_vocab_path = os.path.join(MODEL_ROOT, "model/cnocr/label_cn.txt")
        self.ocr = CnOcr(det_model_name=det_model_name, rec_model_name=rec_model_name, rec_vocab_fp=rec_vocab_path, det_root=det_root, rec_root=rec_root) 
        self.number_ocr = CnOcr(det_model_name=det_model_name, rec_model_name="en_number_mobile_v2.0", det_root=det_root, rec_root=rec_root, cand_alphabet='0123456789.+%')
    
    
    '''
    description: 识别图片中的文字
    img_path：识别的图片
    charac：匹配的文字
    '''
    def ocr_characters(self, img_path, charac):
        ocr_list = self.ocr_img(img_path)
        for vd in ocr_list:
            msg = vd["text"]
            if charac in msg:
                pos = vd["position"]
                log.debug("发现文字 : {}, 轮廓为：{}".format(charac, self.__extract_shape(pos)))
                return (msg, self.ocr_center_pos(pos))
                # return (msg, self.__extract_shape(vd["position"]))
        return None
        
    def __extract_shape(self, npa):
        npl = npa.tolist()
        assert len(npl) == 4
        left = npl[0][0]
        top = npl[0][1]
        right = npl[2][0]
        bottom = npl[2][1]
        
        return [left, top, right, bottom]
    
    def ocr_number(self, img_path):
        result = self.number_ocr.ocr_for_single_line(img_path)
        text = result["text"]
        if text == "":
            return None
        try:
            num = int(text)
            return num
        except ValueError:
            return None
        
    def ocr_mutitext(self, img_path, kwords:list):
        ocr_list = self.ocr_img(img_path)
        ret = {}
        for word in kwords:
            for vd in ocr_list:
                msg = vd["text"]
                if word in msg:
                    pos = vd["position"]
                    log.debug("发现文字 : {}, 轮廓为：{}".format(msg, self.__extract_shape(pos)))
                    ret[word] = {
                        "text":msg,
                        "pos":self.ocr_center_pos(pos)
                    }
                    break
        return ret
                              
                
        
        
    def ocr_img(self, img_path):
        return self.ocr.ocr(img_path)
    
    def ocr_center_pos(self, ocr_array):
        position = np.mean(ocr_array, axis=0)
        return position.tolist()
    
    
    
if __name__ == "__main__":
    ooo = Ocr_tools()
    # pp = r"D:\work\resotools\tmp\test-ResoadbObj\daodamudidi_cropped.png"
    # pp = r"D:\work\resotools\tmp\test-ResoadbObj\liechexingshi.png"
    # rr = ooo.number_ocr.ocr_for_single_line(pp)
    # print(rr)