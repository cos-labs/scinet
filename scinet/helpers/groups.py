"""Helper functions for working with groups"""


def add_group(groups_collection, group_name):
    """Adds a new group to the groups collection if it doesn't already exit

    :param groups_collection: Mongo collection that maintains groups
    :param group_name: Name of group to be added

    :return: ObjectID of new group
    :return: None if group already exists
    """
    if not groups_collection.find({"group_name": group_name}).count():
        return groups_collection.insert({
                                "group_name": group_name,
                                "attempted_submissions": 0,
                                "successful_submissions": 0
                                })
    else:
        return None


def get_groups(groups_collection):
    """Returns a list of group names

    :param groups_collection: Mongo collection that maintains groups

    :return: List of group names
    """
    groups = groups_collection.find()
    return [group for group in groups]
