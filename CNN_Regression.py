import tensorflow as tf
import numpy as np
import math

simulation_data_set = np.array([1, 3])
# simulation_data_set.append([1, 1, 1])

original_data_matrix = np.loadtxt("data_simulation.txt")
input_matrix = []
output_matrix = []


def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv_2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


sess = tf.InteractiveSession()
# paras
weight_conv1 = weight_variable([3, 3, 1, 32])
b_conv1 = bias_variable([32])

# covolutional layer-1
x = tf.placeholder(tf.float32, [None, 500])
x_reshape = tf.reshape(x, [-1, 28, 28, 1])

h_conv1 = tf.nn.relu(conv_2d(x_reshape, weight_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)
# #
xs = tf.placeholder(tf.float32, [None, 300])
ys = tf.placeholder(tf.float32, [None, 10])
#
# conv layer-2
W_conv2 = weight_variable([3, 3, 32, 64])

b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv_2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)

# full connection
weight_full_connection1 = weight_variable([7 * 7 * 64, 1024])
bias_full_connection1 = bias_variable([1024])

h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
h_full_connection1 = tf.nn.relu(tf.matmul(h_pool2_flat, weight_full_connection1) + bias_full_connection1)

# dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_full_connection1, keep_prob)

# output layer: softmax
weight_full_connection2 = weight_variable([1024, 10])
bias_full_connection2 = bias_variable([10])

y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, weight_full_connection2) + bias_full_connection2)
y_ = tf.placeholder(tf.float32, [None, 10])

# model training
cross_entropy = -tf.reduce_sum(y_ * tf.log(y_conv))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

correct_prediction = tf.equal(tf.arg_max(y_conv, 1), tf.arg_max(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

sess.run(tf.initialize_all_variables())


def next_batch(num):
    return np.asarray(input_matrix), np.asarray(output_matrix)


for i in range(20000):
    batch = next_batch(50)

    if i % 100 == 0:
        train_accuracy = accuracy.eval(feed_dict={x: batch[0], y_: batch[1], keep_prob: 1.0})
        print("step %d, training accuracy %g" % (i, train_accuracy))
    train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

# accuracy on test
