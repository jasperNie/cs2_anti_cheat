import sqlite3
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

conn = sqlite3.connect('all_players_data.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM all_player_stats')
data = cursor.fetchall()
conn.close()

X = np.array([row[3:] for row in data])
y = np.array([row[2] for row in data])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

model = tf.keras.Sequential([
    tf.keras.layers.Dense(units=20, activation='relu', input_shape=(X_train.shape[1],)),
    tf.keras.layers.Dense(units=20, activation='relu'),
    tf.keras.layers.Dense(units=20, activation='relu'),
    tf.keras.layers.Dense(units=1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='mean_squared_error', metrics=['mean_absolute_error'])  # Change loss to mean_squared_error

history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test))

test_loss, test_mae = model.evaluate(X_test, y_test)
print('Test Mean Absolute Error:', test_mae)

model.save('cs2_anti_cheat_model.h5')