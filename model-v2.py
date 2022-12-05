"""
Describe: Model's architecture (v2).
Authors: Eduardo Destefani Stefanato & Vitor Souza Premoli Pinto de Oliveira.
Contact: edustefanato@gmail.com
Date: 17/11/2022.
MIT License | Copyright (c) 2022 Eduardo Destefani Stefanato
"""
# importing neural network keras with tensorflow
from keras.layers import Dropout, Conv2D, MaxPooling2D
from keras.layers import AveragePooling2D, concatenate, Conv2DTranspose
from keras import Model, Input, backend

def dice_coef(y_true, y_pred):
    y_true_f = backend.flatten(y_true)
    y_pred_f = backend.flatten(y_pred)
    intersection = backend.sum(y_true_f * y_pred_f)
    return (2.*intersection+1)/(backend.sum(y_true_f)+backend.sum(y_pred_f)+1)

def dice_coef_loss(y_true, y_pred):
    return -dice_coef(y_true, y_pred)

def U_net(input_layer,
          input_filter = 16,
          input_kernel_size = (3,3), 
          second_kernel_size = (3,3), 
          third_kernel_size = (3,3), 
          pool_type ='max',
          activation = 'tanh', 
          optimizer = 'SGD', 
          dropout_rate = 0.25):
    
    # 1st layer: convolution
    # 512 -> 256
    conv1_1 = Conv2D(input_filter, input_kernel_size, activation='relu', 
                     padding="same")(input_layer)
    conv1_1 = Conv2D(input_filter, input_kernel_size, activation='relu', 
                     padding="same")(conv1_1)
    if pool_type == 'max':
        pool1_1 = MaxPooling2D(pool_size=(2, 2))(conv1_1)
    if pool_type == 'average':
        pool1_1 = AveragePooling2D(pool_size=(2, 2))(conv1_1)
    pool1_1 = Dropout(rate=dropout_rate)(pool1_1)

#------------------------------------------------------------------------------ 
    # 3rd layer: convolution 
    # 256 -> 128
    conv1 = Conv2D(input_filter*2, third_kernel_size, padding="same", 
                   activation=activation)(pool1_1)
    conv1 = Conv2D(input_filter*2, third_kernel_size, padding="same", 
                   activation=activation)(conv1)
    if pool_type == 'max':
        pool1 = MaxPooling2D(pool_size=(2, 2))(conv1)
    if pool_type == 'average':
        pool1 = AveragePooling2D(pool_size=(2, 2))(conv1)
    pool1 = Dropout(rate=0.5)(pool1)  
    
#------------------------------------------------------------------------------     
    # 5rd layer: convolution 
    # 128 -> 64
    conv2 = Conv2D(input_filter*4, third_kernel_size, padding="same", 
                   activation=activation)(pool1)
    conv2 = Conv2D(input_filter*4, third_kernel_size, padding="same", 
                   activation=activation)(conv2)
    if pool_type == 'max':
        pool2 = MaxPooling2D(pool_size=(2, 2))(conv2)
    if pool_type == 'average':
        pool2 = AveragePooling2D(pool_size=(2, 2))(conv2)
    pool2 = Dropout(rate=0.5)(pool2)    
    
#------------------------------------------------------------------------------
    # 7th layer: convolution
    # 64 -> 32
    conv3 = Conv2D(input_filter*8, third_kernel_size, padding="same", 
                   activation=activation)(pool2)
    conv3 = Conv2D(input_filter*8, third_kernel_size, padding="same", 
                   activation=activation)(conv3)  
    if pool_type == 'max':
        pool3 = MaxPooling2D(pool_size=(2, 2))(conv3)
    if pool_type == 'average':
        pool3 = AveragePooling2D(pool_size=(2, 2))(conv3)
    pool3 = Dropout(rate=0.5)(pool3)   

#------------------------------------------------------------------------------        
    # 9th layer: convolution
    # 32 -> 16
    conv4 = Conv2D(input_filter*16, third_kernel_size, padding="same", 
                   activation=activation)(pool3)
    conv4 = Conv2D(input_filter*16, third_kernel_size, padding="same", 
                   activation=activation)(conv4)
    if pool_type == 'max':
        pool4 = MaxPooling2D(pool_size=(2, 2))(conv4)
    if pool_type == 'average':
        pool4 = AveragePooling2D(pool_size=(2, 2))(conv4)
    pool4 = Dropout(rate=0.5)(pool4)  

#------------------------------------------------------------------------------        
    # 11th layer: convolution
    # 16 -> 8
    conv5 = Conv2D(input_filter*32, third_kernel_size, padding="same", 
                   activation=activation)(pool4)
    conv5 = Conv2D(input_filter*32, third_kernel_size, padding="same", 
                   activation=activation)(conv5)
    if pool_type == 'max':
        pool5 = MaxPooling2D(pool_size=(2, 2))(conv5)
    if pool_type == 'average':
        pool5 = AveragePooling2D(pool_size=(2, 2))(conv5)
    pool5 = Dropout(rate=0.5)(pool5)  

#------------------------------------------------------------------------------
    # Middle
    convm = Conv2D(input_filter*64, third_kernel_size, padding="same", 
                   activation=activation)(pool5) 
    convm = Conv2D(input_filter*64, third_kernel_size, padding="same", 
                   activation=activation)(convm)

#------------------------------------------------------------------------------       
    #13th layer 8 -> 16 concatenate
    deconv5 = Conv2DTranspose(input_filter*32, (3, 3), strides=(2, 2), 
                              padding="same")(convm)
    uconv5 = concatenate([deconv5, conv5]) #7th
    uconv5 = Dropout(rate=0.5)(uconv5)
    uconv5 = Conv2D(input_filter*32, third_kernel_size, padding="same", 
                    activation=activation)(uconv5) 
    uconv5 = Conv2D(input_filter*32, third_kernel_size, padding="same", 
                    activation=activation)(uconv5)

#------------------------------------------------------------------------------       
    # 14th layer 16 -> 32 concatenate
    deconv4 = Conv2DTranspose(input_filter*16, (3, 3), strides=(2, 2), 
                              padding="same")(uconv5)
    uconv4 = concatenate([deconv4, conv4]) #7th
    uconv4 = Dropout(rate=0.5)(uconv4)
    uconv4 = Conv2D(input_filter*16, third_kernel_size, padding="same", 
                    activation=activation)(uconv4) 
    uconv4 = Conv2D(input_filter*16, third_kernel_size, padding="same", 
                    activation=activation)(uconv4)

#------------------------------------------------------------------------------
    # 15th layer 32 -> 64 concatenate
    deconv3 = Conv2DTranspose(input_filter*8, (3, 3), strides=(2, 2), 
                              padding="same")(uconv4)
    uconv3 = concatenate([deconv3, conv3]) #5th
    uconv3 = Dropout(rate=0.5)(uconv3)
    uconv3 = Conv2D(input_filter*8, third_kernel_size, padding="same", 
                    activation=activation)(uconv3)
    uconv3 = Conv2D(input_filter*8, third_kernel_size, padding="same", 
                    activation=activation)(uconv3)
    
#------------------------------------------------------------------------------
    # 16th layer 64 -> 128 concatenate
    deconv2 = Conv2DTranspose(input_filter*4, (3, 3), strides=(2, 2), 
                              padding="same")(uconv3)
    uconv2 = concatenate([deconv2, conv2]) #3th
    uconv2 = Dropout(rate=0.5)(uconv2)
    uconv2 = Conv2D(input_filter*4, third_kernel_size, padding="same", 
                    activation=activation)(uconv2)
    uconv2 = Conv2D(input_filter*4, third_kernel_size, padding="same", 
                    activation=activation)(uconv2)

#------------------------------------------------------------------------------        
    #17th layer 128 -> 256 concatenate
    deconv1 = Conv2DTranspose(input_filter*2, (3, 3), strides=(2, 2), 
                              padding="same")(uconv2)
    uconv1 = concatenate([deconv1, conv1]) #1th
    uconv1 = Dropout(rate=0.5)(uconv1)
    uconv1 = Conv2D(input_filter, third_kernel_size, padding="same", 
                    activation=activation)(uconv1)  
    uconv1 = Conv2D(input_filter, third_kernel_size, padding="same", 
                    activation=activation)(uconv1) 

#------------------------------------------------------------------------------      
    #18th layer 256 -> 512 concatenate
    deconv1_1 = Conv2DTranspose(input_filter, (3, 3), strides=(2, 2), 
                                padding="same")(uconv1)
    uconv1_1 = concatenate([deconv1_1, conv1_1]) #1th
    uconv1_1 = Dropout(rate=0.5)(uconv1_1)
    uconv1_1 = Conv2D(input_filter, third_kernel_size, padding="same", 
                      activation=activation)(uconv1_1)  
    uconv1_1 = Conv2D(input_filter, third_kernel_size, padding="same", 
                      activation=activation)(uconv1_1) 

#------------------------------------------------------------------------------
    #output   
    output_layer = Conv2D(1, (1,1), padding="same", 
                          activation="sigmoid")(uconv1_1)
    return output_layer

img_size_target = 512
input_layer = Input(shape=(img_size_target, img_size_target, 1))
output_layer = U_net(input_layer, 16)

model = Model(input_layer, output_layer)
# model.summary()