from utils.preprocess import *
from utils.model import create_model

# import and clean data
question, answer = import_movie_data("./data/movie_lines.txt", "./data/movie_conversations.txt")

question = [clean_text(ques) for ques in question]
answer = [clean_text(ans) for ans in answer]

pairs = list(zip(question, answer))

# tokenize
docs, tokens, num_token = add_token(pairs, pairsnum=1000)
input_docs, target_docs = docs
input_tokens, target_tokens = tokens
num_encoder_tokens, num_decoder_tokens = num_token

# create feature and token dictionary
feature, reversed_feature = create_feature_dict(input_tokens, target_tokens)
input_features_dict, target_features_dict = feature
reverse_input_features_dict, reverse_target_features_dict = reversed_feature

# create training data
encoder_input_data, decoder_data, seq_length = create_training_data(
    input_docs, target_docs, num_encoder_tokens, num_decoder_tokens, input_features_dict, target_features_dict)

decoder_input_data, decoder_target_data = decoder_data
max_encoder_seq_length, max_decoder_seq_length = seq_length


#The batch size and number of epochs
batch_size = 8
epochs = 600

# create model
model = create_model(num_encoder_tokens, num_decoder_tokens)

model.fit([encoder_input_data, decoder_input_data], decoder_target_data, batch_size = batch_size, epochs = epochs, validation_split = 0.2)
model.save('model/model.h5')