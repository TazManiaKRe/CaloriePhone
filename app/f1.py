import tensorflow as tf

@tf.function
def macro_soft_f1(label_tensor, matrix_tensor):

    # cast to float32 as we are dealing with float values
    label_tensor = tf.cast(label_tensor, tf.float32)
    matrix_tensor = tf.cast(matrix_tensor, tf.float32)

    # calculate confusion matrix values
    # - TP: true positive
    # - FP: false positive
    # - FN: true negative
    TP = tf.reduce_sum(matrix_tensor * label_tensor, axis=0)
    FP = tf.reduce_sum(matrix_tensor * (1 - label_tensor), axis=0)
    FN = tf.reduce_sum((1 - matrix_tensor) * label_tensor, axis=0)

    # use F1 score formula to calculate F1 score
    f1 = (2*TP) / (2*TP + FN + FP + 1e-16)

    # deduce cost from calculated F1 score
    cost = 1 - f1

    # deduce average across all labels
    avg_cost = tf.reduce_mean(cost)
    
    return avg_cost

@tf.function
def macro_f1(label_tensor, matrix_tensor, thresh=0.1):

    # get prediction if greater than threshold
    label_tensor_filtered = tf.greater(matrix_tensor, thresh)

    # cast to float32 as we are dealing with float values
    label_tensor_prediction = tf.cast(label_tensor_filtered, tf.float32)
    matrix_tensor = tf.cast(matrix_tensor, tf.float32)

    # calculate confusion matrix values
    # - TP: true positive
    # - FP: false positive
    # - FN: true negative
    TP = tf.cast(tf.math.count_nonzero(label_tensor_prediction * label_tensor, axis=0), tf.float32)
    FP = tf.cast(tf.math.count_nonzero(label_tensor_prediction * (1 - label_tensor), axis=0), tf.float32)
    FN = tf.cast(tf.math.count_nonzero((1 - label_tensor_prediction) * label_tensor, axis=0), tf.float32)

    # use F1 score formula to calculate F1 score for current batch
    f1 = (2*TP) / (2*TP + FN + FP + 1e-16)

    # deduce average across all labels for current batch
    f1 = tf.reduce_mean(f1)

    return f1