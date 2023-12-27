import tensorflow as tf
with tf.io.gfile.GFile('tf_ops.pbtxt', 'rb') as f:
    pbtxt = f.read()
    
graph_def = tf.compat.v1.GraphDef()
graph_def.ParseFromString(pbtxt)