from keras.layers import Input, Dense, LeakyReLU, Concatenate, Reshape, Conv2D, Flatten
from keras.models import Model
from keras.optimizers import Adam
import keras.backend as K
import tensorflow as tf

class CriticNetwork(object):
    def __init__(self, sess, state_size, action_size, tau, lr):
        self.sess = sess
        self.tau = tau
        self.lr = lr
        self.action_size = action_size
        self.state_size = state_size

        K.set_session(sess)

        # Now create the model
        self.model, self.action, self.state = self.create_critic_network()
        self.action_grads = tf.gradients(self.model.output, self.action)
        self.sess.run(tf.initialize_all_variables())

    def gradients(self, states, actions):
        return self.sess.run(self.action_grads, feed_dict={
            self.state: states,
            self.action: actions
        })[0]

    # def target_train(self):
    #     critic_weights = self.model.get_weights()
    #     critic_target_weights = self.target_model.get_weights()
    #     for i in range(len(critic_weights)):
    #         critic_target_weights[i] = self.tau * critic_weights[i] + (1 - self.tau) * critic_target_weights[i]
    #     self.target_model.set_weights(critic_target_weights)

    def create_critic_network(self):
        state_input = Input(shape=(self.state_size,))
        action_input = Input(shape=(self.action_size,))


        main_network = Dense(2048)(state_input)
        main_network = LeakyReLU()(main_network)

        concat_network = Concatenate()([main_network, action_input])
        concat_network = Dense(2048)(concat_network)
        concat_network = LeakyReLU()(concat_network)
        concat_network = Dense(2048)(concat_network)
        concat_network = LeakyReLU()(concat_network)

        value_prediction = Dense(1, name='value_prediction')(concat_network)
        critic = Model(inputs=[state_input, action_input], outputs=value_prediction)
        critic.compile(optimizer=Adam(lr=self.lr), loss='mse')
        critic.summary()

        return critic, action_input, state_input