import onnxruntime as ort
import numpy as np

# ONNX模型路径
model_path = '/home/jjp/issac/masterV5-LocomotionWithNP3O/LocomotionWithNP3O/body_latest.onnx'

# 创建ONNX运行时会话
session = ort.InferenceSession(model_path)

# 准备全零输入数据 'obs_hist'
obs_hist_zero = np.zeros((1, 10, 45), dtype=np.float16)

# 构建输入字典
inputs = {'obs_hist': obs_hist_zero}

# 运行模型
outputs = session.run(None, inputs)

# 获取并打印输出结果
output = outputs[0]
print("Model output with zero input:", output)