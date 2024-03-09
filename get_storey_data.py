def get_story_data(sap_model):
    """
    returns:
    story_data (list). The is a nested list with each element consists of
    [story_nm,story_ele,story_hgt,is_master_story,similar_to,splice_above,
     splice_height]
    """
    #Get the data using API
    story_in=sap_model.Story.GetStories()
    #print(f"{dir(sap_model) = }")
    #print(f"{dir(sap_model.Story) = }")
    #print(f"{type(sap_model.Story) = }")
    print(f"{sap_model.Story.__doc__ = }")
    #print(f"{story_in[0] = }")
    #Separate the data to lists
    nos_stories=story_in[0]
    story_nms=story_in[1]
    story_eles=story_in[2]
    story_hgts=story_in[3]
    is_master_story=story_in[4]
    similar_to_story=story_in[5]
    splice_above=story_in[6]
    splice_height=story_in[7]

    #Combine data into one list called story_data
    story_data=[]
    for i in range(len(story_nms)):
        j=-1-i
        story_data.append([story_nms[j],
                           round(story_hgts[j],3),
                           round(story_eles[j],3),
                           is_master_story[j],
                           similar_to_story[j],
                           splice_above[j],
                           splice_height[j]])
    return story_data