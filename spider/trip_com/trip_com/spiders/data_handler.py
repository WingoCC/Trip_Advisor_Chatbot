import json


def read_json_as_dict(data_path):
    with open(data_path, "r") as fp:
        return json.load(fp)


def write_dict_as_json(data_dict, data_path):
    with open(data_path, "w") as fp:
        json.dump(data_dict, fp, indent=2)


def get_data_samples(data_path, save_samples_path):
    trip_data = read_json_as_dict(data_path)
    samples = dict()
    for cur_sample in trip_data:
        if cur_sample["type"] not in samples.keys():
            samples[cur_sample["type"]] = cur_sample
    write_dict_as_json(samples, save_samples_path)


def group_by(item_list, type_name):
    return [item for item in item_list if item["type"] == type_name]


def data_grouping(data_path):
    trip_data = read_json_as_dict(data_path)
    inspirations_list = group_by(trip_data, "inspirations")
    toplists_list = group_by(trip_data, "toplists")
    destination_list = group_by(trip_data, "destination")
    attractions_list = group_by(trip_data, "attractions")
    attraction_list = group_by(trip_data, "attraction")

    write_dict_as_json(inspirations_list, "./collected_info/inspirations.json")
    write_dict_as_json(toplists_list, "./collected_info/toplists.json")
    write_dict_as_json(destination_list, "./collected_info/destination.json")
    write_dict_as_json(attractions_list, "./collected_info/attractions.json")
    write_dict_as_json(attraction_list, "./collected_info/attraction.json")


def find_attraction_in_attractions_list(attraction_name, attractions_list):
    for cur_attractions in attractions_list:
        for cur_attraction in cur_attractions["attractions"]:
            if cur_attraction["name"] == attraction_name:
                return cur_attraction


def find_destination_in_destination_list(destination_name, destination_list):
    for cur_destination in destination_list:
        if destination_name == cur_destination["name"]:
            return cur_destination


def find_destination_in_toplists(destination_name, inspiration_name, toplists):
    for cur_toplist in toplists:
        if inspiration_name == cur_toplist["inspiration"]:
            for cur_destination in cur_toplist["destinations"]:
                if destination_name + "," in cur_destination["name"]:
                    return cur_destination
    return dict()


def find_inspiration_in_inspirations(inspiration_name, inspiration_list):
    for cur_inspiration in inspiration_list:
        if inspiration_name == cur_inspiration["name"]:
            return cur_inspiration


def data_combination(data_path):
    attraction_list = read_json_as_dict("./collected_info/attraction.json")
    attractions_list = read_json_as_dict("./collected_info/attractions.json")
    destination_list = read_json_as_dict("./collected_info/destination.json")
    toplists_list = read_json_as_dict("./collected_info/toplists.json")
    inspiration_list = read_json_as_dict("./collected_info/inspirations.json")[0]["inspirations"]

    # combine attraction.json and attractions.json
    for cur_attraction in attraction_list:
        cur_attraction_in_attractions_list = find_attraction_in_attractions_list(cur_attraction["name"],
                                                                                 attractions_list)
        cur_attraction_in_attractions_list.update(cur_attraction)

    # write_dict_as_json(attractions_list, "./collected_info/attractions_bak.json")

    # combine attractions.json and destination.json
    for cur_attractions in attractions_list:
        cur_destination_in_destination_list = find_destination_in_destination_list(cur_attractions["destination"],
                                                                                   destination_list)
        cur_destination_in_destination_list["attractions"] = cur_attractions["attractions"]

    # write_dict_as_json(destination_list, "./collected_info/destination_bak.json")

    # combine destination.json and toplists.json
    for cur_destination in destination_list:
        cur_destination_in_toplist = find_destination_in_toplists(cur_destination["name"],
                                                                  cur_destination["toplist"],
                                                                  toplists_list)
        cur_destination_in_toplist.update(cur_destination)

    # write_dict_as_json(toplists_list, "./collected_info/toplists_bak.json")

    for cur_toplist in toplists_list:
        cur_inspiration_in_inspiration_list = find_inspiration_in_inspirations(cur_toplist["inspiration"], inspiration_list)
        cur_inspiration_in_inspiration_list.update(cur_toplist)

    write_dict_as_json(inspiration_list, "./collected_info/dataset.json")


if __name__ == "__main__":
    # get_data_samples("./trip_data.json", "./samples.json")

    # data_grouping("./trip_data.json")

    # data_combination("./trip_data.json")

    pass
