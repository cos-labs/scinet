"""
Takes a list of similar JSON's and returns a Conflict JSON
Author: Harry Rybacki
Created on: 15June2013
"""


def get_conflicts(JSON):
    """
    @params:    list of similar JSON objects

    @returns:   JSON object containing a dict of conflicting values and a dict
                of agreed upon fields.
    """
    import uuid
    # fields we don't want to to the Conflict data structure
    ignored_fields = [unicode("id")]
    # create a container to store fields with possible values
    fields_container = {}
    # and a counter to track how many citations have a given field
    fields_counter = {}
    # determine the number of citations within this matched group
    number_of_dicts = len(JSON)

    # for every citation within a matched group
    for dict in JSON:
        # grab every field and possible_value
        for field, possible_value in dict.iteritems():
            # skip field if we don't care about it
            if field in ignored_fields:
                pass
            else:
                # if this field hasn't been seen before
                if field not in fields_container:
                    # add a list to container to store possible values
                    fields_container[field] = []
                    # and add a counter to track the number of citations with said field
                    fields_counter[field] = 0

                # if unique, add the possible value to its respective field 'list'
                if possible_value not in fields_container[field]:
                    fields_container[field].append(possible_value)

                # increment the number of citations containing this field
                fields_counter[field] += 1

    # create the new conflict data structure
    results = {
        "conflicts_bin": {},
        "resolved_bin": {}
    }

    # for every field found in the citations
    for field, possible_values in fields_container.iteritems():
        # if _all_ citations had the same value
        # @todo: modify to at least 2
        if len(possible_values) is 1 and fields_counter[field] is number_of_dicts:
            # put it in the resolved bucket
            results["resolved_bin"][field] = possible_values[0]
        # otherwise, add it to the conflict bucket
        else:
            results["conflicts_bin"][field] = possible_values

    # scrub conflicts to unique ids and 'votes'
    temp_conflicts = {}

    # for every field and possible value
    for field, possible_values in results['conflicts_bin'].items():
        # create a list to store the value with id/votes
        values = []
        # transform into dict with id/votes and append to container
        for value in possible_values:
            values.append({
                "value": value,
                "id": uuid.uuid4().hex,
                "votes": 0
            })
        # add transformed values to new conflicts dict
        temp_conflicts[field] = values

    # add completed conflicts dict to dict for processing
    results['conflicts_bin'] = temp_conflicts
    return results