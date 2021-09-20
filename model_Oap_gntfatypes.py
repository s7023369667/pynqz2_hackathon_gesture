from tensorflow.keras.models import Model
from tensorflow.keras.layers import *
from tensorflow.keras import optimizers
#from termcolor import colored, cprint
#import tensorflow_addons as tfa
from GN import GroupNormalization
import keras.backend as K

'''
  model_OaP_in0_tiny
  channel=64
  self madeup tensorflow-addons GroupNormalization
'''

def OaP_GD_loss(y_true ,y_pred):
    qq = 0.00001
    LF= K.switch(K.equal(y_true,1),
         lambda: -1*K.pow( (1-y_pred) ,2) * K.log(y_pred+qq),
         lambda: -1*K.pow( (1-y_true) ,4) * K.pow(y_pred,2) * K.log(1-y_pred+qq))
    return LF
    # y_true = 1  K.pow( (1-y_pred) ,2) * K.log(y_pred)
    # else        K.pow( (1-y_true) ,4) * K.pow(y_pred,2) * K.log(1-y_pred)

def build_model(input_shape, dim, odim):
    #cprint(colored('Now Import Model_OaP_in0_tiny'),'magenta','on_grey')

    In = Input(shape=(input_shape, dim), name='In')
    NML = GroupNormalization(groups=6,name='Gp')(In)

    ''' part1 : Backbone+最右邊分支(Regularization)'''
    conv1_1 = Conv1D(32*2, 3, strides=1, padding='valid',activation=None, use_bias=False, name='conv1_1')(NML)  # (?, 48, 64)
    relu1_1 = Activation('relu', name='relu1_1')(conv1_1)
    NML1_1 = GroupNormalization(groups=16,name='Gp1_1')(relu1_1)

    conv1_2 = Conv1D(32*2, 2, strides=2, padding='valid',activation=None, use_bias=False, name='conv1_2')(NML1_1)  # (?, 24, 64)
    relu1_2 = Activation('relu', name='relu1_2')(conv1_2)
    NML1_2 = GroupNormalization(groups=16, name='Gp1_2')(relu1_2)

    conv1_3 = Conv1D(32*2, 2, strides=2, padding='valid', activation=None, use_bias=False, name='conv1_3')(NML1_2)  # (?, 12, 64)
    relu1_3 = Activation('relu', name='relu1_3')(conv1_3)
    NML1_3 = GroupNormalization(groups=16, name='Gp1_3')(relu1_3)

    us1_1  = UpSampling1D(size=2,name='us1_1')(NML1_3)  # (?, 24, 128) -> 為了能和 short_2 add
    add1_1 = add([NML1_2,us1_1], name='add1_1')  # Short-cut add NML1_2
    us1_2 = UpSampling1D(size=2, name='us1_2')(add1_1)  # (?, 48, 128) -> 為了能和 short_1 add
    add1_2 = add([NML1_1, us1_2], name='add_2')  # Short-cut add NML1_1

    conv1_4 = Conv1D(32*2 , 2, strides=1, padding='valid', activation=None, use_bias=False, name='conv1_4')(
        add1_2)  # (?, 47, 128)
    relu1_4 = Activation('relu', name='relu1_4')(conv1_4)
    NML1_4 = GroupNormalization(groups=16, name='Gp1_4')(relu1_4)
    pl1_4 = AveragePooling1D(pool_size=4, strides=2, padding='valid', name='pl1_4')(NML1_4)
    flt1_4 = Flatten(name='flt1_4')(pl1_4)

    output_1 = Dense(odim, activation='softmax', name='output_1')(flt1_4)  # (?, 12)
    '''part1 end'''
    ''' part2 Backbone+最左邊分支(PKI)'''
    conv2_1 = Conv1D(32*2, 2, strides=1, padding='valid', activation=None, use_bias=False, name='conv2_1')(
        NML1_4)  # (?, 46, 128)
    relu2_1 = Activation('relu', name='relu2_1')(conv2_1)
    NML2_1 = GroupNormalization(groups=16, name='Gp2_1')(relu2_1)

    conv2_2 = Conv1D(32*2 , 2, strides=1, padding='valid', activation=None, use_bias=False, name='conv2_2')(
        NML2_1)  # (?, 45, 128)
    relu2_2 = Activation('relu', name='relu2_2')(conv2_2)
    NML2_2 = GroupNormalization(groups=16, name='Gp2_2')(relu2_2)
    pl2_2 = AveragePooling1D(pool_size=4, strides=2, padding='valid', name='pl2_2')(NML2_2)
    flt2_2 = Flatten(name='flt2_2')(pl2_2)

    output_2 = Dense(odim, activation='softmax', name='output_2')(flt2_2)  # (?, 12)
    '''part2 end'''
    ''' part3 Backbone+中間分支(SKI)'''
    conv3_1 = Conv1D(32*2, 2, strides=1, padding='valid', activation=None, use_bias=False, name='conv3_1')(
        NML1_4)  # (?, 46, 128)
    relu3_1 = Activation('relu', name='relu3_1')(conv3_1)
    NML3_1 = GroupNormalization(groups=16, name='Gp3_1')(relu3_1)

    conv3_2 = Conv1D(32*2, 2, strides=1, padding='valid', activation=None, use_bias=False, name='conv3_2')(
        NML3_1)  # (?, 45, 128)
    relu3_2 = Activation('relu', name='relu3_2')(conv3_2)
    NML3_2 = GroupNormalization(groups=16, name='Gp3_2')(relu3_2)
    pl3_2 = AveragePooling1D(pool_size=4, strides=2, padding='valid', name='pl3_2')(NML3_2)
    flt3_2 = Flatten(name='flt3_2')(pl3_2)

    output_3 = Dense(odim, activation='softmax', name='output_3')(flt3_2)  # (?, 12)
    '''part3 end'''
    ##Compile
    model = Model(inputs=In, outputs=[output_1 ,output_2 ,output_3])
    Ada = optimizers.Adadelta(learning_rate=1)
    model.compile(loss=[OaP_GD_loss, OaP_GD_loss, OaP_GD_loss], optimizer=Ada, metrics=['accuracy'])

    return model


if __name__ == '__main__':
    model_main = build_model(50, 6, 6)
    model_main.summary()
