from profanity_check import predict, predict_prob


def profanity(input_string):
    return {"string": input_string, "profanity": predict([input_string])}


def profanity_prob(input_string):
    return {"string": input_string, "profanity": predict_prob([input_string])}


def profanity_array(input_array):
    prof_array = []
    profane = False
    for string in input_array:
        test = profanity(string)
        prof_array.append(test)
        if test["profanity"] == 1:
            profane = True
    return prof_array, profane


def profanity_prob_array(input_array):
    prof_prob_array = []
    for string in input_array:
        prof_prob_array.append(profanity_prob(string))
    return prof_prob_array
