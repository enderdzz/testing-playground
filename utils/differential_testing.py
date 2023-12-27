import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import onnx
import torch
import tensorflow as tf
import numpy as np
import onnxruntime as ort

class TestCase:
    def __init__(self, api_name, param) -> None:
        self.api_name = api_name
        self.param = param

def build_tf_model(arg_info, saved_tf_model_dir):

    func = arg_info[0]
    arg_info = arg_info[1:]
    
    signature = gen_signature(arg_info)
    print(f'[+] Generated signature: {signature}')

    cmd_model = func + '('
    for i in range(len(arg_info)):
        arg_name, data, dtype = arg_info[i]
        if 'tf.' in dtype:
            cmd_model += f'{arg_name}=args[{i}],'
        else:
            cmd_model += f'{arg_name}={str(data)},'
    cmd_model += ')'

    class CustomModule(tf.Module):
        def __init__(self):
            super(CustomModule, self).__init__()

        @tf.function(input_signature=signature)
        def __call__(self, *args):
            return func(**para)

    module = CustomModule()
    
    # https://stackoverflow.com/questions/60974077/how-to-save-keras-model-as-frozen-graph
    full_model = tf.function(lambda x: module(*x))
    full_model = full_model.get_concrete_function(signature)
    from tensorflow.python.framework.convert_to_constants import convert_variables_to_constants_v2
    frozen_func = convert_variables_to_constants_v2(full_model)
    frozen_func.graph.as_graph_def()
    tf.io.write_graph(graph_or_graph_def=frozen_func.graph,
                      logdir="./onnx_test/tf_model",
                      name=f"{func}_frozen_graph.pb",
                      as_text=False)
    tf.saved_model.save(module, saved_tf_model_dir)

def gen_model_pair(api="tf.dynamic_stitch", source="Tensorflow", target="ONNX"):
    # TODO: arg info parser, warp into a model.
    func = eval(api)
    para = {'indices': [[0xdeadbeef], [405], [519], [758], [1015]], 'data': [[110.27793884277344], [120.29475402832031], [157.2418212890625], [157.2626953125], [188.45382690429688]]}
    y = func(**para)
    return "", ""

if __name__ == "__main__":
    m1,m2 = gen_model_pair()