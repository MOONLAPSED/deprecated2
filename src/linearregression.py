# Initializing weights and bias
weights = [0.0, 0.0]  # Assuming we have 2 features
bias = 0.0
learning_rate = 0.1  # A small number to control the step size
epochs = 10  # Number of times to iterate over the training set

# Sample dataset (X) and corresponding labels (Y)
X = [[0, 0], [0, 1], [1, 0], [1, 1]]  # Example inputs
Y = [0, 0, 0, 1]  # Example outputs (AND logic)

# Training loop
for epoch in range(epochs):
    total_error = 0  # To track the error for this epoch
    for i in range(len(X)):
        # Forward propagation: calculate the predicted output
        z = weights[0] * X[i][0] + weights[1] * X[i][1] + bias  # Weighted sum
        Y_predicted = 1 if z > 0 else 0  # Step function (activation)

        # Calculate the error
        error = Y[i] - Y_predicted
        total_error += abs(error)  # Accumulate the absolute error

        # Update weights and bias
        weights[0] += learning_rate * error * X[i][0]
        weights[1] += learning_rate * error * X[i][1]
        bias += learning_rate * error

    # Print the error for the epoch
    print(f"Epoch: {epoch}, Total Error: {total_error}")

# Final weights and bias after training
print("Final weights:", weights)
print("Final bias:", bias)

# Example of making predictions after training
for i in range(len(X)):
    z = weights[0] * X[i][0] + weights[1] * X[i][1] + bias
    Y_predicted = 1 if z > 0 else 0
    print(f"Input: {X[i]}, Predicted: {Y_predicted}, Actual: {Y[i]}")