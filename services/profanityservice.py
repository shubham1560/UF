from profanity_check import predict, predict_prob


def profanity(input_string):
    return {"string": input_string, "profanity": predict([input_string])}


def profanity_prob(input_string):
    return {"string": input_string, "profanity": predict_prob([input_string])}


def profanity_array(input_array):
    prof_array = []
    for string in input_array:
        prof_array.append(profanity(string))
    return prof_array


def profanity_prob_array(input_array):
    prof_prob_array = []
    for string in input_array:
        prof_prob_array.append(profanity_prob(string))
    return prof_prob_array
