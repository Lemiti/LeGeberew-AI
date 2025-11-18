# test_tensorflow.py
import tensorflow as tf
import numpy as np

print("🧪 Testing TensorFlow Installation...")
print(f"✅ TensorFlow Version: {tf.__version__}")
print(f"✅ GPU Available: {tf.config.list_physical_devices('GPU')}")
print(f"✅ CPU Devices: {tf.config.list_physical_devices('CPU')}")

# Test a simple operation
a = tf.constant([[1.0, 2.0], [3.0, 4.0]])
b = tf.constant([[1.0, 1.0], [0.0, 1.0]])
c = tf.matmul(a, b)

print(f"✅ Matrix multiplication test: {c.numpy()}")

print("🎉 TensorFlow is working correctly!")