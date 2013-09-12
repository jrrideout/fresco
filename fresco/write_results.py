import numpy as np

def write_to_file(lines, filepath):
    f = open(filepath, 'w')
    for line in lines:
        f.write(line+"\n")
    f.close()

def fold_features_output_lines(fold_outcomes, problem_data):
    lines = []
    
    properties = []
    for fold_index in range(len(fold_outcomes)):
        rec_list = fold_outcomes[fold_index].feature_vector.get_record_list()
        populations = [problem_data.get_feature_abundance(record.get_scope(), record.get_id()) for record in rec_list]    
        pred_scores = fold_outcomes[fold_index].feature_scores
    
        properties += sorted([(fold_index, rec_list[index].get_scope(), rec_list[index].get_id(), pred_scores[index],
                       populations[index]) for index in range(len(rec_list))], key=lambda prop:prop[3], reverse=True)

    header = ("FOLD_NUMBER", "GROUP_ID", "GROUP_SCOPE", "GROUP_SCORE", "GROUP_ABUNDANCE")
    properties[:0] = [header]

    for prop in properties:
        line = ""
        for i in range(len(prop)):
            line += str(prop[i])
            if i != len(prop) - 1:
                line += "\t"
        lines.append(line)
        
    return lines

def feature_output_lines(outcome, problem_data):
    lines = []
    
    feature_vector = outcome.feature_vector

    rec_list = feature_vector.get_record_list()
    populations = [problem_data.get_feature_abundance(record.get_scope(), record.get_id()) for record in rec_list]    
    pred_scores = outcome.feature_scores

    properties = [(rec_list[index].get_id(), rec_list[index].get_scope(), pred_scores[index],
                   populations[index]) for index in range(len(rec_list))] 
    properties.sort(key=lambda prop:prop[2], reverse=True)

    header = ("GROUP_ID", "GROUP_SCOPE", "GROUP_SCORE", "GROUP_ABUNDANCE")
    properties[:0] = [header]

    for prop in properties:
        line = ""
        for i in range(len(prop)):
            line += str(prop[i])
            if i != len(prop) - 1:
                line += "\t"
        lines.append(line)
        
    return lines
    
def testing_output_lines(testing_output):
    lines = []

    header = ("ITERATION", "AVG_PREDICTION_SCORE", "STD_DEV_PREDICTION_SCORE")
    properties = [header]

    for iteration in range(len(testing_output)):
        results = np.array([outcome.prediction_quality for outcome in testing_output[iteration]])
        avg = np.mean(results)
        std = np.std(results)
        properties.append( (iteration, avg, std) ) 

    for prop in properties:
        line = ""
        for i in range(len(prop)):
            line += str(prop[i])
            if i != len(prop) - 1:
                line += "\t"
        lines.append(line)
            
    return lines