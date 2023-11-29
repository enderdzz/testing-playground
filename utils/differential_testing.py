import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import onnx
import torch
import tensorflow as tf
import numpy as np
import onnxruntime as ort
#from onnx2torch import convert


def gen_model(api, framework):
    func = tf.raw_ops.DynamicStitch
    func = tf.dynamic_stitch
    # TODO: arg info parser, warp into a model.
    
    return str(func)

if __name__ == "__main__":
    print(gen_model("", ""))